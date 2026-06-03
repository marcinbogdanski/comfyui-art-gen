# Qwen-Image-Edit 2511

Official ComfyUI Qwen-Image-Edit 2511 native image-edit workflow.

Docs and workflow:

```text
https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit-2511
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/image_qwen_image_edit_2511.json
```

## Model Files

Diffusion model:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/qwen_image_edit_2511_bf16.safetensors \
  'https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI/resolve/main/split_files/diffusion_models/qwen_image_edit_2511_bf16.safetensors'
```

Text encoder:

```bash
mkdir -p /mnt/data/comfyui/models/text_encoders

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors \
  'https://huggingface.co/Comfy-Org/HunyuanVideo_1.5_repackaged/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors'
```

VAE:

```bash
mkdir -p /mnt/data/comfyui/models/vae

wget -c \
  -O /mnt/data/comfyui/models/vae/qwen_image_vae.safetensors \
  'https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors'
```

Optional Lightning LoRA referenced by the official template:

```bash
mkdir -p /mnt/data/comfyui/models/loras

wget -c \
  -O /mnt/data/comfyui/models/loras/Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors \
  'https://huggingface.co/lightx2v/Qwen-Image-Edit-2511-Lightning/resolve/main/Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors'
```

## Workflow

Repo copy:

```text
workflows/qwen-image/2511-edit/original/image_qwen_image_edit_2511.json
```

Current important workflow selections:

```text
UNETLoader:  qwen_image_edit_2511_bf16.safetensors
CLIPLoader:  qwen_2.5_vl_7b_fp8_scaled.safetensors
VAELoader:   qwen_image_vae.safetensors
```

The official template includes an optional Lightning LoRA switch. The LoRA is
downloaded locally so ComfyUI can load and validate the template, but it is not
part of the original baseline smoke.

## Current Local Status

Downloaded on 2026-05-28:

```text
diffusion_models/qwen_image_edit_2511_bf16.safetensors
text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
vae/qwen_image_vae.safetensors
loras/Qwen-Image-Edit-2511-Lightning-4steps-V1.0-bf16.safetensors
```

API smoke test on 2026-05-28 produced:

```text
/mnt/data/comfyui/output/smoke_qwen_image_edit_2511_00001_.png
```

## Sources

```text
https://docs.comfy.org/tutorials/image/qwen/qwen-image-edit-2511
https://huggingface.co/Qwen/Qwen-Image-Edit-2511
https://huggingface.co/Comfy-Org/Qwen-Image-Edit_ComfyUI
```
