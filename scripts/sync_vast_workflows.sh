#!/usr/bin/env bash
set -euo pipefail

COMFYUI_PATH="${COMFYUI_PATH:-/workspace/ComfyUI}"
SOURCE_DIR="${WORKFLOW_SOURCE_DIR:-/workspace/art-gen-ctrl/workflows}"
TARGET_DIR="${WORKFLOW_TARGET_DIR:-${COMFYUI_PATH}/user/default/workflows}"

if [[ ! -d "${SOURCE_DIR}" ]]; then
  echo "Workflow source directory does not exist: ${SOURCE_DIR}" >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"
rsync -a --delete "${SOURCE_DIR}/" "${TARGET_DIR}/"

while IFS= read -r -d '' workflow; do
  cp "${workflow}" "${workflow%.json}.work.json"
done < <(
  find "${TARGET_DIR}" \
    -type f \
    -name '*.json' \
    ! -name '*.api.json' \
    ! -name '*.work.json' \
    -print0
)

find "${TARGET_DIR}" -maxdepth 3 -type f | sort
