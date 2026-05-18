#!/usr/bin/env bash
set -euo pipefail

COMFYUI_REF="${COMFYUI_REF:-v0.20.1}"
WORKSPACE_DIR="${WORKSPACE_DIR:-/workspace}"
COMFYUI_PATH="${COMFYUI_PATH:-${WORKSPACE_DIR}/ComfyUI}"
CUSTOM_NODES_DIR="${COMFYUI_PATH}/custom_nodes"

export DEBIAN_FRONTEND=noninteractive
export PYTHONUNBUFFERED=1
export PIP_NO_CACHE_DIR=1

apt-get update
apt-get install -y --no-install-recommends \
  ca-certificates \
  curl \
  ffmpeg \
  git \
  libgl1 \
  libglib2.0-0 \
  libsm6 \
  libxext6 \
  libxrender1 \
  rsync \
  tini
rm -rf /var/lib/apt/lists/*

mkdir -p "${WORKSPACE_DIR}"

if [[ ! -d "${COMFYUI_PATH}/.git" ]]; then
  git clone --depth 1 --branch "${COMFYUI_REF}" \
    https://github.com/Comfy-Org/ComfyUI.git "${COMFYUI_PATH}"
fi

cd "${COMFYUI_PATH}"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -r manager_requirements.txt
python -m pip install \
  "gguf>=0.17.1" \
  "clip_interrogator>=0.6.0" \
  "accelerate>=1.2.1" \
  cachetools \
  "color-matcher" \
  "colour-science" \
  "diffusers>=0.33.0" \
  dill \
  einops \
  ftfy \
  "imageio-ffmpeg" \
  lark \
  matplotlib \
  mss \
  numba \
  onnxruntime \
  opencv-python-headless \
  "peft>=0.17.0" \
  piexif \
  pixeloe \
  "pillow>=10.3.0" \
  protobuf \
  pyloudnorm \
  rembg \
  "sam-2 @ git+https://github.com/facebookresearch/sam2" \
  scikit-image \
  scipy \
  "sentencepiece>=0.2.0" \
  segment-anything \
  spandrel \
  transparent-background \
  webcolors

mkdir -p "${CUSTOM_NODES_DIR}"

clone_node() {
  local repo="$1"
  local dir="$2"
  local ref="${3:-}"

  if [[ ! -d "${CUSTOM_NODES_DIR}/${dir}/.git" ]]; then
    git clone "${repo}" "${CUSTOM_NODES_DIR}/${dir}"
  fi

  if [[ -n "${ref}" ]]; then
    git -C "${CUSTOM_NODES_DIR}/${dir}" checkout "${ref}" 2>/dev/null \
      || {
        git -C "${CUSTOM_NODES_DIR}/${dir}" fetch origin
        git -C "${CUSTOM_NODES_DIR}/${dir}" checkout "${ref}"
      }
  fi
}

clone_node https://github.com/yolain/ComfyUI-Easy-Use.git ComfyUI-Easy-Use 130c1b5
clone_node https://github.com/city96/ComfyUI-GGUF.git ComfyUI-GGUF 6ea2651
clone_node https://github.com/rgthree/rgthree-comfy.git rgthree-comfy 738105a
clone_node https://github.com/ltdrdata/ComfyUI-Inspire-Pack.git ComfyUI-Inspire-Pack d23db9a
clone_node https://github.com/ltdrdata/ComfyUI-Impact-Pack.git ComfyUI-Impact-Pack 429d015
clone_node https://github.com/kijai/ComfyUI-WanVideoWrapper.git ComfyUI-WanVideoWrapper d18cdb1
clone_node https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite.git ComfyUI-VideoHelperSuite a6879b8
clone_node https://github.com/kijai/ComfyUI-KJNodes.git ComfyUI-KJNodes fca78c9
clone_node https://github.com/cubiq/ComfyUI_essentials.git ComfyUI_essentials 9d9f4be

touch "${CUSTOM_NODES_DIR}/skip_download_model"

mkdir -p \
  "${COMFYUI_PATH}/models/checkpoints" \
  "${COMFYUI_PATH}/models/diffusion_models" \
  "${COMFYUI_PATH}/models/text_encoders" \
  "${COMFYUI_PATH}/models/vae" \
  "${COMFYUI_PATH}/models/loras" \
  "${COMFYUI_PATH}/input" \
  "${COMFYUI_PATH}/output" \
  "${COMFYUI_PATH}/user"

cat > "${WORKSPACE_DIR}/run_comfyui.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
cd "${COMFYUI_PATH:-/workspace/ComfyUI}"
exec python main.py --listen 0.0.0.0 --port "${COMFYUI_PORT:-8188}" --enable-manager "$@"
EOF
chmod +x "${WORKSPACE_DIR}/run_comfyui.sh"

echo "ComfyUI setup complete at ${COMFYUI_PATH}"
echo "Run: ${WORKSPACE_DIR}/run_comfyui.sh --disable-api-nodes"
