#!/usr/bin/env bash
# Hand off from the chunk that is already running to the self-repeating cycle.
#
# That chunk was started before run9.py had a lock file, so it holds none and cycle.sh's
# lock wait would fall straight through. This waits on its actual process id instead, via
# tasklist -- pgrep sees nothing on Windows, which is what caused the collision this avoids.
cd "$(dirname "$0")" || exit 1

WAIT_PID=${1:?usage: start_cycle.sh <pid-to-wait-for>}

while tasklist //FI "PID eq $WAIT_PID" //NH 2>/dev/null | grep -q "$WAIT_PID"; do
  sleep 60
done
echo "[handoff] pid $WAIT_PID finished; starting cycle"

exec bash cycle.sh
