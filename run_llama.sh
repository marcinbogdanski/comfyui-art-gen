#!/usr/bin/env bash
set -euo pipefail

IMAGE="${LLAMA_IMAGE:-ghcr.io/ggml-org/llama.cpp:server-cuda}"
DATA_DIR="${LLAMA_DATA_DIR:-/mnt/data/llm}"
CACHE_DIR="${LLAMA_CACHE_DIR:-${DATA_DIR}/cache}"
GPU_DEVICE="${LLAMA_GPU_DEVICE:-1}"
HOST_PORT="${LLAMA_HOST_PORT:-8081}"
CONTAINER_PORT="${LLAMA_CONTAINER_PORT:-8080}"
MODEL="${LLAMA_MODEL:-HauhauCS/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive:Q4_K_M}"
CTX_SIZE="${LLAMA_CTX_SIZE:-16384}"
GPU_LAYERS="${LLAMA_GPU_LAYERS:-99}"

LLAMA_ARGS=(
  -hf "${MODEL}"
  --host 0.0.0.0
  --port "${CONTAINER_PORT}"
  --jinja
  --ctx-size "${CTX_SIZE}"
  -ngl "${GPU_LAYERS}"
)

mkdir -p "${CACHE_DIR}"

if [[ ! -w "${CACHE_DIR}" ]]; then
  echo "Directory is not writable: ${CACHE_DIR}" >&2
  echo "Fix ownership before running, for example: sudo chown -R $(id -u):$(id -g) ${DATA_DIR}" >&2
  exit 1
fi

exec docker run --rm -it \
  --gpus "device=${GPU_DEVICE}" \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  -v "${CACHE_DIR}:/models/cache" \
  -e LLAMA_CACHE=/models/cache \
  "${IMAGE}" \
  "${LLAMA_ARGS[@]}" \
  "$@"
