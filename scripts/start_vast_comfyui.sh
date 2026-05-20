#!/usr/bin/env bash
set -euo pipefail

COMFYUI_PATH="${COMFYUI_PATH:-/workspace/ComfyUI}"
COMFYUI_HOST="${COMFYUI_HOST:-127.0.0.1}"
COMFYUI_PORT="${COMFYUI_PORT:-8188}"
LOG_FILE="${COMFYUI_LOG_FILE:-/workspace/comfyui.log}"
PID_FILE="${COMFYUI_PID_FILE:-/workspace/comfyui.pid}"

export PYTORCH_CUDA_ALLOC_CONF="${PYTORCH_CUDA_ALLOC_CONF:-expandable_segments:True}"

if [[ -f "${PID_FILE}" ]] && kill -0 "$(cat "${PID_FILE}")" 2>/dev/null; then
  echo "ComfyUI is already running: $(cat "${PID_FILE}")"
  exit 0
fi

cd "${COMFYUI_PATH}"
nohup python main.py \
  --listen "${COMFYUI_HOST}" \
  --port "${COMFYUI_PORT}" \
  --enable-manager \
  --disable-api-nodes \
  "$@" \
  > "${LOG_FILE}" 2>&1 &

echo "$!" > "${PID_FILE}"
echo "Started ComfyUI pid $(cat "${PID_FILE}") on ${COMFYUI_HOST}:${COMFYUI_PORT}"
echo "PYTORCH_CUDA_ALLOC_CONF=${PYTORCH_CUDA_ALLOC_CONF}"
