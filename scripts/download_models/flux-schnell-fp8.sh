#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/ComfyUI/models/checkpoints

wget -c -O /workspace/ComfyUI/models/checkpoints/flux1-schnell-fp8.safetensors \
  "https://huggingface.co/Comfy-Org/flux1-schnell/resolve/main/flux1-schnell-fp8.safetensors"
