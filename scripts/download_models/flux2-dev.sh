#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/ComfyUI/models/text_encoders
mkdir -p /workspace/ComfyUI/models/diffusion_models
mkdir -p /workspace/ComfyUI/models/vae

wget -c -O /workspace/ComfyUI/models/text_encoders/mistral_3_small_flux2_fp8.safetensors \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/text_encoders/mistral_3_small_flux2_fp8.safetensors"

wget -c -O /workspace/ComfyUI/models/diffusion_models/flux2_dev_fp8mixed.safetensors \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/diffusion_models/flux2_dev_fp8mixed.safetensors"

wget -c -O /workspace/ComfyUI/models/vae/flux2-vae.safetensors \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors"
