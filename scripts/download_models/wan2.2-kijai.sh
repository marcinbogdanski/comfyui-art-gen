#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/ComfyUI/models/diffusion_models/WanVideo/2_2
mkdir -p /workspace/ComfyUI/models/loras/WanVideo/Lightx2v
mkdir -p /workspace/ComfyUI/models/text_encoders
mkdir -p /workspace/ComfyUI/models/vae/wanvideo

wget -c -O /workspace/ComfyUI/models/diffusion_models/WanVideo/2_2/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors \
  "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/I2V/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors"

wget -c -O /workspace/ComfyUI/models/diffusion_models/WanVideo/2_2/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors \
  "https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/I2V/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors"

wget -c -O /workspace/ComfyUI/models/loras/WanVideo/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors \
  "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors"

wget -c -O /workspace/ComfyUI/models/text_encoders/umt5-xxl-enc-bf16.safetensors \
  "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-bf16.safetensors"

wget -c -O /workspace/ComfyUI/models/vae/wanvideo/Wan2_1_VAE_bf16.safetensors \
  "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors"
