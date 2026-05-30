# Qwen-Image 2512 SNOFS

Local fallback text-to-image reference workflow for SNOFS Qwen v1.3 on the
Qwen-Image 2512 safetensors baseline.

## Workflow

```text
workflows/qwen-image/2512/nsfw/image_qwen_2512_snofs_112774380_safetensors.json
```

The source is Civitai image `112774380`. The actual downloaded source image is
a PNG and embeds both `prompt` and `workflow` ComfyUI metadata.

Source workflow settings preserved in the local workflow:

```text
prompt: embedded source prompt from image 112774380
negative prompt: empty
seed: 1060675718359106
size: 1056 x 1584
steps: 50
CFG: 4
sampler: euler
scheduler: simple
denoise: 1
ModelSamplingAuraFlow shift: 2
LoRA strength: model 1.0, clip 1.0
```

This is not the closest source-model match. The closer workflow is:

```text
workflows/qwen-image/2512/nsfw/image_qwen2512_lora_snofs.json
```

Intentional local substitutions in this fallback workflow:

```text
source UNET: qwen-image-Q8_0.gguf
local UNET:  qwen_image_2512_fp8_e4m3fn.safetensors

source LoRA: Loras\Musubi\QwenSnofs13b\QwenSnofs13h-step00003500.safetensors
local LoRA:  Qwen_Snofs_1_3.safetensors
```

The source `QwenAspectRatioSelectorLatent` node is replaced by core
`EmptySD3LatentImage` at the same `1056 x 1584` dimensions.

## Models

```text
diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors
text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
vae/qwen_image_vae.safetensors
loras/Qwen_Snofs_1_3.safetensors
```

The SNOFS source artifact is archived externally at:

```text
/mnt/data/comfyui/models/loras/Qwen_Snofs_1_3.png
```

## Smoke Test

API test on 2026-05-30 against `http://127.0.0.1:8188/` passed at the full
source settings using the local safetensors UNET.

```text
/mnt/data/comfyui/output/qwen_2512_snofs_112774380_safetensors_00001_.png
```
