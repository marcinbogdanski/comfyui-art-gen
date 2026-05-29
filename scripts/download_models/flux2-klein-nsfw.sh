#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"

if [[ -z "${CIVITAI_API_KEY:-}" ]]; then
  echo "CIVITAI_API_KEY is required for these Civitai downloads." >&2
  exit 1
fi

mkdir -p "${MODELS_DIR}/diffusion_models"
mkdir -p "${MODELS_DIR}/loras"
mkdir -p "${MODELS_DIR}/text_encoders"

download_civitai() {
  local url="$1"
  local dest="$2"

  curl -fL -C - --retry 5 --retry-delay 5 \
    -H "Authorization: Bearer ${CIVITAI_API_KEY}" \
    -o "${dest}" \
    "${url}"
}

download_civitai \
  "https://civitai.com/api/download/models/2669986?type=Model&format=SafeTensor&size=pruned&fp=fp8" \
  "${MODELS_DIR}/diffusion_models/darkBeast_dbkBlitzV15.safetensors"

download_civitai \
  "https://civitai.com/api/download/models/2985440" \
  "${MODELS_DIR}/diffusion_models/snofsSexNudesAndOtherFunStuff_v14Distilled.safetensors"

download_civitai \
  "https://civitai.com/api/download/models/2944415" \
  "${MODELS_DIR}/diffusion_models/pornmasterFlux2Klein_v4.safetensors"

download_civitai \
  "https://civitai.com/api/download/models/2960556" \
  "${MODELS_DIR}/loras/klein_snofs_v1_4.safetensors"

download_civitai \
  "https://civitai.com/api/download/models/2753532" \
  "${MODELS_DIR}/loras/KLEIN-Unchained-V2.safetensors"

curl -fL -C - --retry 5 --retry-delay 5 \
  -o "${MODELS_DIR}/loras/klein_9B_Turbo_r128.safetensors" \
  "https://huggingface.co/ShadoWxShinigamI/Flux-Klein-Turbo-Lora/resolve/main/klein_9B_Turbo_r128.safetensors"

curl -fL -C - --retry 5 --retry-delay 5 \
  -o "${MODELS_DIR}/text_encoders/qwen_3_8b.safetensors" \
  "https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b.safetensors"
