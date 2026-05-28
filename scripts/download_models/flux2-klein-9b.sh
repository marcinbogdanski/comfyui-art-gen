#!/usr/bin/env bash
set -euo pipefail

: "${HF_TOKEN:?HF_TOKEN is required for gated BFL FLUX.2 Klein 9B downloads}"

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"

mkdir -p "${MODELS_DIR}/diffusion_models"
mkdir -p "${MODELS_DIR}/text_encoders"
mkdir -p "${MODELS_DIR}/vae"

wget -c --header="Authorization: Bearer ${HF_TOKEN}" \
  -O "${MODELS_DIR}/diffusion_models/flux-2-klein-base-9b-fp8.safetensors" \
  "https://huggingface.co/black-forest-labs/FLUX.2-klein-base-9b-fp8/resolve/main/flux-2-klein-base-9b-fp8.safetensors"

wget -c --header="Authorization: Bearer ${HF_TOKEN}" \
  -O "${MODELS_DIR}/diffusion_models/flux-2-klein-9b-fp8.safetensors" \
  "https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/resolve/main/flux-2-klein-9b-fp8.safetensors"

wget -c \
  -O "${MODELS_DIR}/text_encoders/qwen_3_8b_fp8mixed.safetensors" \
  "https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors"

wget -c --header="Authorization: Bearer ${HF_TOKEN}" \
  -O "${MODELS_DIR}/vae/full_encoder_small_decoder.safetensors" \
  "https://huggingface.co/black-forest-labs/FLUX.2-small-decoder/resolve/main/full_encoder_small_decoder.safetensors"

wget -c \
  -O "${MODELS_DIR}/vae/flux2-vae.safetensors" \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors"
