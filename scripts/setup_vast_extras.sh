#!/usr/bin/env bash
set -euo pipefail

COMFYUI_PATH="${COMFYUI_PATH:-/workspace/ComfyUI}"
CUSTOM_NODES_DIR="${COMFYUI_PATH}/custom_nodes"
HUNYUAN_REF="${HUNYUAN_REF:-bf738dba3f542e6744c49bc29c29a20dd14d079d}"
QWEN35_GGUF_REF="${QWEN35_GGUF_REF:-664385968c3ad3f2c48f5c02da195020517e7f73}"
LLAMA_CPP_PYTHON_WHEEL="${LLAMA_CPP_PYTHON_WHEEL:-https://github.com/JamePeng/llama-cpp-python/releases/download/v0.3.39-cu131-linux-20260519/llama_cpp_python-0.3.39%2Bcu131-cp311-cp311-linux_x86_64.whl}"

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

# Tested HunyuanImage runtime. Avoid pulling a replacement Torch wheel here.
python -m pip install --no-deps \
  "transformers==4.57.1" \
  "huggingface-hub==0.36.0" \
  "bitsandbytes==0.48.2"

clone_or_update \
  "https://github.com/Deaquay/ComfyUI-Qwen3.5-Uncensored-GGUF.git" \
  "ComfyUI-Qwen3.5-Uncensored-GGUF" \
  "${QWEN35_GGUF_REF}"

if ! python - <<'PY' >/dev/null 2>&1
from llama_cpp import Llama
from llama_cpp.llama_chat_format import Qwen3VLChatHandler
PY
then
  python -m pip install --no-cache-dir --force-reinstall --no-deps \
    "${LLAMA_CPP_PYTHON_WHEEL}"
fi

python -m pip install --no-cache-dir \
  diskcache \
  hf_xet \
  jinja2 \
  typing-extensions

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -x "${SCRIPT_DIR}/sync_vast_workflows.sh" ]]; then
  "${SCRIPT_DIR}/sync_vast_workflows.sh"
fi

echo "Vast extras setup complete."
