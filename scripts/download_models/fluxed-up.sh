#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"

mkdir -p "${MODELS_DIR}/checkpoints"
mkdir -p "${MODELS_DIR}/clip"
mkdir -p "${MODELS_DIR}/vae/Flux"

curl -fL -C - -H "Authorization: Bearer ${CIVITAI_API_KEY}" \
  -o "${MODELS_DIR}/checkpoints/fluxedUpFluxNSFW_100BF16.safetensors" \
  "https://civitai.red/api/download/models/2892326"

wget -c -O "${MODELS_DIR}/clip/clip_l.safetensors" \
  "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors"

wget -c -O "${MODELS_DIR}/clip/t5xxl_fp16.safetensors" \
  "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors"

wget -c -O "${MODELS_DIR}/clip/clip_g.safetensors" \
  "https://huggingface.co/Comfy-Org/stable-diffusion-3.5-fp8/resolve/main/text_encoders/clip_g.safetensors"

wget -c -O "${MODELS_DIR}/vae/Flux/flux_vae.safetensors" \
  "https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors"
ln -sf Flux/flux_vae.safetensors "${MODELS_DIR}/vae/flux_vae.safetensors"
