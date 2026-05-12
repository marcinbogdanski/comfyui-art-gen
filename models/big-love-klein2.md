# Big Love Klein 2

Working Flux 2 Klein fine-tune for ComfyUI image editing/reference workflows.

## Model Files

Main diffusion model:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/bigLove_klein2_bf16_pruned.safetensors \
  'https://huggingface.co/Granddyser/biglove-klein2/resolve/main/bigLove_klein2_bf16_pruned.safetensors'
```

Text encoder:

```bash
mkdir -p /mnt/data/comfyui/models/text_encoders

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/qwen_3_8b_fp8mixed.safetensors \
  'https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-9b/resolve/main/split_files/text_encoders/qwen_3_8b_fp8mixed.safetensors?download=true'
```

VAE:

```bash
mkdir -p /mnt/data/comfyui/models/vae

wget -c \
  -O /mnt/data/comfyui/models/vae/flux2-vae.safetensors \
  'https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors?download=true'
```

Optional lower-VRAM fallback:

```bash
wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/bigLove_klein2_fp8_pruned.safetensors \
  'https://huggingface.co/Granddyser/biglove-klein2/resolve/main/bigLove_klein2_fp8_pruned.safetensors'
```

For this host's 24 GB RTX 3090, the pruned BF16 file is the preferred starting point.

## Custom Nodes

The tested Civitai workflow uses:

```bash
cd /mnt/data/comfyui/custom_nodes

git clone https://github.com/yolain/ComfyUI-Easy-Use.git
git clone https://github.com/city96/ComfyUI-GGUF.git
```

Observed revisions:

```text
ComfyUI-Easy-Use  130c1b5
ComfyUI-GGUF      6ea2651
```

`ComfyUI-GGUF` is only required by the saved workflow because it contains a GGUF loader node. That node is not connected when using the BF16 safetensors model, but ComfyUI still wants to know the node type when loading the workflow.

## Container Dependencies

ComfyUI Manager attempted to install custom node packages at runtime, but the container runs ComfyUI as the non-root `comfy` user and the Python environment is image-owned. The durable fix is to bake the needed dependencies into the Docker image.

The Dockerfile currently installs these extra packages:

```text
gguf>=0.13.0
clip_interrogator>=0.6.0
accelerate
diffusers
lark
matplotlib
onnxruntime
opencv-python-headless
peft
protobuf
sentencepiece
spandrel
```

After changing the Dockerfile, rebuild:

```bash
docker build -t local/comfyui:cu130 .
```

Then start ComfyUI normally:

```bash
./run_comfyui.sh --disable-api-nodes
```

## Workflow

The tested workflow is saved at:

```text
/mnt/data/comfyui/user/default/workflows/BigLove_Klein2_Civitai.json
```

Original Civitai image/workflow source:

```text
https://civitai.red/images/125229083
```

The original Civitai `workflow.json` was malformed for strict JSON parsers because it contained the same workflow object twice concatenated back-to-back. The fixed copy keeps one object and is pretty-printed.

Current important workflow selections:

```text
UNETLoader:       bigLove_klein2_bf16_pruned.safetensors
CLIPLoader:       qwen_3_8b_fp8mixed.safetensors, flux2, default
VAELoader:        flux2-vae.safetensors
Sampler:          euler
CFG:              1
Flux2Scheduler:   4 steps
Save prefix:      BigLoveKlein1
```

If ComfyUI still shows missing nodes after the custom nodes are installed and the backend log says they loaded, right-click the affected node and choose `Reload node`.

## Reference Images

The workflow has two reference image inputs:

```text
Image 1 -> first Reference Conditioning node
Image 1 or Image 2 -> second Reference Conditioning node through easy imageSwitch
```

The `easy imageSwitch` node is titled `Use Image 1 Only?`.

- `true`: Image 2 is ignored; Image 1 feeds both reference-conditioning passes.
- `false`: Image 2 feeds the second reference-conditioning pass.

Image 2 is not generic guidance; when enabled, it is a second explicit reference. Additional references should be feasible by chaining another `Reference Conditioning` pass, but more references can conflict or dilute control.

## Prompting Notes

This model worked best with detailed text prompts plus matching reference images.

Observed behavior:

- Detailed descriptions of character, items, location, and framing work reasonably well when the reference images match.
- Reference images alone are weak; the model does not reliably infer which visual details matter.
- Standard poses are usually okay.
- Unusual poses, occlusions, limb interactions, and contact points are fragile and can produce anatomy failures.
- For multi-reference edits, name each reference's role explicitly, for example:

```text
Use reference image 1 for character identity, reference image 2 for pose, and reference image 3 for lighting and background.
```

For harder poses, use explicit physical descriptions rather than vague intent:

```text
left hand on chair arm, right knee bent toward camera, torso leaning forward
```

## Sources

```text
https://huggingface.co/Granddyser/biglove-klein2
https://huggingface.co/Comfy-Org/vae-text-encorder-for-flux-klein-9b
https://huggingface.co/Comfy-Org/flux2-dev
https://github.com/yolain/ComfyUI-Easy-Use
https://github.com/city96/ComfyUI-GGUF
```
