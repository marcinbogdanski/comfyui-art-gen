#!/usr/bin/env bash
set -euo pipefail

COMFYUI_PATH="${COMFYUI_PATH:-/workspace/ComfyUI}"
NODE_DIR="${COMFYUI_PATH}/custom_nodes/Comfy_HunyuanImage3"
NODE_FILE="${NODE_DIR}/hunyuan_instruct_nodes.py"
EXPECTED_HUNYUAN_REF="${EXPECTED_HUNYUAN_REF:-bf738dba3f542e6744c49bc29c29a20dd14d079d}"

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
PATCH_FILE="${PATCH_FILE:-${REPO_ROOT}/patches/Comfy_HunyuanImage3/lowvram-multifusion-cond-vae.patch}"
MARKER="Low-VRAM controls for 24-32GB GPUs (repo patch marker)."

if [[ ! -f "${NODE_FILE}" ]]; then
  echo "Missing Hunyuan node file: ${NODE_FILE}" >&2
  exit 1
fi

if [[ ! -f "${PATCH_FILE}" ]]; then
  echo "Missing patch file: ${PATCH_FILE}" >&2
  exit 1
fi

if [[ -d "${NODE_DIR}/.git" ]]; then
  current_ref="$(git -C "${NODE_DIR}" rev-parse HEAD)"
  if [[ "${current_ref}" != "${EXPECTED_HUNYUAN_REF}" ]]; then
    echo "Warning: patch was built for Comfy_HunyuanImage3 ${EXPECTED_HUNYUAN_REF}, current ref is ${current_ref}" >&2
  fi
fi

if grep -qF "${MARKER}" "${NODE_FILE}"; then
  echo "Hunyuan low-VRAM patch already applied: ${NODE_FILE}"
else
  git -C "${NODE_DIR}" apply "${PATCH_FILE}"
  echo "Applied Hunyuan low-VRAM patch: ${PATCH_FILE}"
fi

PYTHON_BIN="${PYTHON_BIN:-python}"
if ! command -v "${PYTHON_BIN}" >/dev/null 2>&1; then
  PYTHON_BIN="python3"
fi

"${PYTHON_BIN}" -m py_compile "${NODE_FILE}"
echo "Validated patched node: ${NODE_FILE}"
