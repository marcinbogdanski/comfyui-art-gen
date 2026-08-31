# PornMaster Z-Image Turbo V3.5 BF16

Simplified local T2I reference workflow for Civitai image 129004302 using the
exact PornMaster Turbo V3.5 BF16 release.

## Sources

```text
Reference image: https://civitai.red/images/129004302
Model page:      https://civitai.red/models/2270401/pornmaster-z-image?modelVersionId=2903129
Version ID:      2903129
File ID:         2781142
Base model:      ZImageTurbo
Local file:      pornmasterZImage_turboV35Bf16.safetensors
SHA256:          4cc3baec019603f86e054ca0df8a036f17da984d8c4091b717c2a9256d0d4b15
```

The selected image embeds complete ComfyUI prompt and workflow metadata and
uses the exact BF16 release. V3.5 is described as reducing interference with
character LoRAs compared with V3.

## Local Files

```text
diffusion_models/pornmasterZImage_turboV35Bf16.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

The source CLIP filename `qweb_3_4b.safetensors` is a typo-like local alias;
the model page links `qwen_3_4b.safetensors`, which is used locally.

## Workflow

```text
workflows/z-image/turbo/nsfw/z_image_turbo_checkpoint_pornmaster_v35_bf16.json
```

Retained settings:

```text
Latent size:       1024x1536
Seed:              877135049644322
Steps/CFG:         9 / 1
Sampler/scheduler: Euler / Simple
AuraFlow shift:    3
Negative:          zeroed positive conditioning
```

The source empty LoRA-manager, GPU-cleanup, and audio notification nodes are
omitted. No active LoRAs or trained words are present.

## Current Local Status

Targeted frontend smoke test passed on 2026-08-31: 10 API nodes converted from
11 workflow nodes / 10 links, `/prompt` accepted the graph, and history
completed successfully.

```text
/mnt/data/comfyui/output/z_image_turbo_checkpoint_pornmaster_v35_bf16_00001_.png
```
