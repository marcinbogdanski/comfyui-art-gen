# Z-Image Turbo NSFW Photorealistic ZiT 8.2

Local Z-Image Turbo reference workflow for Civitai image 131713347 using
`Z-Image Turbo NSFW [Photorealistic] [ZiT]` version `8.2 (BF16+FP8)`.

## Sources

```text
Reference image:
https://civitai.red/images/131713347

Model page:
https://civitai.red/models/2237711/z-image-turbo-nsfw-photorealistic-zit?modelVersionId=2973933

Abliterated text encoder:
https://huggingface.co/BennyDaBall/Qwen3-4b-Z-Image-Turbo-AbliteratedV1
```

Source version facts:

```text
Model:            Z-Image Turbo NSFW [Photorealistic] [ZiT]
Version:          8.2 (BF16+FP8)
Model version ID: 2973933
Base model:       ZImageTurbo
Civitai BF16 ID:  2853556
Civitai filename: zImageTurboNSFW_82BF16FP8.safetensors
Selected file:    full BF16
Local filename:   zImageTurboNSFW_82BF16.safetensors
```

The Civitai version exposes FP8 and BF16 files under the same displayed
filename. The source image metadata names `ZiTC_8.2_BF16`, so this workflow
intentionally uses the BF16 file.

## Local Files

Required local ComfyUI files:

```text
diffusion_models/zImageTurboNSFW_82BF16.safetensors
text_encoders/Qwen3-4b-Z-Image-Turbo-AbliteratedV1.safetensors
vae/ae.safetensors
```

Source-local filename mappings:

```text
diffusion_models\ZiT\WIP\ZiTC_8.2_BF16.safetensors -> zImageTurboNSFW_82BF16.safetensors
qwen\Qwen3-4b-Z-Image-Turbo-AbliteratedV1.safetensors -> Qwen3-4b-Z-Image-Turbo-AbliteratedV1.safetensors
Flux\flux_vae.safetensors -> ae.safetensors
```

The source `Flux\flux_vae.safetensors` maps to `ae.safetensors`; the local
archive copies have matching SHA256 hashes. No Civitai trainedWords or trigger
words are listed for this model version.

## Workflow

Repo workflow:

```text
workflows/z-image/turbo/nsfw/image_zit_model_photorealistic_82.json
```

The workflow keeps the source image's direct Z-Image Turbo text-to-image path
and replaces the source GUI's wildcard, string-concat, prompt-tag, rgthree, and
custom save nodes with ordinary local ComfyUI nodes. The disabled/upscale/prompt
generation branches in the embedded source workflow are intentionally omitted.

Important retained settings:

```text
UNETLoader:             zImageTurboNSFW_82BF16.safetensors, default
CLIPLoader:             Qwen3-4b-Z-Image-Turbo-AbliteratedV1.safetensors, lumina2, default
VAELoader:              ae.safetensors
Latent size:            1088 x 1632, batch 1
Seed:                   199127156564090
Sampler:                KSampler, 12 steps, CFG 1.0, dpmpp_sde, simple
Denoise:                1.0
Negative:               ConditioningZeroOut
Save prefix:            z-image-photorealistic-82
```

Prompt:

```text
A amateur photo of a 18y-o caucasian adult woman with Gold Retro Bouffant hair. She is wearing open jacket.  A adult woman with pale skin and long black hair, wearing a large, dark purple witch hat with a gold emblem. She has purple eyes and a confident smile. She is dressed in a purple lace bra that accentuates her large breasts, and an orange cloth is tied around her waist. She leans against a cracked, purple wall in a narrow alleyway with brick buildings on either side. The background includes a lantern on the left and a cloudy sky. Her expression is relaxed and seductive, and her overall appearance is that of a sexy, magical witch.

In a in a boutique cosmetics store with sleek displays, white lighting, and tiled floors location with detailed background environment.
```

Generation-affecting omission:

```text
The source graph's custom wildcard prompt processors are replaced by their
already-resolved text from the source image metadata.
The source graph's custom LoRA prompt-tags node is omitted because no active
LoRAs are present.
The source graph's disabled/upscale/LLM/image-comparer branches are omitted.
```

## Current Local Status

Created from the workflow-bearing Civitai image metadata archived in
`/mnt/data/comfyui/models/diffusion_models/zImageTurboNSFW_82BF16.png`.

Frontend smoke test:

```text
2026-06-01: passed with the pinned Playwright Docker frontend smoke command,
using the actual ComfyUI frontend app.graphToPrompt() path, /prompt, and
/history success. The smoke check verified the converted workflow id
(zit-model-photorealistic-82) and 9 API nodes / 10 workflow nodes /
9 workflow links before submission.

Output file:
/mnt/data/comfyui/output/z-image-photorealistic-82_00001_.png
```
