#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/data/comfyui/models")
weight_exts = {".safetensor", ".safetensors", ".pth", ".gguf"}
sidecar_exts = {".md", ".html", ".png", ".jpeg", ".jpg", ".json", ".txt"}
source_exts = {".png", ".jpeg", ".jpg", ".json", ".txt"}

files = [
    path
    for path in sorted(root.rglob("*"))
    if path.is_file() and not any("Hunyuan" in part for part in path.parts)
]
recognized = set()
problems = []

for weight in [path for path in files if path.suffix.lower() in weight_exts]:
    recognized.add(weight)
    sidecars = [
        path
        for path in files
        if path.parent == weight.parent
        and path.stem == weight.stem
        and path.suffix.lower() in sidecar_exts
    ]
    recognized.update(sidecars)

    md = weight.with_suffix(".md")
    if md not in sidecars:
        problems.append((weight, "missing .md"))

    is_redirect = False
    if md in sidecars:
        text = md.read_text().strip()
        is_redirect = text.lower().startswith("see ")
        if is_redirect:
            target = text.split("`", 2)[1] if "`" in text else ""
            if not target or not (md.parent / target).exists():
                problems.append((weight, "redirect target missing"))

    if not is_redirect and not any(path.suffix.lower() in source_exts for path in sidecars):
        problems.append((weight, "missing source/reference .png/.jpeg/.jpg/.json/.txt"))

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
