# ComfyUI Server

Minimal Docker-based ComfyUI server for this headless GPU box.

## Build

```bash
docker build -t local/comfyui:cu130 .
```

## Run

```bash
./run_comfyui.sh
```

Data is stored under `/mnt/data/comfyui`.
The wrapper starts a detached container named `comfyui` on watercooled GPU 1.

## Access

```text
http://x399.lan:8188/
```

The wrapper sets `PYTORCH_CUDA_ALLOC_CONF` to
`expandable_segments:True` to reduce CUDA allocator fragmentation on large
ComfyUI workflows and starts ComfyUI with `--disable-cuda-malloc` so PyTorch's
allocator controls CUDA allocations.
