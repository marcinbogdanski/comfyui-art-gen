# RedCraft ZIB Distilled AGILE

Simplified local reference workflow for archived Civitai image 123529843 using
the RedCraft ERNIE RedMIX ZIB Distilled FUNxAGILE Z-Image Base checkpoint.

## Sources

```text
Reference image:
https://civitai.red/images/123529843

Model page:
https://civitai.red/models/958009/redcraft-or-or-ernie-redmix?modelVersionId=2754977
```

Source version facts:

```text
Model:            RedCraft ERNIE RedMIX
Version:          ZIB Distilled FUNxAGILE
Model version ID: 2754977
Base model:       ZImageBase
Primary filename: redcraftERNIERedmix_zibDistilled.safetensors
```

The archived reference image with embedded workflow metadata is stored outside
this control repo at:

```text
/mnt/data/comfyui/models/diffusion_models/redcraftERNIERedmix_zibDistilled.png
```

## Local Files

Required local ComfyUI files:

```text
diffusion_models/redcraftERNIERedmix_zibDistilled.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

The source image workflow used this source-local UNet filename:

```text
RedZFUN-v6-ZIB-Distilled-AGILE-8steps-ComfyUI_00001_.safetensors
```

The local workflow maps that to the archived Civitai primary filename:

```text
redcraftERNIERedmix_zibDistilled.safetensors
```

## Workflow

Repo workflow:

```text
workflows/z-image/base/nsfw/z_image_base_merge_redcraft_zib_agile.json
```

The workflow keeps only the first-pass generation path from the embedded source
metadata. It intentionally omits the source workflow's LoadImage/reference
conditioning, second pass, SeedVR2, Flux/Klein, and upscale/postprocess nodes.

Important settings:

```text
UNETLoader:        redcraftERNIERedmix_zibDistilled.safetensors, default
CLIPLoader:        qwen_3_4b.safetensors, lumina2, default
VAELoader:         ae.safetensors
Latent size:       576 x 1088, batch 1
Sampler:           euler
Scheduler:         simple
Steps:             8
CFG:               1
Denoise:           1
Seed:              622136782347257
Negative:          zeroed conditioning from the positive prompt
Save prefix:       z-image-redcraft-zib-agile
```

Prompt:

```text
a national geographic style image of a vibrant flock of pink flamingos with black legs and beaks, standing amidst numerous small gray flamingo chicks. The scene is set on a sandy shore with a deep blue sky in the background. The reflective surface in the foreground enhances the striking colors of the flamingos.


An artistic logo in the upper left corner of the screen that reads'ZImage+ AGILExFUN '
```

No Civitai trainedWords or trigger words are listed for this version.

## Current Local Status

Created on 2026-05-30 from the archived workflow-bearing Civitai image metadata.
API smoke test on 2026-05-30 produced:

```text
/mnt/data/comfyui/output/smoke_redcraft_zib_agile_00001_.png
```
