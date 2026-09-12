# Zimage Turbo by Stable Yogi 2603 FP8

Reconstructed local reference workflow for Civitai image 135673413 using the
primary FP8 SafeTensor release of Stable Yogi 2603.

## Sources

```text
Reference image: https://civitai.red/images/135673413
Model page:      https://civitai.red/models/2221503/zimage-turbo-by-stable-yogi?modelVersionId=3096324
Version ID:      3096324
File ID:         2975960
Base model:      ZImageTurbo
Local file:      zimageTurboByStable_2603Fp8.safetensors
SHA256:          8be4161e7d6ec8a6c714e4c62a4856b92e59d16102b7d7927f0964bbf3a5fa32
```

The selected reference has no embedded ComfyUI workflow. Its Forge Neo
metadata identifies the exact published model hash and supplies the full
prompt, seed, dimensions, sampler, schedule, and shift.

## Local Files

```text
diffusion_models/zimageTurboByStable_2603Fp8.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

The source names `huihui-qwen3-4b-abliterated-v2-q8_0` and
`zImageTurboVAE_v10`; neither is local. The workflow intentionally uses the
standard Z-Image support files above, matching the substitution pattern used by
the existing Stable Yogi 2602 reconstruction.

The source negative prompt contains the Neo preset names
`BSY_General_Negatives_V1_PRO BSY_Realism_Negatives_V1_PRO`. Their expanded
prompt text is not present in the source metadata or local setup, so the local
workflow intentionally substitutes zeroed negative conditioning.

## Workflow

```text
workflows/z-image/turbo/nsfw/z_image_turbo_checkpoint_stable_yogi_2603_fp8.json
```

Retained settings:

```text
Latent size:       896x1152
Seed:              3451954774
Steps/CFG:         9 / 1
Sampler/scheduler: Euler / Beta
AuraFlow shift:    9
Negative:          zeroed positive conditioning
```

Neo's `Discard penultimate sigma: True` and clip-skip setting have no direct
plain-node equivalent and are omitted. The source prompt contains `99bsy99`,
but version 2603 has an empty Civitai `trainedWords` list, so it is preserved as
part of this reference prompt rather than declared a required trigger.

## Current Local Status

Targeted frontend smoke test passed on 2026-08-31: 10 API nodes converted from
11 workflow nodes / 10 links, `/prompt` accepted the graph, and history
completed successfully.

```text
/mnt/data/comfyui/output/z_image_turbo_checkpoint_stable_yogi_2603_fp8_00001_.png
```
