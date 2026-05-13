# Wan 2.2 Kijai Wrapper

Wan 2.2 setup notes for `ComfyUI-WanVideoWrapper`.

## Custom Nodes

Installed under `/mnt/data/comfyui/custom_nodes`:

```text
ComfyUI-WanVideoWrapper  d18cdb1
ComfyUI-VideoHelperSuite a6879b8
ComfyUI-KJNodes          fca78c9
```

The Docker image bakes in the Python dependencies for these nodes. Rebuild
after Dockerfile changes:

```bash
docker build -t local/comfyui:cu130 .
```

## Workflows

Upstream workflows are saved unchanged:

```text
/mnt/data/comfyui/user/default/workflows/wan22-upstream
```

Editable copies are saved separately:

```text
/mnt/data/comfyui/user/default/workflows/wan22-work
```

The first work copies changed only:

- `LoadImage` input to `BigLoveKlein1_00070_.png`
- `WanVideoModelLoader` attention mode from `sageattn` to `sdpa`
- model path separators from Windows `\` to Linux/API-friendly `/`

Reason: `sageattention` is optional and was not installed because it can require
native/CUDA build work. `sdpa` is the wrapper default and works with the runtime
image.

## Recommended First Test

Start with:

```text
/mnt/data/comfyui/user/default/workflows/wan22-work/wanvideo_2_2_I2V_A14B_example_WIP.work.json
```

The basic A14B I2V workflow imports cleanly except for missing `Note` nodes,
which are annotation nodes and not part of execution.

An API-format prompt for the executable path to `VHS_VideoCombine` is saved at:

```text
/mnt/data/comfyui/user/default/workflows/wan22-work/wanvideo_2_2_I2V_A14B_example_WIP.api.json
```

For normal testing, prefer the no-compile copies:

```text
/mnt/data/comfyui/user/default/workflows/wan22-work/wanvideo_2_2_I2V_A14B_example_WIP.no_compile.work.json
/mnt/data/comfyui/user/default/workflows/wan22-work/wanvideo_2_2_I2V_A14B_example_WIP.no_compile.api.json
```

These disconnect `WanVideoTorchCompileSettings` from both
`WanVideoModelLoader` `compile_args` inputs. Keeping compile enabled on the
runtime image failed at sampling time because PyTorch/Triton wanted a C
compiler. The no-compile API prompt completed successfully.

The no-compile copies also set `VHS_VideoCombine.save_output=true` so future
videos are saved to `/mnt/data/comfyui/output` instead of only container temp.

## Required Model Files

For the basic Kijai Wan 2.2 A14B I2V workflow:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models/WanVideo/2_2
mkdir -p /mnt/data/comfyui/models/loras/WanVideo/Lightx2v
mkdir -p /mnt/data/comfyui/models/text_encoders
mkdir -p /mnt/data/comfyui/models/vae/wanvideo

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/WanVideo/2_2/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors \
  'https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/I2V/Wan2_2-I2V-A14B-HIGH_fp8_e4m3fn_scaled_KJ.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/WanVideo/2_2/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors \
  'https://huggingface.co/Kijai/WanVideo_comfy_fp8_scaled/resolve/main/I2V/Wan2_2-I2V-A14B-LOW_fp8_e4m3fn_scaled_KJ.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/loras/WanVideo/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors \
  'https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Lightx2v/lightx2v_I2V_14B_480p_cfg_step_distill_rank64_bf16.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/umt5-xxl-enc-bf16.safetensors \
  'https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-bf16.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/vae/wanvideo/Wan2_1_VAE_bf16.safetensors \
  'https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors'
```

The upstream graph also contains an unconnected native `CLIPLoader` branch that
references `umt5_xxl_fp16.safetensors`. It was left unchanged, but it is not on
the execution path for the first A14B I2V test.

## Optional Smaller 5B I2V Test

The 5B I2V workflow copy is:

```text
/mnt/data/comfyui/user/default/workflows/wan22-work/wanvideo_2_2_5B_I2V_example_WIP.work.json
```

It references:

```bash
mkdir -p /mnt/data/comfyui/models/diffusion_models/WanVideo/2_2
mkdir -p /mnt/data/comfyui/models/text_encoders
mkdir -p /mnt/data/comfyui/models/vae/wanvideo

wget -c \
  -O /mnt/data/comfyui/models/diffusion_models/WanVideo/2_2/wan2.2_ti2v_5B_fp16.safetensors \
  'https://huggingface.co/Comfy-Org/Wan_2.2_ComfyUI_Repackaged/resolve/main/split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/text_encoders/umt5-xxl-enc-bf16.safetensors \
  'https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-bf16.safetensors'

wget -c \
  -O /mnt/data/comfyui/models/vae/wanvideo/Wan2_2_VAE_bf16.safetensors \
  'https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_2_VAE_bf16.safetensors'
```

## Startup Check

Start detached:

```bash
COMFYUI_DETACH=1 COMFYUI_CONTAINER_NAME=comfyui ./run_comfyui.sh --disable-api-nodes
```

Check logs:

```bash
docker logs --tail 240 comfyui
```

Known startup warnings:

- `sageattention` missing: expected unless we intentionally add it later.
- FantasyPortrait `onnx` missing: irrelevant for the basic Wan 2.2 I2V workflow.
