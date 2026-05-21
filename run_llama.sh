#!/usr/bin/env bash
set -euo pipefail

mkdir -p /mnt/data/llm/cache

exec docker run -d --rm \
  --name llama \
  --gpus device=3 \
  -p 8081:8080 \
  -v /mnt/data/llm/cache:/models/cache \
  -e LLAMA_CACHE=/models/cache \
  ghcr.io/ggml-org/llama.cpp:server-cuda \
  -hf HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive:Q4_K_M \
  --host 0.0.0.0 \
  --port 8080 \
  --jinja \
  --ctx-size 16384 \
  -ngl 99 \
  "$@"
