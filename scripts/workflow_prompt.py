#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid
from pathlib import Path


BATCH_INDEX = {
    "EmptyLatentImage": 2,
    "EmptySD3LatentImage": 2,
    "EmptyFlux2LatentImage": 2,
    "📐 Resolution Image Size Selector": 10,
}

LATENT_RESOLUTION_TYPES = {
    "EmptyLatentImage",
    "EmptySD3LatentImage",
    "EmptyFlux2LatentImage",
}

SEED_INDEX = {
    "RandomNoise": 0,
    "KSampler": 0,
    "KSamplerAdvanced": 1,
    "KSampler //Inspire": 0,
    "SeedVarianceEnhancer": 4,
}

TRIGGER_REQUIRED_VALUES = {"required", "optional", "no", "unknown"}


def parse_prompt_file(path):
    text = Path(path).read_text()
    if "\n---\n" not in text:
        return {}, text.strip()

    metadata_text, prompt = text.split("\n---\n", 1)
    metadata = json.loads(metadata_text)
    assert isinstance(metadata, dict), "expected prompt metadata to be a JSON object"
    return metadata, prompt.strip()


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


def post_json(base_url, route, payload):
    data = json.dumps(payload).encode()
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}{route}",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        text = response.read().decode()
    return json.loads(text) if text else {}


def get_json(base_url, route):
    with urllib.request.urlopen(f"{base_url.rstrip('/')}{route}") as response:
        text = response.read().decode()
    return json.loads(text) if text else {}


def apply_required_trigger_words(workflow, prompt):
    metadata_notes = [
        n
        for n in workflow["nodes"]
        if n.get("type") == "Note" and n.get("title") == "Metadata"
    ]
    assert len(metadata_notes) == 1, "expected exactly one Metadata note"

    metadata_text = metadata_notes[0]["widgets_values"][0]
    assert "\n---\n" in metadata_text, "expected Metadata note JSON front matter separator"
    metadata = json.loads(metadata_text.split("\n---\n", 1)[0])
    assert (
        metadata.get("trigger_required") in TRIGGER_REQUIRED_VALUES
    ), "expected trigger_required to be required, optional, no, or unknown"
    assert isinstance(metadata.get("trigger_words"), list), "expected trigger_words list"

    if metadata.get("trigger_required") != "required":
        return prompt

    trigger_words = metadata["trigger_words"]
    assert trigger_words, "required trigger metadata must list trigger_words"
    prefix = ", ".join(trigger_words)
    return f"{prefix}, {prompt}"


def prompt_resolution(metadata):
    width = metadata.get("width")
    height = metadata.get("height")
    if width is None and height is None:
        return None

    assert width is not None and height is not None, "expected both width and height"
    assert (
        isinstance(width, int) and not isinstance(width, bool) and width > 0
    ), "expected positive integer width"
    assert (
        isinstance(height, int) and not isinstance(height, bool) and height > 0
    ), "expected positive integer height"
    return width, height


def set_resolution(workflow, width, height):
    width_nodes = [
        n
        for n in workflow["nodes"]
        if n.get("type") == "PrimitiveInt" and n.get("title") == "Width"
    ]
    height_nodes = [
        n
        for n in workflow["nodes"]
        if n.get("type") == "PrimitiveInt" and n.get("title") == "Height"
    ]
    if width_nodes or height_nodes:
        assert len(width_nodes) == 1, "expected exactly one Width PrimitiveInt"
        assert len(height_nodes) == 1, "expected exactly one Height PrimitiveInt"
        width_nodes[0]["widgets_values"][0] = width
        height_nodes[0]["widgets_values"][0] = height
        return

    latent_nodes = [
        n for n in workflow["nodes"] if n.get("type") in LATENT_RESOLUTION_TYPES
    ]
    if len(latent_nodes) == 1:
        latent_node = latent_nodes[0]
        latent_node["widgets_values"][0] = width
        latent_node["widgets_values"][1] = height
        return

    selector_nodes = [
        n
        for n in workflow["nodes"]
        if n.get("type") == "📐 Resolution Image Size Selector"
    ]
    if len(selector_nodes) == 1:
        selector_node = selector_nodes[0]
        selector_node["widgets_values"][0] = "Custom"
        selector_node["widgets_values"][2] = width
        selector_node["widgets_values"][3] = height
        return

    raise AssertionError("cannot determine single generation resolution source")


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


def submit_prompt(base_url, converted_prompt):
    response = post_json(
        base_url,
        "/prompt",
        {
            "prompt": converted_prompt["prompt"],
            "client_id": str(uuid.uuid4()),
            "extra_data": {
                "extra_pnginfo": {
                    "workflow": converted_prompt["workflow"],
                },
            },
        },
    )
    if response.get("node_errors"):
        raise RuntimeError(f"ComfyUI node_errors: {json.dumps(response['node_errors'])}")

    prompt_id = response.get("prompt_id")
    if not prompt_id:
        raise RuntimeError(f"ComfyUI /prompt response missing prompt_id: {response}")
    print(f"PY prompt submit ok: {prompt_id}", flush=True)
    return prompt_id


def wait_for_history(base_url, prompt_id, timeout):
    deadline = time.monotonic() + float(timeout)
    while time.monotonic() < deadline:
        history = get_json(base_url, f"/history/{prompt_id}")
        if prompt_id in history:
            return history[prompt_id]
        time.sleep(2)

    raise TimeoutError(f"timed out waiting for prompt {prompt_id}")


