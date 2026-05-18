# FLUX.2 Dev FP8

Official ComfyUI FLUX.2 dev example, tested on a 24 GB RTX 4090 VastAI instance with ComfyUI dynamic VRAM/RAM offload.

Docs and workflow image:

```text
https://comfyanonymous.github.io/ComfyUI_examples/flux2/
https://raw.githubusercontent.com/comfyanonymous/ComfyUI_examples/master/flux2/flux2_example.png
```

## Model Files

Text encoder:

```bash
mkdir -p /mnt/data/comfyui/models/text_encoders

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/mistral_3_small_flux2_fp8.safetensors \
  'https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/text_encoders/mistral_3_small_flux2_fp8.safetensors'
```

FP8 diffusion model:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/flux2_dev_fp8mixed.safetensors \
  'https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/diffusion_models/flux2_dev_fp8mixed.safetensors'
```

VAE:

```bash
mkdir -p /mnt/data/comfyui/models/vae

wget -c \
  -O /mnt/data/comfyui/models/vae/flux2-vae.safetensors \
  'https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors'
```

## Workflow

Use the official `flux2_example.png` workflow image directly, or extract/load the embedded GUI workflow as JSON.

Current important workflow selections:

```text
UNETLoader:             flux2_dev_fp8mixed.safetensors
CLIPLoader:             mistral_3_small_flux2_fp8.safetensors, flux2, default
VAELoader:              flux2-vae.safetensors
EmptyFlux2LatentImage:  1024 x 1024, batch 1
Flux2Scheduler:         20 steps, 1024 x 1024
Sampler:                euler
Guidance:               4.0
```

The example image embeds both GUI workflow metadata and an API prompt. The GUI workflow is the one to load from ComfyUI; the API prompt is only for programmatic queue submission.

## Notes

- The FP8 diffusion file is still large, around 35 GB on disk; this is expected.
- On the tested 24 GB RTX 4090, the exact 1024x1024 example ran successfully through ComfyUI's dynamic offload path.
- First run loads the text encoder and diffusion model into staged/offloaded memory, so expect high VRAM use and slower startup than smaller models.
- The example includes two bypassed reference-image inputs; leave them bypassed for the baseline text-to-image test.

## Sources

```text
https://comfyanonymous.github.io/ComfyUI_examples/flux2/
https://huggingface.co/Comfy-Org/flux2-dev
https://github.com/black-forest-labs/flux2
```
