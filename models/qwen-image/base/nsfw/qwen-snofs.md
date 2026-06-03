# Qwen-Image SNOFS

Local text-to-image reference workflow for SNOFS Qwen v1.3 on the original
Qwen-Image GGUF baseline used by the source image.

## Workflow

```text
workflows/qwen-image/2512/nsfw/qwen_2512_lora_snofs.json
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
UNET: qwen-image-Q8_0.gguf via UnetLoaderGGUF
```

The workflow filename follows the local Qwen 2512 LoRA naming style, but the
UNET is the exact source-reference GGUF from image `112774380`.

Intentional local substitution:

```text
source LoRA: Loras\Musubi\QwenSnofs13b\QwenSnofs13h-step00003500.safetensors
local LoRA:  Qwen_Snofs_1_3.safetensors
```

Activation keyword note:

```text
The Civitai metadata for SNOFS Qwen v1.3 lists no trained words. No required
activation keyword was found for this version; use normal prompt terms for the
target composition.
```

The source `TorchCompileModelQwenImage` node is preserved. The source
`QwenAspectRatioSelectorLatent` node is not installed locally, so the workflow
uses core `EmptySD3LatentImage` at the same `1056 x 1584` dimensions.

## Models

```text
diffusion_models/qwen-image-Q8_0.gguf
text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
vae/qwen_image_vae.safetensors
loras/Qwen_Snofs_1_3.safetensors
```

The SNOFS source artifact is archived externally at:

```text
/mnt/data/comfyui/models/loras/Qwen_Snofs_1_3.png
```

The GGUF source record is archived externally at:

```text
/mnt/data/comfyui/models/diffusion_models/qwen-image-Q8_0.md
```

## Smoke Test

API test on 2026-05-30 against `http://127.0.0.1:8188/` passed at the full
source settings using `UnetLoaderGGUF`, `qwen-image-Q8_0.gguf`, and the local
public `Qwen_Snofs_1_3.safetensors` LoRA.

```text
/mnt/data/comfyui/output/qwen_snofs_112774380_gguf_00001_.png
```
