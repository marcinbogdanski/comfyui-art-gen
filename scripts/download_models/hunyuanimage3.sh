#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"

mkdir -p "${MODELS_DIR}"

hf download EricRollei/HunyuanImage-3-NF4-v2 \
  --local-dir "${MODELS_DIR}/HunyuanImage-3-NF4-v2"

hf download EricRollei/HunyuanImage-3-INT8-v2 \
  --local-dir "${MODELS_DIR}/HunyuanImage-3-INT8-v2"

hf download EricRollei/HunyuanImage-3.0-Instruct-Distil-NF4-v2 \
  --local-dir "${MODELS_DIR}/HunyuanImage-3.0-Instruct-Distil-NF4-v2"

hf download EricRollei/HunyuanImage-3.0-Instruct-Distil-INT8-v2 \
  --local-dir "${MODELS_DIR}/HunyuanImage-3.0-Instruct-Distil-INT8-v2"
