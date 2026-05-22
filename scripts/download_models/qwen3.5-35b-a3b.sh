#!/usr/bin/env bash
set -euo pipefail

MODELS_DIR="${COMFYUI_MODELS_DIR:-${COMFYUI_PATH:-/workspace/ComfyUI}/models}"
QWEN35_MODEL_DIR="${MODELS_DIR}/LLM/GGUF/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive"

mkdir -p "${QWEN35_MODEL_DIR}"

wget -c -O "${QWEN35_MODEL_DIR}/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf" \
  "https://huggingface.co/HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/resolve/main/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"

wget -c -O "${QWEN35_MODEL_DIR}/mmproj-Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf" \
  "https://huggingface.co/HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/resolve/main/mmproj-Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf"
