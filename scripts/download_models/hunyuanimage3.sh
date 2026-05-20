#!/usr/bin/env bash
set -euo pipefail

mkdir -p /workspace/ComfyUI/models

hf download EricRollei/HunyuanImage-3-NF4-v2 \
  --local-dir /workspace/ComfyUI/models/HunyuanImage-3-NF4-v2

hf download EricRollei/HunyuanImage-3-INT8-v2 \
  --local-dir /workspace/ComfyUI/models/HunyuanImage-3-INT8-v2

hf download EricRollei/HunyuanImage-3.0-Instruct-Distil-NF4-v2 \
  --local-dir /workspace/ComfyUI/models/HunyuanImage-3.0-Instruct-Distil-NF4-v2

hf download EricRollei/HunyuanImage-3.0-Instruct-Distil-INT8-v2 \
  --local-dir /workspace/ComfyUI/models/HunyuanImage-3.0-Instruct-Distil-INT8-v2
