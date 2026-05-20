#!/usr/bin/env bash
set -euo pipefail

mkdir -p /mnt/data/comfyui/{models,input,output,custom_nodes,user}

exec docker run -d --rm \
  --name comfyui \
  --gpus device=1 \
  -p 8188:8188 \
  -e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  -v /mnt/data/comfyui/models:/opt/ComfyUI/models \
  -v /mnt/data/comfyui/input:/opt/ComfyUI/input \
  -v /mnt/data/comfyui/output:/opt/ComfyUI/output \
  -v /mnt/data/comfyui/custom_nodes:/opt/ComfyUI/custom_nodes \
  -v /mnt/data/comfyui/user:/opt/ComfyUI/user \
  local/comfyui:cu130 \
  --listen 0.0.0.0 \
  --port 8188 \
  --enable-manager \
  --disable-api-nodes \
  --disable-cuda-malloc \
  "$@"
