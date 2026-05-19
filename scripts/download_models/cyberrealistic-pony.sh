#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/ComfyUI/models/checkpoints
mkdir -p /workspace/ComfyUI/models/upscale_models

curl -fL -C - -H "Authorization: Bearer ${CIVITAI_API_KEY}" \
  -o /workspace/ComfyUI/models/checkpoints/cyberrealisticPony_v180Coreshift.safetensors \
  "https://civitai.com/api/download/models/2884631?type=Model&format=SafeTensor&size=pruned&fp=fp16"

wget -c -O /workspace/ComfyUI/models/upscale_models/4x_NickelbackFS_72000_G.pth \
  "https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_NickelbackFS_72000_G.pth"
