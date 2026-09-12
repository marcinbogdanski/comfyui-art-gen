# Moody Pro Mix Collector's Edition

Simplified reference workflow for Civitai image 137713412 using the primary
FP8 release of Moody Pro Mix `Collector's Edition: 典藏版`.

## Sources

```text
Reference image: https://civitai.red/images/137713412
Model page:      https://civitai.red/models/620406/moody-pro-mix?modelVersionId=3161628
Version ID:      3161628
File ID:         3041996
Base model:      ZImageTurbo
Civitai file:    moodyProMix_collectorsEdition.safetensors (primary FP8)
Local file:      moodyProMix_collectorsEdition_fp8.safetensors
SHA256:          b4fd8053584dd72af86d35240b77a8d480ff43b4332ba190e54db6dce1f946a6
```

The source PNG embeds a complete ComfyUI API prompt but not a GUI workflow
graph. That prompt names an unpublished author-local checkpoint,
`ComfyUI\moody-pro-signature_00003_.safetensors`. The local workflow
reconstructs its separable two-pass path and maps the development name to the
public primary FP8 file associated with the Collector's Edition image set.

## Local Files

```text
diffusion_models/moodyProMix_collectorsEdition_fp8.safetensors
text_encoders/qwen_3_4b.safetensors
vae/ae.safetensors
```

## Workflow

```text
workflows/z-image/turbo/nsfw/z_image_turbo_merge_moody_pro_collectors_edition.json
```

The graph copies the existing Moody Pro V10 simplified two-pass structure and
replaces the model, creator prompt, seed, save prefix, and metadata. It retains:

```text
Latent size:       640x960
Seed:              778908346712803
First pass:        9 steps, CFG 1, DPM++ 2M SDE, beta, steps 0-7
Latent upscale:    bislerp 1.7x
Second pass:       DPM++ 2M SDE, sgm_uniform, start step 4
AuraFlow shift:    3
Output size:       1088x1632
```

The source final image continues through Ultimate SD Upscale and color
correction to 2176x3264. Those downstream postprocessing stages are omitted.
The source Dori Krea 2 LoRA is also omitted because its model strength is zero.
No trained words are listed.

## Current Local Status

Targeted frontend smoke test passed on 2026-08-31: 12 API nodes converted from
13 workflow nodes / 15 links, `/prompt` accepted the graph, and history
completed successfully.

```text
/mnt/data/comfyui/output/z_image_turbo_merge_moody_pro_collectors_edition_00001_.png
```
