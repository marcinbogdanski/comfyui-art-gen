#!/usr/bin/env python3
import json
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/data/comfyui/models")
weight_exts = {".safetensor", ".safetensors", ".pth", ".gguf"}
source_exts = {".png", ".jpeg", ".jpg", ".json", ".txt"}
image_exts = {".png", ".jpeg", ".jpg"}
ignored_dirs = {"LLM", "clip", "controlnet", "text_encoders", "vae", "upscale_models"}


def check_image(path):
    data = path.read_bytes()
    ext = path.suffix.lower()
    kind = ".png" if data.startswith(b"\x89PNG\r\n\x1a\n") else ".jpg" if data.startswith(b"\xff\xd8\xff") else ""
    text = data.decode("latin1", "ignore")
    problems = []

    if ext == ".png" and kind != ".png":
        problems.append("image extension is not png")
    if ext in {".jpg", ".jpeg"} and kind != ".jpg":
        problems.append("image extension is not jpg/jpeg")

    has_comfy = "workflow\x00" in text or ('"last_node_id"' in text and '"nodes"' in text)
    has_a1111 = "Steps:" in text and "Sampler:" in text and "Seed:" in text
    if not has_comfy and not has_a1111:
        problems.append("image missing ComfyUI workflow or A1111 parameters")

    return problems


def check_md(path):
    text = path.read_text().strip()
    marker = "```json model_summary\n"
    if not text.startswith(marker):
        return {}, ["missing model_summary json block"]

    end = text.find("\n```", len(marker))
    if end == -1:
        return {}, ["missing model_summary json block"]

    problems = []
    try:
        data = json.loads(text[len(marker):end])
    except json.JSONDecodeError as e:
        return {}, [f"invalid model_summary json: {e.msg}"]

    if not isinstance(data, dict):
        return {}, ["model_summary json is not an object"]
    if not isinstance(data.get("source"), str) or not data["source"].strip():
        problems.append("missing source")
    if "html" in data and not isinstance(data["html"], str):
        problems.append("html must be a filename string")
    if not isinstance(data.get("workflows"), list) or not data["workflows"]:
        problems.append("missing workflows")
    elif not all(isinstance(workflow, str) and workflow for workflow in data["workflows"]):
        problems.append("workflows must be filename strings")

    return data, problems


def same_folder(path, filename):
    return not Path(filename).is_absolute() and Path(filename).name == filename

files = [
    path
    for path in sorted(root.rglob("*"))
    if path.is_file() and not any("Hunyuan" in part for part in path.parts)
    and not any(part.startswith(".") for part in path.relative_to(root).parts)
    and path.relative_to(root).parts[0] not in ignored_dirs
    and path.relative_to(root) != Path("README.md")
]
recognized = set()
problems = []

for weight in [path for path in files if path.suffix.lower() in weight_exts]:
    recognized.add(weight)
    md = weight.with_suffix(".md")
    if md not in files:
        problems.append((weight, "missing .md"))
        continue

    recognized.add(md)
    data, md_problems = check_md(md)
    for problem in md_problems:
        problems.append((md, problem))
    if md_problems:
        continue

    source = data["source"]
    is_redirect = source.endswith(".md")

    if source.endswith(".md"):
        if not same_folder(md, source) or not (md.parent / source).exists():
            problems.append((weight, "redirect target missing"))

    html = data.get("html", "")
    if not is_redirect and not html:
        problems.append((weight, "missing .html"))
    if html:
        if not same_folder(md, html):
            problems.append((md, "html must be a same-folder filename"))
        elif not (md.parent / html).exists():
            problems.append((weight, "missing .html"))
        else:
            recognized.add(md.parent / html)

    for workflow in data["workflows"]:
        if workflow == "not_available":
            continue
        if not same_folder(md, workflow):
            problems.append((md, "workflow must be a same-folder filename"))
            continue

        path = md.parent / workflow
        if not path.exists():
            problems.append((weight, f"missing workflow {workflow}"))
            continue
        recognized.add(path)

        if path.suffix.lower() not in source_exts:
            problems.append((path, "workflow must be .png/.jpeg/.jpg/.json/.txt"))
        if path.suffix.lower() in image_exts:
            for problem in check_image(path):
                problems.append((path, problem))

if problems:
    print("Rule check failures:")
    for weight, problem in problems:
        print(f"- {weight.relative_to(root)}: {problem}")

untracked = [path for path in files if path not in recognized]
if untracked:
    print("\nUntracked files:")
    for path in untracked:
        print(f"- {path.relative_to(root)}")

if not problems and not untracked:
    print("ok")

sys.exit(1 if problems or untracked else 0)
