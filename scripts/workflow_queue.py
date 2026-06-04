#!/usr/bin/env python3
import argparse
import asyncio
import sys
import time
from pathlib import Path


OUTPUT_DIR = Path("/mnt/data/comfyui/output")


def read_matrix(path):
    workflows = []
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            workflows.append(line)
    return workflows


def existing_output_count(run_id, workflow):
    prefix = f"{run_id}_{Path(workflow).stem}"
    return len(list(OUTPUT_DIR.glob(f"{prefix}_*.png")))


async def run_job(name, base_url, workflow, args, repo_root):
    cmd = [
        sys.executable,
        str(repo_root / "scripts" / "workflow_prompt.py"),
        "-w",
        workflow,
        "--base-url",
        base_url,
        "--timeout",
        args.timeout,
    ]
    if args.prompt is not None:
        cmd.extend(["--prompt", args.prompt])
    if args.batch is not None:
        cmd.extend(["--batch", str(args.batch)])
    if args.seed is not None:
        cmd.extend(["--seed", str(args.seed)])
    if args.id is not None:
        cmd.extend(["--id", args.id])
    if args.dry_run:
        cmd.append("--dry-run")

    started = time.monotonic()
    print(f"START {name} {workflow}", flush=True)
    process = await asyncio.create_subprocess_exec(
        *cmd,
        cwd=repo_root,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    async for line in process.stdout:
        print(f"{name} {workflow}: {line.decode().rstrip()}", flush=True)

    rc = await process.wait()
    elapsed = time.monotonic() - started
    if rc:
        print(f"FAIL {name} {workflow} ({elapsed:.1f}s)", flush=True)
        return False

    print(f"DONE {name} {workflow} ({elapsed:.1f}s)", flush=True)
    return True


async def worker(name, base_url, queue, failures, args, repo_root):
    while True:
        try:
            workflow = queue.get_nowait()
        except asyncio.QueueEmpty:
            return

        try:
            if args.id is not None and not args.dry_run:
                expected = args.batch or 1
                existing = existing_output_count(args.id, workflow)
                if existing >= expected:
                    print(
                        f"SKIP {name} {workflow}: found {existing}/{expected} output PNGs",
                        flush=True,
                    )
                    continue
                if existing:
                    print(
                        f"WARN {name} {workflow}: found partial {existing}/{expected} output PNGs; skipping",
                        flush=True,
                    )
                    continue

            ok = await run_job(name, base_url, workflow, args, repo_root)
            if not ok:
                failures.append((name, workflow))
        except Exception as exc:
            print(f"ERROR {name} {workflow}: {exc}", flush=True)
            failures.append((name, workflow))
        finally:
            queue.task_done()


async def main_async(args):
    repo_root = Path(__file__).resolve().parents[1]
    workflows = args.workflow or read_matrix(repo_root / args.matrix)
    workers = [f"http://127.0.0.1:{8188 + i}" for i in range(args.workers)]

    queue = asyncio.Queue()
    for workflow in workflows:
        queue.put_nowait(workflow)

    failures = []
    tasks = [
        asyncio.create_task(worker(f"worker-{i}", base_url, queue, failures, args, repo_root))
        for i, base_url in enumerate(workers, start=1)
    ]
    await asyncio.gather(*tasks)

    if failures:
        print("FAILED JOBS:", flush=True)
        for name, workflow in failures:
            print(f"{name} {workflow}", flush=True)
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt")
    parser.add_argument("--matrix", default="workflows/test_matrix.txt")
    parser.add_argument("-w", "--workflow", action="append")
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--timeout", default="600")
    parser.add_argument("-b", "--batch", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--id")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    assert args.workers > 0, "--workers must be positive"

    raise SystemExit(asyncio.run(main_async(args)))


if __name__ == "__main__":
    main()
