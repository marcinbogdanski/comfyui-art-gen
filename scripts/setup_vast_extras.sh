#!/usr/bin/env bash
set -euo pipefail

COMFYUI_PATH="${COMFYUI_PATH:-/workspace/ComfyUI}"
CUSTOM_NODES_DIR="${COMFYUI_PATH}/custom_nodes"
HUNYUAN_REF="${HUNYUAN_REF:-bf738dba3f542e6744c49bc29c29a20dd14d079d}"

mkdir -p "${CUSTOM_NODES_DIR}"

clone_or_update() {
  local repo="$1"
  local dir="$2"
  local ref="$3"

  if [[ ! -d "${CUSTOM_NODES_DIR}/${dir}/.git" ]]; then
    git clone "${repo}" "${CUSTOM_NODES_DIR}/${dir}"
  fi

  git -C "${CUSTOM_NODES_DIR}/${dir}" fetch --all --tags
  git -C "${CUSTOM_NODES_DIR}/${dir}" checkout "${ref}"
}

clone_or_update \
  "https://github.com/EricRollei/Comfy_HunyuanImage3.git" \
  "Comfy_HunyuanImage3" \
  "${HUNYUAN_REF}"

if [[ -f "${CUSTOM_NODES_DIR}/Comfy_HunyuanImage3/requirements.txt" ]]; then
  python -m pip install -r "${CUSTOM_NODES_DIR}/Comfy_HunyuanImage3/requirements.txt"
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -x "${SCRIPT_DIR}/sync_vast_workflows.sh" ]]; then
  "${SCRIPT_DIR}/sync_vast_workflows.sh"
fi

echo "Vast extras setup complete."
