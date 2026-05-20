#!/usr/bin/env bash
set -euo pipefail

IMAGE="${COMFYUI_IMAGE:-local/comfyui:cu130}"
DATA_DIR="${COMFYUI_DATA_DIR:-/mnt/data/comfyui}"
GPU_DEVICE="${COMFYUI_GPU_DEVICE:-0}"
HOST_PORT="${COMFYUI_HOST_PORT:-8188}"
CONTAINER_PORT="${COMFYUI_CONTAINER_PORT:-8188}"
DETACH="${COMFYUI_DETACH:-0}"
CONTAINER_NAME="${COMFYUI_CONTAINER_NAME:-comfyui}"
PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"
COMFYUI_ARGS=(
  --listen 0.0.0.0
  --port "${CONTAINER_PORT}"
  --enable-manager
)

for dir in models input output custom_nodes user; do
  mkdir -p "${DATA_DIR}/${dir}"

  if [[ ! -w "${DATA_DIR}/${dir}" ]]; then
    echo "Directory is not writable: ${DATA_DIR}/${dir}" >&2
    echo "Fix ownership before running, for example: sudo chown -R $(id -u):$(id -g) ${DATA_DIR}" >&2
    exit 1
  fi
done

DOCKER_ARGS=(--rm)

if [[ "${DETACH}" == "1" ]]; then
  DOCKER_ARGS+=(-d --name "${CONTAINER_NAME}")
else
  DOCKER_ARGS+=(-it)
fi

exec docker run "${DOCKER_ARGS[@]}" \
  --gpus "device=${GPU_DEVICE}" \
  -p "${HOST_PORT}:${CONTAINER_PORT}" \
  -e "PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF}" \
  -v "${DATA_DIR}/models:/opt/ComfyUI/models" \
  -v "${DATA_DIR}/input:/opt/ComfyUI/input" \
  -v "${DATA_DIR}/output:/opt/ComfyUI/output" \
  -v "${DATA_DIR}/custom_nodes:/opt/ComfyUI/custom_nodes" \
  -v "${DATA_DIR}/user:/opt/ComfyUI/user" \
  "${IMAGE}" \
  "${COMFYUI_ARGS[@]}" \
  "$@"
