# Dark Beast DBZiT9 DIM RClaw

Local Z-Image Turbo reference workflow for Civitai image 124809807 using the
Dark Beast `DBZiT9 DIM RClaw` checkpoint.

## Sources

```text
Reference image:
https://civitai.red/images/124809807

Model page:
https://civitai.red/models/2242173/dark-beast-or?modelVersionId=2788849
```

Source version facts:

```text
Model:            Dark Beast
Version:          DBZiT9 DIM RClaw
Model version ID: 2788849
Base model:       ZImageTurbo
Civitai filename: darkBeast_dbzit9DIMRclaw.safetensors
Selected file:    pruned BF16
Local filename:   darkBeast_dbzit9DIMRclaw.safetensors
```

The source description recommends CFG 1, 8 steps, and Euler + Simple. It says
the version is remixed around Moody Porn Mix 8 for faster inference, sharper
coherence, fewer hallucinations, and improved poses, faces, and details.

## Local Files

Required local ComfyUI files:

```text
diffusion_models/darkBeast_dbzit9DIMRclaw.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

Source-local filename mappings:

```text
DarkBeastZ9-RClaw-8step-BF16-ComfyUI.safetensors -> darkBeast_dbzit9DIMRclaw.safetensors
qwen_3_4b.safetensors -> qwen_3_4b.safetensors
ae.safetensors -> ae.safetensors
```

No Civitai trainedWords or trigger words are listed for this model version.

## Workflow

Repo workflow:

```text
workflows/z-image/turbo/nsfw/image_zit_model_dark_beast_dbzit9_rclaw.json
```

The workflow keeps the source image's core two-pass Z-Image Turbo path and
omits the downstream SeedVR2 upscaler branch. No active LoRAs are retained in
the source prompt path. The embedded GUI workflow does contain disabled
`LoraLoaderModelOnly` nodes for `zit_fdpo_v1.safetensors` and
`Z1\Z-Detail-Slider.safetensors`, both at strength 0.35; those inactive nodes
are intentionally omitted.

Important retained settings:

```text
UNETLoader:       darkBeast_dbzit9DIMRclaw.safetensors, default
CLIPLoader:       qwen_3_4b.safetensors, lumina2, default
VAELoader:        ae.safetensors
Latent size:      768 x 1024, batch 1
First seed:       532351574181291
First sampler:    KSampler, 8 steps, CFG 1.0, euler, simple, denoise 1.0
Negative:         ConditioningZeroOut
Intermediate:     decode, bicubic scale to 864 x 1632, VAE encode
Refine seed:      194935556594676
Refine sampler:   KSampler, 8 steps, CFG 1.0, euler, simple, denoise 0.5
Save prefix:      z-image-dark-beast-dbzit9-rclaw
```

Generation-affecting omission:

```text
SeedVR2 final upscaler branch omitted.
Disabled zit_fdpo_v1.safetensors LoRA node omitted.
Disabled Z1\Z-Detail-Slider.safetensors LoRA node omitted.
```

The source image metadata includes a SeedVR2 branch after the refined image. The
local workflow intentionally stops at the refined ZIT image because the goal is
to validate the checkpoint and reconstruct the core reference, not the final
external upscaler polish.

## Current Local Status

Created from the workflow-bearing Civitai image metadata archived in
`/mnt/data/comfyui/models/diffusion_models/darkBeast_dbzit9DIMRclaw.png`.

Frontend smoke test:

```text
2026-05-31: passed with the pinned Playwright Docker frontend smoke command,
using the actual ComfyUI frontend app.graphToPrompt() path, /prompt, and
/history success. The smoke check verified the converted workflow id
(zit-model-dark-beast-dbzit9-rclaw) and 14 API nodes / 15 workflow nodes /
18 workflow links before submission.

Output files:
/mnt/data/comfyui/output/z-image-dark-beast-dbzit9-preview_00001_.png
/mnt/data/comfyui/output/z-image-dark-beast-dbzit9-rclaw_00001_.png
```
