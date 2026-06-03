# Qwen-Image 2512

Official ComfyUI Qwen-Image 2512 native text-to-image workflow.

Docs and workflow:

```text
https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/qwen_2512_original.json
```

## Model Files

Diffusion model:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors \
  'https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors'
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

## Workflow

Repo copy:

```text
workflows/qwen-image/2512/original/qwen_2512_original.json
```

Current important workflow selections:

```text
UNETLoader:  qwen_image_2512_fp8_e4m3fn.safetensors
CLIPLoader:  qwen_2.5_vl_7b_fp8_scaled.safetensors
VAELoader:   qwen_image_vae.safetensors
```

The official template includes an optional Lightning LoRA switch. The LoRA is
not part of the original baseline set and is not downloaded here.

## Current Local Status

Downloaded on 2026-05-28:

```text
diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors
text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
vae/qwen_image_vae.safetensors
```

API smoke test on 2026-05-28 produced:

```text
/mnt/data/comfyui/output/smoke_qwen_image_2512_00001_.png
```

## Sources

```text
https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512
https://huggingface.co/Qwen/Qwen-Image-2512
https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI
```
