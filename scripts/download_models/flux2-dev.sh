#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"

mkdir -p "${MODELS_DIR}/text_encoders"
mkdir -p "${MODELS_DIR}/diffusion_models"
mkdir -p "${MODELS_DIR}/vae"

wget -c -O "${MODELS_DIR}/text_encoders/mistral_3_small_flux2_fp8.safetensors" \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/text_encoders/mistral_3_small_flux2_fp8.safetensors"

wget -c -O "${MODELS_DIR}/diffusion_models/flux2_dev_fp8mixed.safetensors" \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/diffusion_models/flux2_dev_fp8mixed.safetensors"

wget -c -O "${MODELS_DIR}/vae/flux2-vae.safetensors" \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors"
