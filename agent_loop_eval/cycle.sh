#!/usr/bin/env bash
# Keep working run 9 until all 100 tasks are done.
#
# One pass of run9.py stops when its chunk is finished or every key is spent. Neither is a
# reason to stop for good -- keys recover from per-minute limits within the minute -- so this
# keeps invoking it until the trace count reaches 100 or stops moving.
#
# Concurrency is enforced by run9.py's own lock file, not by a check here. An earlier version
# of this script guarded with `pgrep -f`, which matches nothing against Windows process
# command lines under Git Bash: it started a second run on top of a live one, where each
# deletes the traces the other is writing. A supervisor cannot reliably detect the thing it
# supervises on this platform, so the process that owns the data refuses duplicates instead.
cd "$(dirname "$0")" || exit 1
PY=../.venv/Scripts/python.exe
LOCK=run9_retry_loop/run9.lock

traces() { ls run9_retry_loop/task-*.json 2>/dev/null | wc -l; }

# Wait out any run already in flight, by its lock rather than by process table.
while [ -f "$LOCK" ]; do
  echo "[cycle] run in progress ($(traces)/100 traces); waiting"
  sleep 60
done

for pass in $(seq 1 12); do
  before=$(traces)
  if [ "$before" -ge 100 ]; then
    echo "[cycle] all 100 tasks complete"
    break
  fi

  echo "[cycle] pass $pass starting at $before/100"
  # Unbuffered: a buffered run shows nothing until it exits, so a pass failing every call
  # on a dead key looks identical to a pass working normally.
  $PY -u run9.py 12
  status=$?
  after=$(traces)

  if [ "$status" -ne 0 ] && [ -f "$LOCK" ]; then
    echo "[cycle] another run holds the lock; stopping so the two do not collide"
    break
  fi
  if [ "$after" -le "$before" ]; then
    # No progress: every key is throttled or spent. Back off rather than spin on it.
    echo "[cycle] pass $pass added nothing; waiting 10 min"
    sleep 600
  fi
done

echo "[cycle] finished at $(traces)/100"
