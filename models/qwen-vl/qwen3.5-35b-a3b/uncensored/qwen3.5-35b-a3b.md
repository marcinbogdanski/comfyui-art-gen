# Qwen3.5 35B A3B Uncensored HauhauCS Aggressive

Setup notes for running the GGUF VLM inside ComfyUI on the Vast RTX PRO 6000
Blackwell instance.

## Custom Node

Installed by:

```text
scripts/setup_vast_extras.sh
```

The tested node pack is:

```text
Deaquay/ComfyUI-Qwen3.5-Uncensored-GGUF
```

The tested `llama-cpp-python` wheel is:

```text
llama_cpp_python-0.3.39+cu131-cp311-cp311-linux_x86_64.whl
```

This wheel provides the Qwen VL chat handlers needed for GGUF plus `mmproj`
image input.

## Model Files

Downloaded by:

```text
scripts/download_models/qwen3.5-35b-a3b.sh
```

Model source files:

```text
/workspace/ComfyUI/models/LLM/GGUF/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf
/workspace/ComfyUI/models/LLM/GGUF/Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive/mmproj-Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-f16.gguf
```

The node scans this `LLM/GGUF` location and discovers the model as:

```text
[local] Qwen3.5-35B-A3B-Uncensored-HauhauCS-Aggressive-Q4_K_M.gguf
```

## Workflow

Repo copies:

```text
workflows/qwen35/qwen3.5_35b_vlm_describe.json
```

This workflow loads an image, sends it through the
`Qwen3.5-Uncensored Advanced (GGUF)` node, previews the returned description,
and saves the same description as a text file with the `qwen35_description`
prefix.

Set `keep_model_loaded=false` when using it as an occasional image description
or tagging step so ComfyUI unloads the GGUF model after the run.

## Smoke Test

Tested by direct node invocation with a synthetic red-square image:

```text
Output: A solid red square centered on a black background.
VRAM after unload: roughly 560 MiB
```
