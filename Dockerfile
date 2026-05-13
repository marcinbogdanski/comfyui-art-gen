FROM pytorch/pytorch:2.9.1-cuda13.0-cudnn9-runtime

ARG COMFYUI_REF=v0.20.1
ARG USER_ID=1000
ARG GROUP_ID=1000

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    COMFYUI_PATH=/opt/ComfyUI

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        ffmpeg \
        git \
        libgl1 \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        tini \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid "${GROUP_ID}" comfy \
    && useradd --uid "${USER_ID}" --gid "${GROUP_ID}" --create-home --shell /bin/bash comfy

RUN git clone --depth 1 --branch "${COMFYUI_REF}" https://github.com/Comfy-Org/ComfyUI.git "${COMFYUI_PATH}" \
    && chown -R comfy:comfy "${COMFYUI_PATH}" /home/comfy

WORKDIR ${COMFYUI_PATH}

RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install -r requirements.txt \
    && python -m pip install -r manager_requirements.txt \
    && python -m pip install \
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

USER comfy

VOLUME ["/opt/ComfyUI/models", "/opt/ComfyUI/input", "/opt/ComfyUI/output", "/opt/ComfyUI/custom_nodes", "/opt/ComfyUI/user"]

EXPOSE 8188

ENTRYPOINT ["/usr/bin/tini", "--", "python", "main.py"]
CMD ["--listen", "0.0.0.0", "--port", "8188", "--enable-manager"]
