#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"
REVISION="952f49d49653cb42e7d6cf7cbfad74738073ec7d"
BASE_URL="https://huggingface.co/Comfy-Org/Krea-2/resolve/${REVISION}"

mkdir -p "${MODELS_DIR}/diffusion_models"
mkdir -p "${MODELS_DIR}/text_encoders"
mkdir -p "${MODELS_DIR}/vae"

download() {
  local relative_path=$1
  local sha256=$2
  local target="${MODELS_DIR}/${relative_path}"

  wget -c -O "${target}" "${BASE_URL}/${relative_path}"
  printf '%s  %s\n' "${sha256}" "${target}" | sha256sum -c -
}

download \
  "diffusion_models/krea2_raw_int8_convrot.safetensors" \
  "5585a4a38c4bcfb6fde2d480a4aa6edf7f665721ebde56d30662c35a45f5fa5c"
download \
  "diffusion_models/krea2_turbo_int8_convrot.safetensors" \
  "8e4eeda70dd5037ab1ba2bef6b417f9f901e26093117cf397f741fc1fdaaf3f1"
download \
  "text_encoders/qwen3vl_4b_fp8_scaled.safetensors" \
  "54bd5144df0bbc25dd6ccadfcb826b521445a1b06ae5a42570bdd2974ca87094"
download \
  "vae/qwen_image_vae.safetensors" \
  "a70580f0213e67967ee9c95f05bb400e8fb08307e017a924bf3441223e023d1f"
