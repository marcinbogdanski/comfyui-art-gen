#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/ComfyUI/models/checkpoints
mkdir -p /workspace/ComfyUI/models/clip
mkdir -p /workspace/ComfyUI/models/vae

curl -fL -C - -H "Authorization: Bearer ${CIVITAI_API_KEY}" \
  -o /workspace/ComfyUI/models/checkpoints/fluxedUpFluxNSFW_100BF16.safetensors \
  "https://civitai.red/api/download/models/2892326"

wget -c -O /workspace/ComfyUI/models/clip/clip_l.safetensors \
  "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"

wget -c -O /workspace/ComfyUI/models/clip/t5xxl_fp16.safetensors \
  "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors"

wget -c -O /workspace/ComfyUI/models/clip/clip_g.safetensors \
  "https://huggingface.co/Comfy-Org/stable-diffusion-3.5-fp8/resolve/main/text_encoders/clip_g.safetensors"

wget -c -O /workspace/ComfyUI/models/vae/ae.safetensors \
  "https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors"

ln -sf ae.safetensors /workspace/ComfyUI/models/vae/flux_vae.safetensors
