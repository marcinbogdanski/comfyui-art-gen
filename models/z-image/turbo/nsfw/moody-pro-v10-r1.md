# Moody Pro Mix ZIT V10 R1 DPO

Simplified no-LoRA local reference workflow for Civitai image 131057640 using
Moody Pro Mix `ZIT V10 R1 DPO`.

## Sources

```text
Reference image:
https://civitai.red/images/131057640

Model page:
https://civitai.red/models/620406/moody-pro-mix?modelVersionId=2954679
```

Source version facts:

```text
Model:            Moody Pro Mix
Version:          ZIT V10 R1 DPO
Model version ID: 2954679
Base model:       ZImageTurbo
Civitai filename: moodyProMix_zitV10R1DPO.safetensors
Selected file:    full FP16
Local filename:   moodyProMix_zitV10R1DPO.safetensors
```

The source workflow used this source-local UNet filename:

```text
ComfyUI\zimage conversion\moody-porn-v10R1_00001_.safetensors
```

The local workflow maps that to:

```text
moodyProMix_zitV10R1DPO.safetensors
```

The source image metadata does not prove whether the author used the full FP16
or pruned FP8 Civitai file. The local archive has the full FP16 file, so this
workflow intentionally uses that variant.

## Local Files

Required local ComfyUI files:

```text
diffusion_models/moodyProMix_zitV10R1DPO.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

No acceleration LoRA or custom LoRA is required for the retained initial
generation path.

## Workflow

Repo workflow:

```text
workflows/z-image/turbo/nsfw/image_zit_model_moody_pro_v10_r1.json
```

The workflow keeps the source image's initial two-stage generation path and
omits downstream final-image branches: LoRA detailers, manual mask/inpaint,
face detector, UltimateSDUpscale, skin contrast, SeedVR, image comparers, and
unused model loaders.

Important retained settings:

```text
UNETLoader:              moodyProMix_zitV10R1DPO.safetensors, default
CLIPLoader:              qwen_3_4b.safetensors, lumina2, default
VAELoader:               ae.safetensors
Latent size:             640 x 960, batch 1
Seed:                    193375074158420
First sampler:           KSamplerAdvanced, 9 steps, CFG 1, dpmpp_2m_sde, beta
First negative:          zeroed prompt conditioning
First step range:        start 0, end 7, return leftover noise enabled
Latent upscale:          bislerp, scale 1.7
Second sampler:          KSamplerAdvanced, 9 steps, CFG 1, dpmpp_2m_sde, sgm_uniform
Second negative:         source prompt conditioning, matching the source workflow
Second step range:       start 4, end 999, return leftover noise disabled
Save prefix:             z-image-moody-pro-v10-r1
```

No Civitai trainedWords or trigger words are listed for this model version.

## Current Local Status

Created from the workflow-bearing Civitai image metadata. After the local GUI
workflow link table was checked directly, an API prompt derived from the saved
GUI workflow JSON was submitted to ComfyUI and completed on 2026-05-31,
producing the output below. This validation was not run through the actual
ComfyUI frontend `graphToPrompt()` path.

```text
/mnt/data/comfyui/output/smoke_zit_moody_pro_v10_r1_fixed_00001_.png
```

The smoke output is a 1088 x 1632 PNG, matching the 640 x 960 latent after the
source 1.7x latent upscale.
