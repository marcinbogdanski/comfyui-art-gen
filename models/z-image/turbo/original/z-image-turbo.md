# Z-Image-Turbo

Official ComfyUI Z-Image-Turbo text-to-image workflow, tested on a 24 GB RTX 4090 VastAI instance.

Docs and workflow:

```text
https://docs.comfy.org/tutorials/image/z-image/z-image-turbo
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/image_z_image_turbo.json
```

## Model Files

Diffusion model:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/z_image_turbo_bf16.safetensors \
  'https://huggingface.co/Comfy-Org/z_image_turbo/resolve/main/split_files/diffusion_models/z_image_turbo_bf16.safetensors'
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
workflows/z-image/image_z_image_turbo.json
```

Optional LoRAs:

- [Civit.Art V2T1](https://civitai.red/models/2502792/civitart?modelVersionId=2937757) - painterly style
- [Civit.Art V1TI](https://civitai.red/models/2502792/civitart?modelVersionId=2813397) - illustration style

Current important workflow selections:

```text
UNETLoader:             z_image_turbo_bf16.safetensors
CLIPLoader:             qwen_3_4b.safetensors, lumina2, default
VAELoader:              ae.safetensors
EmptySD3LatentImage:    1024 x 1024, batch 1
ModelSamplingAuraFlow:  shift 3
KSampler:               4 steps, cfg 1, res_multistep, simple
```

## Notes

- The official workflow template is a GUI workflow/subgraph template, not a direct API prompt graph.
- Tested successfully on the rented 24 GB RTX 4090 with dynamic loading.
- The test output used the `z-image-turbo` save prefix.
