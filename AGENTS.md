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
