# FLUX.2 Klein NSFW T2I Stack

Local text-to-image workflow for Flux.2 Klein-family NSFW checkpoints and
LoRAs.

## Workflow

Repo copy:

```text
workflows/flux-2/klein/nsfw/image_flux2_klein_lora_stack.json
```

Reference-specific copies:

```text
workflows/flux-2/klein/nsfw/image_flux2_klein_merge_pornmaster_turbo.json
workflows/flux-2/klein/nsfw/image_flux2_klein_merge_darkbeast.json
workflows/flux-2/klein/nsfw/image_flux2_klein_merge_snofs_model.json
workflows/flux-2/klein/nsfw/image_flux2_klein_lora_base_snofs.json
workflows/flux-2/klein/nsfw/image_flux2_klein_lora_distilled_nsfw.json
workflows/flux-2/klein/nsfw/image_flux2_klein_lora_base_unchained.json
```

All workflows are plain-node variants of the official Flux.2 Klein
text-to-image graph:

```text
UNETLoader
optional LoraLoaderModelOnly chain
CLIPLoader
VAELoader
CLIPTextEncode
EmptyFlux2LatentImage
Flux2Scheduler
KSamplerSelect
CFGGuider
SamplerCustomAdvanced
VAEDecode
SaveImage
```

All LoRA nodes are bypassed by default. Un-bypass one or two at a time.

## Models

Downloaded and archived on 2026-05-29:

```text
diffusion_models/darkBeast_dbkBlitzV15_pruned_bf16.safetensors
diffusion_models/snofsSexNudesAndOtherFunStuff_v14Distilled.safetensors
diffusion_models/pornmasterFlux2Klein_v4.safetensors
loras/Flux Klein - NSFW v2.safetensors
loras/KLEIN-Unchained-V2.safetensors
loras/klein_9B_Turbo_r128.safetensors
text_encoders/qwen_3_8b.safetensors
```

Previously present:

```text
loras/klein_snofs_v1_4.safetensors
```

Download command reference:

```text
scripts/download_models/flux2-klein-nsfw.sh
```

## Reference Workflows

Each reference-specific workflow is preloaded with a representative prompt and
seed from its source workflow or source image metadata.

PornMaster + Turbo LoRA uses reference image
`https://civitai.red/images/131261970`. Its source metadata names
`flux2\PornMaster_flux2_klein_9b_base_fp8_V4.safetensors`, mapped locally to
`pornmasterFlux2Klein_v4.safetensors`.

SNOFS v1.4 Distilled uses reference image
`https://civitai.red/images/132173008`. Its source metadata names
`Snofs_1_4_KleinDistilled.safetensors`, mapped locally to
`snofsSexNudesAndOtherFunStuff_v14Distilled.safetensors`. The selected source
workflow is pure text-to-image: no img2img input, no extra LoRAs, empty
negative prompt, `1024 x 1552`, Euler, 8 steps, CFG 1, seed
`85554630378179`.

Dark Beast DBK BlitZ V1.5 uses reference image
`https://civitai.red/images/120314989`. The local reference tracks only the
initial text-to-image generation path, not the SeedVR2 upscale stage. Its source
metadata names `DarkBeastKlein-v2-Blitz-9b-BF16-single-transformer.safetensors`,
mapped locally to `darkBeast_dbkBlitzV15_pruned_bf16.safetensors`. The source
VAE name `flux2-klein-vae.safetensors` is not present locally, so the workflow
uses `flux2-vae.safetensors`.

| Workflow | UNET model | LoRA | VAE | Default steps | Steps range | Default CFG | CFG range |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `image_flux2_klein_merge_pornmaster_turbo.json` | `pornmasterFlux2Klein_v4.safetensors` | `klein_9B_Turbo_r128.safetensors` @ 1.0 | `flux2-vae.safetensors` | 4 | 4 | 1 | 1 |
| `image_flux2_klein_merge_darkbeast.json` | `darkBeast_dbkBlitzV15_pruned_bf16.safetensors` | none | `flux2-vae.safetensors` | 5 | 5 | 1 | 1 |
| `image_flux2_klein_merge_snofs_model.json` | `snofsSexNudesAndOtherFunStuff_v14Distilled.safetensors` | none | `flux2-vae.safetensors` | 8 | 6-8 | 1 | 1 |
| `image_flux2_klein_lora_base_snofs.json` | `flux-2-klein-base-9b-fp8.safetensors` | `klein_snofs_v1_4.safetensors` @ 1.0 | `flux2-vae.safetensors` | 50 | 50 | 5 | 5 |
| `image_flux2_klein_lora_distilled_nsfw.json` | `flux-2-klein-9b-fp8.safetensors` | `Flux Klein - NSFW v2.safetensors` @ 0.7 | `flux2-vae.safetensors` | 8 | 4-8 | 1 | 1-1.5 |
| `image_flux2_klein_lora_base_unchained.json` | `flux-2-klein-base-9b-fp8.safetensors` | `KLEIN-Unchained-V2.safetensors` @ 1.0 | `flux2-vae.safetensors` | 10 | 6-20 | 1 | 1 |

## Smoke Tests

API smoke tests ran on 2026-05-29 against `http://127.0.0.1:8188/` with
small outputs. PornMaster was updated afterward to the selected reference image
above.

| Configuration | Result | Output |
| --- | --- | --- |
| PornMaster + Turbo LoRA | pass | `/mnt/data/comfyui/output/flux2_klein_pornmaster_turbo_smoke_00001_.png` |
| Dark Beast DBK BlitZ V1.5 | pass | `/mnt/data/comfyui/output/flux2_klein_darkbeast_smoke_00001_.png` |
| SNOFS v1.4 Distilled checkpoint | pass | `/mnt/data/comfyui/output/flux2_klein_snofs_model_smoke_00001_.png` |
| Base + SNOFS Klein LoRA | pass | `/mnt/data/comfyui/output/flux2_klein_base_snofs_lora_smoke_00001_.png` |
| Distilled + no-face-change LoRA | pass | `/mnt/data/comfyui/output/flux2_klein_distilled_nsfw_lora_smoke_00001_.png` |
| Base + Unchained LoRA | pass | `/mnt/data/comfyui/output/flux2_klein_base_unchained_lora_smoke_00001_.png` |

No new custom nodes were required for the text-to-image workflow.
