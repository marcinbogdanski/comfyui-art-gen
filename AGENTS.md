# Agent Notes

This repo manages a Docker-based ComfyUI server for host `x399`.

Operational preferences:

- Use manual `docker run --rm -it` via `./run_comfyui.sh`; do not introduce Docker Compose unless requested.
- Do not install CUDA Toolkit, PyTorch, ComfyUI, or model dependencies on the host.
- Persistent ComfyUI data lives under `/mnt/data/comfyui`.
- Keep model files out of git; document model download commands instead.
- Default access URL is `http://x399.lan:8188/`.
- Start with one GPU per ComfyUI instance; default wrapper uses GPU 0.
- Do not expose ComfyUI directly to the public internet.

Image setup:

- Base image is the official PyTorch CUDA runtime image.
- Switch from `runtime` to `devel` only if custom nodes need native/CUDA compilation.

## Memory files

- If present, read recent `memory/YYYY-MM-DD.md` entries for session continuity.
- Use the human/logical day, not strict midnight, when naming entries; if work happens after midnight but before Marcin sleeps, use the previous calendar date.
- Write significant progress to `memory/YYYY-MM-DD.md` when useful; multiple entries per day are fine.
- Prefer appending new sections to the end of an existing memory file, unless cleanup or structure clearly requires insertion elsewhere.
- Use memory files for worklog notes, setup lessons, repo/process decisions, and next-session handover.

## Tools

### GitHub CLI

- The `gh` CLI is available and pre-authenticated for agent access.
- GitHub permissions are scoped to selected repositories.
- Do not force-push or delete the main branch.

