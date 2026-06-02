#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path


BATCH_INDEX = {
    "EmptyLatentImage": 2,
    "EmptySD3LatentImage": 2,
    "EmptyFlux2LatentImage": 2,
    "📐 Resolution Image Size Selector": 10,
}

SEED_INDEX = {
    "RandomNoise": 0,
    "KSampler": 0,
    "KSamplerAdvanced": 1,
    "KSampler //Inspire": 0,
    "SeedVarianceEnhancer": 4,
}


def is_oom_output(text):
    lower = text.lower()
    oom_markers = [
        "out of memory",
        "cuda out of memory",
        "torch.outofmemoryerror",
        "allocation on device",
    ]
    return any(marker in lower for marker in oom_markers)


def run_workflow(cmd):
    result = subprocess.run(
        cmd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode == 0:
        if result.stdout:
            print(result.stdout, end="")
        return

    if is_oom_output(result.stdout or ""):
        raise RuntimeError("CUDA OOM error")

    if result.stdout:
        print(result.stdout, end="", file=sys.stderr)
    raise subprocess.CalledProcessError(result.returncode, cmd)


def free_memory(base_url):
    data = json.dumps({"unload_models": True, "free_memory": True}).encode()
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/free",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        response.read()


def main():
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser()
    parser.add_argument("prompt_file")
    parser.add_argument(
        "-w",
        "--workflow",
        default="workflows/flux-2/dev/original/flux2_dev_original.json",
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8188")
    parser.add_argument("--timeout", default="600")
    parser.add_argument("-b", "--batch", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--id")
    args = parser.parse_args()

    workflow_path = Path(args.workflow)
    if not workflow_path.is_absolute():
        workflow_path = repo_root / workflow_path

    workflow = json.loads(workflow_path.read_text())
    prompt = Path(args.prompt_file).read_text().strip()

    prompt_nodes = [n for n in workflow["nodes"] if n.get("type") == "CLIPTextEncode"]

    if len(prompt_nodes) == 1:
        prompt_node = prompt_nodes[0]
    else:
        positive_nodes = [
            n for n in prompt_nodes if "positive" in (n.get("title") or "").lower()
        ]
        assert len(positive_nodes) == 1, "expected exactly one positive CLIPTextEncode node"
        prompt_node = positive_nodes[0]

    if prompt_node.get("widgets_values"):
        prompt_node["widgets_values"][0] = prompt
    else:
        prompt_node["widgets_values"] = [prompt]

    if args.batch is not None:
        batch_nodes = [n for n in workflow["nodes"] if n.get("type") in BATCH_INDEX]
        assert len(batch_nodes) == 1, "expected exactly one batch-size node"
        batch_node = batch_nodes[0]
        batch_node["widgets_values"][BATCH_INDEX[batch_node["type"]]] = args.batch

    if args.seed is not None:
        seed_nodes = [n for n in workflow["nodes"] if n.get("type") in SEED_INDEX]
        assert seed_nodes, "expected at least one seed node"
        for seed_node in seed_nodes:
            seed_node["widgets_values"][SEED_INDEX[seed_node["type"]]] = args.seed

    if args.id is not None:
        save_nodes = [n for n in workflow["nodes"] if n.get("type") == "SaveImage"]
        assert len(save_nodes) == 1, "expected exactly one SaveImage node"
        save_nodes[0]["widgets_values"][0] = f"{args.id}_{workflow_path.stem}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_workflow = Path(tmpdir) / "workflow.json"
        tmp_workflow.write_text(json.dumps(workflow, indent=2) + "\n")
        cmd = [
            "docker",
            "run",
            "--rm",
            "--network",
            "host",
            "--ipc=host",
            "-v",
            f"{repo_root}:/work:ro",
            "-v",
            f"{tmpdir}:/input:ro",
            "-w",
            "/tmp",
            "mcr.microsoft.com/playwright:v1.57.0-noble",
            "sh",
            "-lc",
            "npm init -y >/dev/null && "
            "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 "
            "npm install playwright@1.57.0 >/dev/null && "
            "cp /work/scripts/gui_workflow_smoke.mjs . && "
            'node gui_workflow_smoke.mjs --base-url "$1" '
            '--submit --wait --timeout "$2" /input/workflow.json',
            "sh",
            args.base_url,
            args.timeout,
        ]

        try:
            free_memory(args.base_url)
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    run_workflow(cmd)
                    break
                except RuntimeError as exc:
                    if str(exc) != "CUDA OOM error":
                        raise
                    if attempt == max_attempts - 1:
                        print("CUDA OOM error", flush=True)
                        raise SystemExit(1)
                    print("CUDA OOM error; retrying", flush=True)
                    time.sleep(2)
                except subprocess.CalledProcessError:
                    if attempt == max_attempts - 1:
                        raise
                    print("workflow failed; retrying", flush=True)
                    time.sleep(2)
        finally:
            free_memory(args.base_url)


if __name__ == "__main__":
    main()
