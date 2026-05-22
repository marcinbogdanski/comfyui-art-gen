#!/usr/bin/env python3
from pathlib import Path
import sys

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/mnt/data/comfyui/models")
weight_exts = {".safetensor", ".safetensors", ".pth", ".gguf"}
sidecar_exts = {".md", ".html", ".png", ".jpeg", ".jpg", ".json", ".txt"}
source_exts = {".png", ".jpeg", ".jpg", ".json", ".txt"}
image_exts = {".png", ".jpeg", ".jpg"}


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
    if not text.startswith("---\n"):
        return "", text, ["missing source front matter"]
    parts = text.split("---", 2)
    if len(parts) < 3:
        return "", text, ["missing source front matter"]
    _, front_matter, body = parts
    source = [line for line in front_matter.splitlines() if line.strip().startswith("source: ")]
    source = source[0].split(":", 1)[1].strip() if source else ""
    return source, body.strip(), [] if source else ["missing source front matter"]

files = [
    path
    for path in sorted(root.rglob("*"))
    if path.is_file() and not any("Hunyuan" in part for part in path.parts)
    and not any(part.startswith(".") for part in path.relative_to(root).parts)
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
    html = weight.with_suffix(".html")
    if md not in sidecars:
        problems.append((weight, "missing .md"))

    is_redirect = False
    if md in sidecars:
        source, text, md_problems = check_md(md)
        for problem in md_problems:
            problems.append((md, problem))
        is_redirect = source.endswith(".md") or text.lower().startswith("see ")
        if source.endswith(".md"):
            if not (md.parent / source).exists():
                problems.append((weight, "redirect target missing"))
        elif is_redirect:
            target = text.split("`", 2)[1] if "`" in text else ""
            if not target or not (md.parent / target).exists():
                problems.append((weight, "redirect target missing"))

    if not is_redirect and not any(path.suffix.lower() in source_exts for path in sidecars):
        problems.append((weight, "missing source/reference .png/.jpeg/.jpg/.json/.txt"))
    if not is_redirect and html not in sidecars:
        problems.append((weight, "missing .html"))

    for image in [path for path in sidecars if path.suffix.lower() in image_exts]:
        for problem in check_image(image):
            problems.append((image, problem))

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
