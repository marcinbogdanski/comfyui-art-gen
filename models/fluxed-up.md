# Fluxed Up

Civitai FLUX checkpoint tested on the VastAI RTX 4090 instance.

Links:

```text
https://civitai.red/models/847101/fluxed-up-flux-nsfw-checkpoint?modelVersionId=2892326
https://civitai.red/images/128636099
```

Download the BF16 checkpoint:

```bash
mkdir -p /mnt/data/comfyui/models/checkpoints

source ~/.bashrc

curl -L \
  -H "Authorization: Bearer ${CIVITAI_API_KEY}" \
  -o /mnt/data/comfyui/models/checkpoints/fluxedUpFluxNSFW_100BF16.safetensors \
  'https://civitai.red/api/download/models/2892326'
```

This Civitai download requires an API key. Keep it in `CIVITAI_API_KEY`.

Required shared FLUX support files:

```bash
mkdir -p /mnt/data/comfyui/models/clip /mnt/data/comfyui/models/vae

wget -c \
  -O /mnt/data/comfyui/models/clip/clip_l.safetensors \
  'https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/clip/t5xxl_fp16.safetensors \
  'https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp16.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/clip/clip_g.safetensors \
  'https://huggingface.co/Comfy-Org/stable-diffusion-3.5-fp8/resolve/main/text_encoders/clip_g.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/vae/Flux/flux_vae.safetensors \
  'https://huggingface.co/Comfy-Org/Lumina_Image_2.0_Repackaged/resolve/main/split_files/vae/ae.safetensors'
```

Workflow:

```text
workflows/fluxed-up/Fluxed_Up_Civitai_128636099.json
workflows/fluxed-up/Fluxed_Up_Civitai_128636099.api.json
```

The Civitai reference image contains an embedded ComfyUI workflow, but that
workflow depends on the uploader's custom wildcard/prompt-helper nodes and
local wildcard files. The repo workflow replaces those helpers with core nodes
and uses the resolved final prompt embedded in the image metadata.

Tested settings:

```text
Checkpoint:       fluxedUpFluxNSFW_100BF16.safetensors
Text encoders:    t5xxl_fp16.safetensors, clip_l.safetensors, clip_g.safetensors
VAE:              Flux/flux_vae.safetensors
Size:             864 x 1536
Sampler:          dpmpp_sde
Scheduler:        beta
Steps:            35
Flux guidance:    4.0
Seed:             38218886691817
```
