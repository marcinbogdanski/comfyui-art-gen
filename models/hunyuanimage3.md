# HunyuanImage 3

HunyuanImage 3 setup notes for `EricRollei/Comfy_HunyuanImage3` on the Vast RTX
PRO 6000 Blackwell instance.

## Custom Node

Installed by:

```text
scripts/setup_vast_extras.sh
```

The tested runtime pins are:

```text
transformers==4.57.1
huggingface-hub==0.36.0
bitsandbytes==0.48.2
```

The newer `transformers` / `bitsandbytes` combination initially installed on
the Vast image produced quantized-model failures.

## Model Files

Downloaded by:

```text
scripts/download_models/hunyuanimage3.sh
```

Tested workflow models:

```text
/workspace/ComfyUI/models/HunyuanImage-3-NF4-v2
/workspace/ComfyUI/models/HunyuanImage-3.0-Instruct-Distil-NF4-v2
```

The INT8 model folders are downloaded too, but they were not reliable in this
runtime and are not used by the checked-in workflows.

## Workflows

Repo copies:

```text
workflows/hunyuanimage3/hunyuanimage3_base_nf4.json
workflows/hunyuanimage3/hunyuanimage3_base_nf4.api.json
workflows/hunyuanimage3/hunyuanimage3_instruct_distil_nf4.json
workflows/hunyuanimage3/hunyuanimage3_instruct_distil_nf4.api.json
workflows/hunyuanimage3/hunyuanimage3_instruct_multifusion_nf4.json
workflows/hunyuanimage3/hunyuanimage3_instruct_multifusion_nf4.api.json
```

Important settings:

```text
Base NF4:              post_action=keep_loaded
Instruct-Distil NF4:   vae_tiling=on, vae_offload=on
Multi-fusion NF4:      blocks_to_swap=20, image 1 = source face/identity, image 2 = target pose/scene
```

`post_action=full_unload` made second base runs fail because ComfyUI reused the
cached loader output after the model had been cleared. Keeping the model loaded
is the better default for interactive prompt/seed iteration.

`vae_tiling=auto` / `vae_offload=auto` on Instruct-Distil can return a 64x64
black fallback image after VAE decode OOM. Force both settings to `on`.

## Operational Notes

HunyuanImage can leave large model state in VRAM after failed runs or after
switching between other big models. If errors are fixed by restart, that is the
expected current recovery path:

```bash
/workspace/art-gen-ctrl/scripts/start_vast_comfyui.sh
```

If ComfyUI is already running, stop it first with the PID in
`/workspace/comfyui.pid`, then start it again. A clean idle server should show
roughly `560 MiB` VRAM used.
