#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"

mkdir -p "${MODELS_DIR}/checkpoints"
mkdir -p "${MODELS_DIR}/upscale_models"

curl -fL -C - -H "Authorization: Bearer ${CIVITAI_API_KEY}" \
  -o "${MODELS_DIR}/checkpoints/cyberrealisticPony_v180Coreshift.safetensors" \
  "https://civitai.com/api/download/models/2884631?type=Model&format=SafeTensor&size=pruned&fp=fp16"

wget -c -O "${MODELS_DIR}/upscale_models/4x_NickelbackFS_72000_G.pth" \
  "https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_NickelbackFS_72000_G.pth"
