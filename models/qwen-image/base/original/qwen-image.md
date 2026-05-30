# Qwen-Image

Official ComfyUI original Qwen-Image native text-to-image workflow.

Docs and workflow:

```text
https://comfyanonymous.github.io/ComfyUI_examples/qwen_image/
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/image_qwen_image.json
```

## Model Files

Diffusion model:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/qwen_image_fp8_e4m3fn.safetensors \
  'https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_fp8_e4m3fn.safetensors'
```

Text encoder:

```bash
mkdir -p /mnt/data/comfyui/models/text_encoders

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors \
  'https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors'
```

VAE:

```bash
mkdir -p /mnt/data/comfyui/models/vae

wget -c \
  -O /mnt/data/comfyui/models/vae/qwen_image_vae.safetensors \
  'https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors'
```

The same commands are also captured in:

```text
scripts/download_models/qwen-image.sh
```

## Workflow

MCNL reference copy:

```text
workflows/qwen-image/base/nsfw/image_qwen_lora_mcnl.json
```

Current important workflow selections:

```text
UNETLoader:  qwen_image_fp8_e4m3fn.safetensors
CLIPLoader:  qwen_2.5_vl_7b_fp8_scaled.safetensors
VAELoader:   qwen_image_vae.safetensors
```

## Current Local Status

Downloaded on 2026-05-30:

```text
diffusion_models/qwen_image_fp8_e4m3fn.safetensors
text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
vae/qwen_image_vae.safetensors
```

The original safetensors file is used by the MCNL source image `93972166` and
is the exact UNET selected by the local MCNL workflow.

## Sources

```text
https://comfyanonymous.github.io/ComfyUI_examples/qwen_image/
https://huggingface.co/Qwen/Qwen-Image
https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI
```