def collect_output_files(history_entry):
    files = []
    for output in history_entry.get("outputs", {}).values():
        for image in output.get("images", []):
            files.append("/".join(p for p in [image.get("subfolder"), image.get("filename")] if p))
        for gif in output.get("gifs", []):
            files.append("/".join(p for p in [gif.get("subfolder"), gif.get("filename")] if p))
    return files


def validate_history_success(history_entry):
    status = history_entry.get("status", {})
    if status.get("status_str") == "success" and status.get("completed") is True:
        return

    history_text = json.dumps(history_entry)
    if is_oom_output(history_text):
        raise RuntimeError("CUDA OOM error")
    raise RuntimeError(f"prompt did not complete successfully: {json.dumps(status)}")


def main():
    repo_root = Path(__file__).resolve().parents[1]

    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt")
    parser.add_argument(
        "-w",
        "--workflow",
        default="workflows/flux-2/dev/original/flux2_dev_original.json",
    )
    parser.add_argument("--base-url", default="http://127.0.0.1:8188")
    parser.add_argument("--timeout", default="3600")
    parser.add_argument("-b", "--batch", type=int)
    parser.add_argument("--seed", type=int)
    parser.add_argument("--id")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    workflow_path = Path(args.workflow)
    if not workflow_path.is_absolute():
        workflow_path = repo_root / workflow_path

    workflow = json.loads(workflow_path.read_text())

    if args.prompt is not None:
        prompt_metadata, prompt = parse_prompt_file(args.prompt)
        prompt = apply_required_trigger_words(workflow, prompt)
        resolution = prompt_resolution(prompt_metadata)
        if resolution is not None:
            set_resolution(workflow, *resolution)

        prompt_nodes = [
            n for n in workflow["nodes"] if n.get("type") == "CLIPTextEncode"
        ]
        assert prompt_nodes, "expected at least one CLIPTextEncode node"

        if len(prompt_nodes) == 1:
            prompt_node = prompt_nodes[0]
        else:
            positive_nodes = [
                n for n in prompt_nodes if "positive" in (n.get("title") or "").lower()
            ]
            assert (
                len(positive_nodes) == 1
            ), "expected exactly one positive CLIPTextEncode node"
            prompt_node = positive_nodes[0]

        text_inputs = [
            i for i in prompt_node.get("inputs", []) if i.get("name") == "text"
        ]
        assert all(
            i.get("link") is None for i in text_inputs
        ), "expected positive CLIPTextEncode text input to be unconnected"

        if prompt_node.get("widgets_values"):
            prompt_node["widgets_values"][0] = prompt
        else:
            prompt_node["widgets_values"] = [prompt]

    if args.batch is not None:
        batch_nodes = [n for n in workflow["nodes"] if n.get("type") in BATCH_INDEX]
        assert len(batch_nodes) == 1, "expected exactly one batch-size node"
        batch_node = batch_nodes[0]
        batch_node["widgets_values"][BATCH_INDEX[batch_node["type"]]] = args.batch

    seed_nodes = [n for n in workflow["nodes"] if n.get("type") in SEED_INDEX]
    assert seed_nodes, "expected at least one seed node"

    if args.seed is not None:
        for seed_node in seed_nodes:
            seed_node["widgets_values"][SEED_INDEX[seed_node["type"]]] = args.seed

    save_nodes = [n for n in workflow["nodes"] if n.get("type") == "SaveImage"]
    assert len(save_nodes) == 1, "expected exactly one SaveImage node"

    if args.id is not None:
        save_nodes[0]["widgets_values"][0] = f"{args.id}_{workflow_path.stem}"

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_workflow = Path(tmpdir) / "workflow.json"
        tmp_prompt = Path(tmpdir) / "prompt.json"
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
            f"{tmpdir}:/input",
            "-w",
            "/tmp",
            "mcr.microsoft.com/playwright:v1.57.0-noble",
            "sh",
            "-lc",
            "npm init -y >/dev/null && "
            "PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 "
            "npm install playwright@1.57.0 >/dev/null && "
            "cp /work/scripts/gui_workflow_convert.mjs . && "
            'node gui_workflow_convert.mjs --base-url "$1" '
            '--timeout "$2" --output /input/prompt.json /input/workflow.json',
            "sh",
            args.base_url,
            args.timeout,
        ]

        run_workflow(cmd)
        if args.dry_run:
            return

        converted_prompt = json.loads(tmp_prompt.read_text())
        try:
            free_memory(args.base_url)
            max_attempts = 3
            for attempt in range(max_attempts):
                submitted = False
                try:
                    prompt_id = submit_prompt(args.base_url, converted_prompt)
                    submitted = True
                    history = wait_for_history(args.base_url, prompt_id, args.timeout)
                    validate_history_success(history)
                    files = collect_output_files(history)
                    print(
                        f"PY prompt history ok: {', '.join(files) if files else 'no saved outputs'}",
                        flush=True,
                    )
                    break
                except TimeoutError:
                    raise
                except RuntimeError as exc:
                    if str(exc) != "CUDA OOM error":
                        raise
                    if attempt == max_attempts - 1:
                        print("CUDA OOM error", flush=True)
                        raise SystemExit(1)
                    print("CUDA OOM error; retrying", flush=True)
                    time.sleep(2)
                except Exception:
                    if submitted:
                        raise
                    if attempt == max_attempts - 1:
                        raise
                    print("workflow failed; retrying", flush=True)
                    time.sleep(2)
        finally:
            free_memory(args.base_url)


if __name__ == "__main__":
    main()
