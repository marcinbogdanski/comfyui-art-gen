# NSFW Master ZIT V2

Local Z-Image Turbo reference workflow for Civitai image 129038681 using the
NSFW Master Z-Image Turbo V2 LoRA.

## Sources

```text
Reference image:
https://civitai.red/images/129038681

Model page:
https://civitai.red/models/667086/nsfw-master?modelVersionId=2904324
```

Source version facts:

```text
LoRA:             NSFW MASTER
Version:          Z-Image Turbo V2
Model version ID: 2904324
File ID:          2782086
Base model:       ZImageTurbo
sha256:           36320CDDAE030103FF72B43C2878CB6659079BB7B742B9E90A94B5F9D6B6D33D
Civitai filename: NSFW_master_ZIT_000017532.safetensors
Local filename:   NSFW_master_ZIT_000017532.safetensors
```

The Civitai description recommends LoRA weight 0.8 and lists no trigger words.
The reference image's embedded workflow uses the LoRA at strength 1.0, so this
reproduction workflow keeps strength 1.0 to match the reference image.

## Local Files

Required local ComfyUI files:

```text
diffusion_models/z_image_turbo_bf16.safetensors
loras/NSFW_master_ZIT_000017532.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

Source-local filename mappings:

```text
z-image-turbo.safetensors (source widget label) -> z_image_turbo_bf16.safetensors
NSFW_master_ZIT_000017532.safetensors -> NSFW_master_ZIT_000017532.safetensors
qwen_3_4b.safetensors -> qwen_3_4b.safetensors
ae.safetensors -> ae.safetensors
```

The source `UNETLoader` widget is labeled `z-image-turbo.safetensors`, but the
node's own embedded model metadata points at the base
`z_image_turbo_bf16.safetensors` Comfy-Org file, so the local workflow uses that
canonical filename.

No Civitai trainedWords or trigger words are listed for this LoRA version.

## Workflow

Repo workflow:

```text
workflows/z-image/turbo/nsfw/z_image_turbo_lora_nsfw_master.json
```

The workflow reproduces the source image's direct text-to-image generation path.
The source graph was already a clean, single-pass, all-core-node ComfyUI graph,
so the only substantive change is the UNET filename mapping above. The two-pass
hires-fix variant seen in some gallery images is intentionally out of scope; this
is a first-image-only reference.

Important retained settings:

```text
UNETLoader:             z_image_turbo_bf16.safetensors, default
CLIPLoader:             qwen_3_4b.safetensors, lumina2, default
VAELoader:              ae.safetensors
LoRA:                   NSFW_master_ZIT_000017532.safetensors, model-only 1.0
                        (LoraLoaderModelOnly)
Latent size:            768 x 1024, batch 1
Seed:                   287072326087703 (fixed)
Sampler:                KSampler, 9 steps, CFG 1.0, euler, simple
Denoise:                1.0
Negative:               ConditioningZeroOut (no text negative prompt)
Save prefix:            z-image-nsfw-master
```

Notable differences from the Mystic XXX ZIT reference: this source uses
`LoraLoaderModelOnly` (model-only, no CLIP-side LoRA), a `ConditioningZeroOut`
negative instead of a text negative, and no `ModelSamplingAuraFlow` shift node.

## Current Local Status

Created from the workflow-bearing Civitai image metadata archived in
`/mnt/data/comfyui/models/loras/NSFW_master_ZIT_000017532.png`.

Frontend smoke test:

```text
2026-05-31: passed with the pinned Playwright Docker frontend smoke command,
using the actual ComfyUI frontend app.graphToPrompt() path, /prompt, and
/history success. The smoke check verified the converted workflow id
(zit-lora-nsfw-master) and 11 nodes / 10 links before submission.

Output file:
/mnt/data/comfyui/output/z-image-nsfw-master_00001_.png
```

The generated image faithfully reproduces reference image 129038681 (close-up
"finger to lips" portrait, dark hair with bangs, blue eyes, blurred background),
confirming the LoRA loads and runs correctly through the simplified workflow.
