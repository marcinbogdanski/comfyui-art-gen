# Zimage Turbo NSFW by Stable Yogi 2602-NSFW-BF16

Local Z-Image Turbo reference workflow for Civitai image 120285584 using the
`Zimage Turbo NSFW by Stable Yogi` checkpoint, version `2602-NSFW-BF16`.

## Sources

```text
Reference image:
https://civitai.red/images/120285584

Model page:
https://civitai.red/models/2221503/zimage-turbo-nsfw-by-stable-yogi?modelVersionId=2668773
```

Source version facts:

```text
Model:            Zimage Turbo NSFW by Stable Yogi
Version:          2602-NSFW-BF16
Model version ID: 2668773
Base model:       ZImageTurbo
Civitai filename: zimageTurboNSFWBy_2602NSFWBF16.safetensors
Selected file:    full BF16 (primary)
Local filename:   zimageTurboNSFWBy_2602NSFWBF16.safetensors
SHA256:           85a1093af0667ac19e18b3b04234b695f7e97f766abbdcd3e1b0cbdc75c2db78
```

Trigger word: `99bsy99` (Civitai `trainedWords`), included at the start of the
positive prompt. The source description is brief: an experimental Z-Image Turbo
tune for darker, low-light, high-contrast scenes.

Download command (authenticated Civitai):

```bash
source ~/.bashrc
curl -L -H "Authorization: Bearer $CIVITAI_API_KEY" \
  -o /mnt/data/comfyui/models/diffusion_models/zimageTurboNSFWBy_2602NSFWBF16.safetensors \
  "https://civitai.com/api/download/models/2668773"
```

## Local Files

Required local ComfyUI files:

```text
diffusion_models/zimageTurboNSFWBy_2602NSFWBF16.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

Source filename mappings:

```text
zimageTurboNSFWBy_2602NSFWBF16.safetensors -> zimageTurboNSFWBy_2602NSFWBF16.safetensors
qwen_3_4b_fp8 (source meta) -> qwen_3_4b.safetensors
ae -> ae.safetensors
```

The reference image metadata names the text encoder `qwen_3_4b_fp8`, which is
not present locally. The non-fp8 `qwen_3_4b.safetensors` is used instead; it is
also the encoder shipped by the author's own linked workflow.

## Workflow

Repo workflow:

```text
workflows/z-image/turbo/nsfw/z_image_turbo_checkpoint_stable_yogi_2602.json
```

The reference image (120285584) carries no embedded ComfyUI workflow, only
SwarmUI-style generation parameters. This workflow reconstructs the direct
one-pass Z-Image Turbo text-to-image path from those parameters using plain
local nodes.

Important retained settings:

```text
UNETLoader:           zimageTurboNSFWBy_2602NSFWBF16.safetensors, default
CLIPLoader:           qwen_3_4b.safetensors, lumina2, default
VAELoader:            ae.safetensors
ModelSamplingAuraFlow: shift 6.3
Latent size:          1344 x 1728, batch 1 (EmptySD3LatentImage)
Seed:                 361675996
Sampler:              KSampler, 9 steps, CFG 1.0, res_multistep, bong_tangent
Denoise:              1.0
Negative:             ConditioningZeroOut
Save prefix:          z-image-stable-yogi-2602
```

The `bong_tangent` scheduler is provided by the RES4LYF custom node, which is
installed on the `x399` ComfyUI server.

Prompt:

```text
99bsy99, with her long wavy black hair, smooth light tan skin with freckles, large breasts, thick eyebrows, and a mole under her mouth, lies spread-legged on a kitchen counter, her expressive black eyes smiling as she blushes, the romantic candlelit atmosphere casting dramatic chiaroscuro shadows, her legs apart revealing her covered nipples and lips, her parted blue eyes gazing lustfully at the viewer from below. Her brown hair cascades down, twin braids adorned with a belt, while her exposing her uncensored female pubic hair, her clitoral hood visible as she lies on the counter with her knees in cross-laced footwear, a utility belt holding a zipper, surrounded by a cityscape with skyscrapers and motor vehicles.
```

Generation-affecting notes:

```text
Text encoder mapped from source qwen_3_4b_fp8 to local qwen_3_4b.safetensors.
SwarmUI-only source options with no comfy-core KSampler equivalent are omitted:
  "Discard penultimate sigma" (True) and clip skip 2.
```

The model description links a separate Civitai "Workflows" entry,
`Z Image Turbo Workflow by Stable_Yogi` (model 2186721), and says to "use the
same workflow I used for the preview images." That is a generic, heavy
multi-pass pipeline (2-pass + Detail Daemon + SeedVR2 upscale, GGUF/safetensors
switch, bypassed LoRA stacks) needing several custom node packs, and its sampler
settings (heunpp2 / linear_quadratic, 5 steps, no shift node) do not match this
image's reported parameters. It is intentionally not adopted; this workflow
reproduces the chosen reference image's own parameters with plain nodes instead.

## Current Local Status

Created from the reference image generation metadata archived in
`/mnt/data/comfyui/models/diffusion_models/zimageTurboNSFWBy_2602NSFWBF16.png`
and `.txt`.

Frontend smoke test:

```text
2026-06-01: passed with the pinned Playwright Docker frontend smoke command,
using the actual ComfyUI frontend app.graphToPrompt() path, /prompt, and
/history success. The smoke check converted the workflow id
(zit-model-stable-yogi-2602) to 10 API nodes / 11 workflow nodes /
10 workflow links before submission.

Output file:
/mnt/data/comfyui/output/z-image-stable-yogi-2602_00001_.png (1344x1728)
```
