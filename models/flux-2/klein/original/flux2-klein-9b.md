# FLUX.2 Klein 9B

Official ComfyUI FLUX.2 Klein 9B workflows from the Comfy-Org template
repository.

Docs and workflows:

```text
https://docs.comfy.org/tutorials/flux/flux-2-klein
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/flux2_klein_original_9b.json
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/image_flux2_klein_image_edit_9b_base.json
https://raw.githubusercontent.com/Comfy-Org/workflow_templates/refs/heads/main/templates/image_flux2_klein_image_edit_9b_distilled.json
```

## Model Files

Diffusion models:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  --header="Authorization: Bearer ${HF_TOKEN}" \
  -O /mnt/data/comfyui/models/diffusion_models/flux-2-klein-base-9b-fp8.safetensors \
  'https://huggingface.co/black-forest-labs/FLUX.2-klein-base-9b-fp8/resolve/main/flux-2-klein-base-9b-fp8.safetensors'

wget -c \
  --header="Authorization: Bearer ${HF_TOKEN}" \
  -O /mnt/data/comfyui/models/diffusion_models/flux-2-klein-9b-fp8.safetensors \
  'https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8/resolve/main/flux-2-klein-9b-fp8.safetensors'
```

Text encoder:

```bash
mkdir -p /mnt/data/comfyui/models/text_encoders

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/qwen_3_8b_fp8mixed.safetensors \
  'https://huggingface.co/Comfy-Org/flux2-klein-9B/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors'
```

VAE:

```bash
mkdir -p /mnt/data/comfyui/models/vae

wget -c \
  --header="Authorization: Bearer ${HF_TOKEN}" \
  -O /mnt/data/comfyui/models/vae/full_encoder_small_decoder.safetensors \
  'https://huggingface.co/black-forest-labs/FLUX.2-small-decoder/resolve/main/full_encoder_small_decoder.safetensors'
```

The ComfyUI docs page also lists `flux2-vae.safetensors` in the 9B storage
section; the current 9B template metadata uses `full_encoder_small_decoder.safetensors`.

## Workflow

Repo copies:

```text
workflows/flux-2/klein/original/flux2_klein_original_9b.json
workflows/flux-2/klein/original/flux2_klein_original_9b_distilled.json
workflows/flux-2/klein/original/image_flux2_klein_image_edit_9b_base.json
workflows/flux-2/klein/original/image_flux2_klein_image_edit_9b_distilled.json
```

Current important 9B base text-to-image selections:

```text
UNETLoader:  flux-2-klein-base-9b-fp8.safetensors
CLIPLoader:  qwen_3_8b_fp8mixed.safetensors
VAELoader:   full_encoder_small_decoder.safetensors
```

Current important 9B distilled text-to-image selections:

```text
UNETLoader:      flux-2-klein-9b-fp8.safetensors
CLIPLoader:      qwen_3_8b_fp8mixed.safetensors
VAELoader:       full_encoder_small_decoder.safetensors
Flux2Scheduler:  4 steps
CFGGuider:       1 CFG
```

## Current Local Status

Downloaded on 2026-05-28:

```text
diffusion_models/flux-2-klein-base-9b-fp8.safetensors
diffusion_models/flux-2-klein-9b-fp8.safetensors
text_encoders/qwen_3_8b_fp8mixed.safetensors
vae/full_encoder_small_decoder.safetensors
```

API smoke test on 2026-05-28 produced:

```text
/mnt/data/comfyui/output/smoke_flux2_klein_9b_00001_.png
/mnt/data/comfyui/output/smoke_flux2_klein_9b_distilled_00001_.png
```

The smoke test used the official 9B text-to-image path with
`flux-2-klein-base-9b-fp8.safetensors`. A second API smoke test used the same
graph shape with `flux-2-klein-9b-fp8.safetensors` and distilled settings.

## Sources

```text
https://docs.comfy.org/tutorials/flux/flux-2-klein
https://huggingface.co/black-forest-labs/FLUX.2-klein-base-9b-fp8
https://huggingface.co/black-forest-labs/FLUX.2-klein-9b-fp8
https://huggingface.co/Comfy-Org/flux2-klein-9B
```
