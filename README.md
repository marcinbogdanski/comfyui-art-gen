# ComfyUI Server

Minimal Docker-based ComfyUI server for this headless GPU box.

## Build

```bash
docker build -t local/comfyui:cu130 .
```

## Run

```bash
./run_comfyui.sh --disable-api-nodes
```

Data is stored under `/mnt/data/comfyui`.

## Access

```text
http://x399.lan:8188/
```

Useful overrides:

```bash
COMFYUI_GPU_DEVICE=1 COMFYUI_HOST_PORT=8189 ./run_comfyui.sh
```

The wrapper defaults `PYTORCH_CUDA_ALLOC_CONF` to
`expandable_segments:True` to reduce CUDA allocator fragmentation on large
ComfyUI workflows. Set `PYTORCH_CUDA_ALLOC_CONF` explicitly before launching to
override it for debugging.

Use `--disable-cuda-malloc` when relying on this setting; it disables ComfyUI's
allocator so PyTorch's allocator, and therefore `PYTORCH_CUDA_ALLOC_CONF`,
controls CUDA allocations.
