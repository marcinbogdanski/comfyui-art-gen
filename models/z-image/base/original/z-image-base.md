# Z-Image Base

Official ComfyUI Z-Image base text-to-image workflow.

Docs and workflow:

```text
https://docs.comfy.org/tutorials/image/z-image/z-image
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/z_image_base_original.json
```

## Model Files

Diffusion model:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/z_image_bf16.safetensors \
  'https://huggingface.co/Comfy-Org/z_image/resolve/main/split_files/diffusion_models/z_image_bf16.safetensors'
```

Text encoder:

```bash
mkdir -p /mnt/data/comfyui/models/text_encoders

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/qwen_3_4b.safetensors \
  'https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/text_encoders/qwen_3_4b.safetensors'
```

VAE:

```bash
mkdir -p /mnt/data/comfyui/models/vae

wget -c \
  -O /mnt/data/comfyui/models/vae/ae.safetensors \
  'https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/vae/ae.safetensors'
```

## Workflow

Repo copy:

```text
workflows/z-image/base/original/z_image_base_original.json
```

Current important workflow selections:

```text
UNETLoader:  z_image_bf16.safetensors
CLIPLoader:  qwen_3_4b.safetensors
VAELoader:   ae.safetensors
```

Existing local Ogre workflow files in this folder are separate local variants
and are not the official baseline workflow.

## Current Local Status

Downloaded on 2026-05-28:

```text
diffusion_models/z_image_bf16.safetensors
```

The shared Z-Image support files `text_encoders/qwen_3_4b.safetensors` and
`vae/ae.safetensors` were already present from Z-Image-Turbo.

API smoke test on 2026-05-28 produced:

```text
/mnt/data/comfyui/output/smoke_z_image_base_00001_.png
```

## Sources

```text
https://docs.comfy.org/tutorials/image/z-image/z-image
https://huggingface.co/Tongyi-MAI/Z-Image
https://huggingface.co/Comfy-Org/z_image
```
