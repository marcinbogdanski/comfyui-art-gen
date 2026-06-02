# Qwen-Image MCNL

Local text-to-image reference workflow for MCNL v1.0 on the original
Qwen-Image safetensors baseline used by the source image.

## Workflow

```text
workflows/qwen-image/base/nsfw/qwen_base_lora_mcnl.json
```

The source is Civitai image `93972166`. The actual downloaded source image is a
PNG and embeds both `prompt` and `workflow` ComfyUI metadata.

Source workflow settings preserved in the local workflow:

```text
prompt: embedded source prompt from image 93972166
negative prompt: empty
seed: 647694238050087
size: 1024 x 1360
steps: 20
CFG: 2.5
sampler: dpmpp_2m
scheduler: sgm_uniform
denoise: 1
ModelSamplingAuraFlow shift: 3.1
LoRA strength: model 1.0, clip 1.0
UNET: qwen_image_fp8_e4m3fn.safetensors
```

The source `Power Lora Loader (rgthree)` node is replaced by core `LoraLoader`
with the same MCNL LoRA and strength.

## Models

```text
diffusion_models/qwen_image_fp8_e4m3fn.safetensors
text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
vae/qwen_image_vae.safetensors
loras/qwen_MCNL_v1.0.safetensors
```

## Smoke Test

API test on 2026-05-30 against `http://127.0.0.1:8189/` passed at full source
settings using the local original Qwen-Image safetensors UNET.

```text
/mnt/data/comfyui/output/Qwen-Image-MCNL-93972166-safetensors_00001_.png
```

The output is substantially closer to the source image than the earlier
Qwen-Image 2512 substitution: same poster concept, similar body angle, large
title placement, readable `nudity` subtitle, and similar lighting/crop. Minor
differences remain in exact pose, clothing folds, and framing.
