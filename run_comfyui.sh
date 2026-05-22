#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p /mnt/data/comfyui/{models,input,output,custom_nodes,user}
mkdir -p "$SCRIPT_DIR/workflows"

exec docker run -d \
  --name comfyui \
  --gpus device=1 \
  -p 8188:8188 \
  -e PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
  -v /mnt/data/comfyui/models:/opt/ComfyUI/models \
  -v /mnt/data/comfyui/input:/opt/ComfyUI/input \
  -v /mnt/data/comfyui/output:/opt/ComfyUI/output \
  -v /mnt/data/comfyui/custom_nodes:/opt/ComfyUI/custom_nodes \
  -v /mnt/data/comfyui/user:/opt/ComfyUI/user \
  -v "$SCRIPT_DIR/workflows:/opt/ComfyUI/user/default/workflows" \
  local/comfyui:cu130 \
  --listen 0.0.0.0 \
  --port 8188 \
  --enable-manager \
  --disable-api-nodes \
  --disable-cuda-malloc \
  "$@"
