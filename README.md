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
