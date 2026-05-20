# Qwen3.5 VLM Examples

These workflows target `Deaquay/ComfyUI-Qwen3.5-Uncensored-GGUF` and the
Qwen3.5 35B A3B GGUF model documented in `models/qwen3.5-35b-a3b.md`.

The workflow loads an image, sends it through
`Qwen3.5-Uncensored Advanced (GGUF)`, previews the returned description with
`Preview as Text`, and saves the same description as a text file with
`Save String KJ`.

Set `keep_model_loaded=false` for normal mixed-model ComfyUI sessions. Leave it
enabled only when repeatedly captioning many images and no other large model
needs the GPU.
