# Mystic XXX ZIT V7

Local Z-Image Turbo reference workflow for Civitai image 127357705 using the
Mystic XXX ZIT v7 LoRA.

## Sources

```text
Reference image:
https://civitai.red/images/127357705

Model page:
https://civitai.red/models/2206377/zit-mystic-xxx?modelVersionId=2855359
```

Source version facts:

```text
LoRA:             Mystic-XXX-ZIT-V7
Version:          v7.0
Model version ID: 2855359
Base model:       ZImageTurbo
Civitai filename: Mystic-XXX-ZIT-V7.safetensors
Local filename:   Mystic-XXX-ZIT-V7.safetensors
```

## Local Files

Required local ComfyUI files:

```text
diffusion_models/z_image_turbo_bf16.safetensors
loras/Mystic-XXX-ZIT-V7.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

Source-local filename mappings:

```text
z-image/z_image_turbo_bf16.safetensors -> z_image_turbo_bf16.safetensors
ZIT/Mystic-XXX-ZIT-V7.safetensors -> Mystic-XXX-ZIT-V7.safetensors
qwen_3_4b.safetensors -> qwen_3_4b.safetensors
Flux/ae.safetensors -> ae.safetensors
```

No Civitai trainedWords or trigger words are listed for this LoRA version.

## Workflow

Repo workflow:

```text
workflows/z-image/turbo/nsfw/z_image_turbo_lora_mystic_xxx_v7.json
```

The workflow keeps the source image's direct text-to-image generation path and
replaces source-machine prompt-file/group nodes with ordinary local ComfyUI
nodes. It preserves the embedded source prompt, negative prompt, model sampling
shift, latent size, batch size, seed, sampler, scheduler, CFG, denoise, and LoRA
strengths.

Important retained settings:

```text
UNETLoader:             z_image_turbo_bf16.safetensors, default
CLIPLoader:             qwen_3_4b.safetensors, lumina2, default
VAELoader:              ae.safetensors
Model sampling shift:   3.0
LoRA:                   Mystic-XXX-ZIT-V7.safetensors, model 1.0, clip 1.0
Latent size:            832 x 1216, batch 2
Seed:                   802953
Sampler:                KSampler, 9 steps, CFG 1.0, res_2s, bong_tangent
Denoise:                1.0
Negative prompt:        blurry ugly bad
Save prefix:            z-image-mystic-xxx-v7
```

## Current Local Status

Created from the workflow-bearing Civitai image metadata in
`/mnt/data/comfyui/models/loras/Mystic-XXX-ZIT-V7.png`.

Frontend smoke test:

```text
2026-05-31: passed with the pinned Playwright Docker frontend smoke command,
using the actual ComfyUI frontend `app.graphToPrompt()` path, `/prompt`, and
`/history` success.

Output files:
/mnt/data/comfyui/output/z-image-mystic-xxx-v7_00003_.png
/mnt/data/comfyui/output/z-image-mystic-xxx-v7_00004_.png
```

The smoke script now verifies the frontend-converted workflow id and node/link
counts before submission, avoiding a startup race where ComfyUI's default graph
can otherwise overwrite the just-loaded workflow.
