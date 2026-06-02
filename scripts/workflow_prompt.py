#!/usr/bin/env python3
import argparse
import json
import subprocess
import tempfile
from pathlib import Path


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

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_workflow = Path(tmpdir) / "workflow.json"
        tmp_workflow.write_text(json.dumps(workflow, indent=2) + "\n")
        subprocess.run(
            [
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
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
