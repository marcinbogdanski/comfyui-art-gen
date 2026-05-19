#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/ComfyUI/models/LLM/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive

wget -c -O /workspace/ComfyUI/models/LLM/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf \
  "https://huggingface.co/HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/resolve/main/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf"

wget -c -O /workspace/ComfyUI/models/LLM/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/mmproj-Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf \
  "https://huggingface.co/HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/resolve/main/mmproj-Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf"
