"""Run 9 in chunks: work N tasks, then score and analyse, without losing progress.

A full 100-task pass costs more model quota than is available in one sitting, and the
earlier attempt at one proved the risk -- a crash at task 51 threw away 25 minutes of work
because nothing was resumable. Everything here is resumable at task granularity:

  * a task whose trace file exists is never re-run;
  * requirement groups are cached per task, so re-scoring is free;
  * attribution verdicts are cached per capability, so re-analysing is free.

So this can be invoked as many times as it takes. Each call works the next CHUNK unfinished
tasks, then rebuilds the reports over everything finished so far -- the reports are always
current for the tasks that exist, rather than only appearing at the end.

    python run9.py            # next 10 tasks, then score + analyse
    python run9.py 25         # next 25 instead
    python run9.py 0          # score + analyse only, run no new tasks
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import agent_loop_evaluation as loop
from agent_loop_evaluation import ROOT, USE_CASES_FILE, parse_use_cases

RUN_DIR = ROOT / "run9_retry_loop"
CHUNK = 10

# A lock older than this belonged to a run that was killed before it could clean up. Set
# well above the slowest observed chunk so a live run is never mistaken for a dead one.
STALE_LOCK_SECONDS = 2 * 60 * 60


def done_tasks() -> set[int]:
    """Tasks genuinely finished, not merely written to disk.

    A task stopped by quota still gets a trace saved, and the runner skips any task whose
    trace exists -- so without this check the first quota stop would permanently mark every
    remaining task as done. It happened on the first chunk: tasks 6-10 were saved with zero
    queries and would never have been retried.
    """
    finished = set()
    for path in RUN_DIR.glob("task-*.json"):
        try:
            trace = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            path.unlink()          # truncated by an interrupted write; redo it
            continue
        if trace.get("error") or not trace.get("queries"):
            path.unlink()          # quota stop or crash; redo it
            continue
        finished.add(int(path.stem.split("-")[-1]))
    return finished


def run_chunk(size: int) -> int:
    """Run the next `size` unfinished tasks. Returns how many were actually run."""
    cases = parse_use_cases(USE_CASES_FILE)
    todo = [c for c in cases if c.identifier not in done_tasks()][:size]
    if not todo:
        return 0

    # The runner writes to its own TRACE_DIR and skips tasks already there, so pointing it
    # at the run directory makes resume automatic rather than something to coordinate here.
    loop.TRACE_DIR = RUN_DIR
    loop.NUM_TASKS = max(c.identifier for c in todo)
    print(f"[run9] running tasks {[c.identifier for c in todo]}")
    loop.main()
    return len(todo)


def score_and_analyse() -> None:
    for script in ("score_with_groups.py", "analyse_failures.py"):
        print(f"\n[run9] {script} over {len(done_tasks())} tasks")
        result = subprocess.run([sys.executable, str(ROOT / script), RUN_DIR.name],
                                cwd=ROOT, text=True)
        if result.returncode != 0:
            print(f"[run9] {script} exited {result.returncode}; reports may be stale")
            return


def acquire_lock() -> Path | None:
    """Refuse to start while another run9 is working the same directory.

    Two concurrent runs corrupt each other rather than going faster: `done_tasks` deletes
    any trace that looks unfinished, so one process deletes the file the other is midway
    through writing, and both then redo the same task against a shared per-minute rate
    limit. This happened -- a supervisor script's `pgrep` guard silently matched nothing on
    Windows and started a second run alongside the first.

    O_EXCL makes the check and the claim one step, so two processes starting together
    cannot both win.
    """
    lock = RUN_DIR / "run9.lock"
    try:
        handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        age = time.time() - lock.stat().st_mtime
        if age < STALE_LOCK_SECONDS:
            owner = lock.read_text(encoding="utf-8").strip()
            print(f"[run9] another run is active (lock held by {owner}, "
                  f"{age / 60:.0f} min old); exiting rather than corrupting its traces")
            return None
        print(f"[run9] clearing stale lock ({age / 60:.0f} min old)")
        lock.unlink(missing_ok=True)
        handle = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    os.write(handle, f"pid {os.getpid()}".encode())
    os.close(handle)
    return lock


def main() -> None:
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    size = CHUNK
    if len(sys.argv) > 1:
        size = int(sys.argv[1])

    lock = acquire_lock()
    if lock is None:
        sys.exit(1)
    try:
        run(size)
    finally:
        lock.unlink(missing_ok=True)


def run(size: int) -> None:
    """Work the next `size` unfinished tasks, then rebuild the reports over everything done."""
    before = len(done_tasks())
    if size:
        run_chunk(size)
    after = len(done_tasks())
    print(f"\n[run9] tasks complete: {after}/100  (+{after - before} this call)")

    if after:
        score_and_analyse()

    remaining = 100 - after
    print(f"\n[run9] {remaining} tasks remaining" if remaining else "\n[run9] all 100 done")
    if remaining:
        print("[run9] run this again to continue; nothing already finished is repeated")


if __name__ == "__main__":
    main()
