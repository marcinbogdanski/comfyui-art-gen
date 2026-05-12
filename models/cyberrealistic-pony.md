# CyberRealistic Pony

Working Pony/SDXL checkpoint tested with ComfyUI.

Links:

```text
https://civitai.red/models/443821/cyberrealistic-pony
https://civitai.red/images/128392606
```

Download the FP16/pruned checkpoint:

```bash
mkdir -p /mnt/data/comfyui/models/checkpoints

wget -c \
  -O /mnt/data/comfyui/models/checkpoints/cyberrealisticPony_v180Coreshift.safetensors \
  'https://civitai.com/api/download/models/2884631?type=Model&format=SafeTensor&size=pruned&fp=fp16'
```

Download the upscaler required by the example image workflow:

```bash
mkdir -p /mnt/data/comfyui/models/upscale_models

wget -c \
  -O /mnt/data/comfyui/models/upscale_models/4x_NickelbackFS_72000_G.pth \
  'https://huggingface.co/uwg/upscaler/resolve/main/ESRGAN/4x_NickelbackFS_72000_G.pth'
```

Workflow notes:

- The workflow embedded in the Civitai image works after small fixes.
- Change the `Load Checkpoint` node to `cyberrealisticPony_v180Coreshift.safetensors`.
- Add the missing upscaler model `4x_NickelbackFS_72000_G.pth`.
- Change the scheduler in both `KSampler` nodes to `karras`.
- With those changes, the generated image is virtually identical to the source image and clean.

Things that were not required:

- `--fp32-vae`
- FP32 checkpoint
- Prompt changes
