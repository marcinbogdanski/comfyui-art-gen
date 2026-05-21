#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"

mkdir -p "${MODELS_DIR}/diffusion_models"
mkdir -p "${MODELS_DIR}/text_encoders"
mkdir -p "${MODELS_DIR}/vae"

wget -c -O "${MODELS_DIR}/diffusion_models/bigLove_klein2_bf16_pruned.safetensors" \
  "https://huggingface.co/Granddyser/biglove-klein2/resolve/main/bigLove_klein2_bf16_pruned.safetensors"

wget -c -O "${MODELS_DIR}/text_encoders/qwen_3_8b_fp8mixed.safetensors" \
  "https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-9b/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors?download=true"

wget -c -O "${MODELS_DIR}/vae/flux2-vae.safetensors" \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors?download=true"
