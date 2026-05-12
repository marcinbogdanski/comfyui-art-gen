# Big Love Klein 2 Txt2Img Upscale Workflow

Workflow-specific notes for the Civitai Big Love Klein 2 txt2img/upscale workflow.

Model files are documented in `models/big-love-klein2.md`; this note only covers workflow placement, custom nodes, and operational quirks.

## Workflow Files

Primary saved workflow:

```text
/mnt/data/comfyui/user/default/workflows/BigLove_Klein2_Txt2Img_Upscale_Civitai.json
```

Original Civitai image/workflow source:

```text
https://civitai.red/images/125229038
```

Original backup with Inspire and rgthree nodes intact:

```text
/mnt/data/comfyui/user/default/workflows/BigLove_Klein2_Txt2Img_Upscale_Civitai.original-inspire-rgthree.json
```

The working copy may be simplified if frontend/custom-node serialization gets in the way. Keep the original backup around for comparison.

## Custom Nodes

This workflow brought in additional node packs beyond the first Big Love Klein 2 reference workflow:

```bash
cd /mnt/data/comfyui/custom_nodes

git clone https://github.com/rgthree/rgthree-comfy.git
git clone https://github.com/ltdrdata/ComfyUI-Inspire-Pack.git
git clone https://github.com/ltdrdata/ComfyUI-Impact-Pack.git
```

Observed revisions:

```text
rgthree-comfy          738105a
ComfyUI-Inspire-Pack  d23db9a
ComfyUI-Impact-Pack   429d015
```

`ComfyUI-Inspire-Pack` loads `KSampler //Inspire`, but that sampler calls Impact Pack helper code at runtime. If Impact Pack is missing, queueing fails with:

```text
[ERROR] You need to install 'ComfyUI-Impact-Pack'
```

## Container Dependencies

The Docker image has been updated to bake in runtime dependencies for Easy-Use, GGUF, rgthree, Inspire, and Impact Pack. Impact-related additions include:

```text
cachetools
webcolors
dill
piexif
scikit-image
segment-anything
sam-2 @ git+https://github.com/facebookresearch/sam2
```

Rebuild after Dockerfile changes:

```bash
docker build -t local/comfyui:cu130 .
```

Impact Pack's startup script can auto-download SAM model files. A marker file was added to prevent that by default:

```text
/mnt/data/comfyui/custom_nodes/skip_download_model
```

Remove that marker only if Impact/SAM nodes are intentionally being used and model downloads are desired.

## Known Quirks

The original workflow used:

```text
KSampler //Inspire
Mute / Bypass Repeater (rgthree)
Fast Bypasser (rgthree)
```

`rgthree-comfy` logs a warning that ComfyUI's new Node 2.0 rendering may break some rgthree nodes and properties. If rgthree nodes show as missing or behave strangely, disable Node 2.0/new node rendering in the frontend settings and hard-refresh the browser.

At one point, queueing the original workflow failed with:

```text
Node 'ID #402' has no class_type. The workflow may be corrupted or a custom node is missing.
```

The node was `KSampler //Inspire`. The backend did expose that class, so this looked like frontend workflow serialization rather than a missing Python import. A pragmatic workaround is to replace `KSampler //Inspire` with core `KSampler` using the same generation settings:

```text
seed:       792533402553663
steps:      4
cfg:        1
sampler:    euler
scheduler:  beta
denoise:    1
```

This keeps core image generation close to the original but removes Inspire-specific seed/noise scheduling controls.

The rgthree bypass nodes are UI convenience controls for toggling the upscale branch. Removing them does not change the base txt2img generation path, but it can make the upscale branch always follow the normal node modes instead of being controlled by the rgthree toggle UI.

## Diversity

Four-image batches were observed to produce near-identical images when the sampler used fixed seed behavior. For more diversity:

- Set seed behavior to `randomize`.
- Use an incremental/random per-batch seed mode if using `KSampler //Inspire`.
- Queue separate runs instead of relying on one batch.
- Reduce over-constraining prompts or references when appropriate.

## Operational Check

After rebuilding and restarting ComfyUI, startup should show these packs loading:

```text
ComfyUI-GGUF
ComfyUI-Easy-Use
rgthree-comfy
ComfyUI-Inspire-Pack
ComfyUI-Impact-Pack
```

Start normally:

```bash
./run_comfyui.sh --disable-api-nodes
```
