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
        "gguf>=0.13.0" \
        "clip_interrogator>=0.6.0" \
        accelerate \
        diffusers \
        lark \
        matplotlib \
        onnxruntime \
        opencv-python-headless \
        peft \
        protobuf \
        sentencepiece \
        spandrel

USER comfy

VOLUME ["/opt/ComfyUI/models", "/opt/ComfyUI/input", "/opt/ComfyUI/output", "/opt/ComfyUI/custom_nodes", "/opt/ComfyUI/user"]

EXPOSE 8188

ENTRYPOINT ["/usr/bin/tini", "--", "python", "main.py"]
CMD ["--listen", "0.0.0.0", "--port", "8188", "--enable-manager"]
