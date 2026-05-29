# Adding a Model or LoRA

## Goal

Add a new model or LoRA with enough source context, local files, and a simplified
reference workflow that a future agent can understand the source and reproduce
the selected example as closely as practical.

This is a goal and decision process, not a replacement for existing rules.
Before acting, read:

- `AGENTS.md`
- `workflows/README.md`
- `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md`

The control repo and `/mnt/data/comfyui/models` have different jobs. Keep source
artifacts in the model archive according to its rules, and keep local runnable
workflow references in this repo.

## Start With A Plan

When asked to add a model or LoRA, first familiarize yourself with the relevant
instructions and source pages. Then report whether you have enough information
and give a short plan. Do not begin downloads or file edits until the plan is
clear, unless the user already gave an explicit implementation plan.

## Source Selection

Prefer sources in the order defined by `AGENTS.md`: user-provided link, then
official or popular upstream source, then mirrors only when needed and
documented.

Identify the available model files and variants before downloading. Prefer the
source workflow's exact named model file when available. If the exact source
filename is local-only, map it to the closest source-listed file by model
version, precision, size, hash, and source notes. If the mapping is unclear,
pause and ask.

Avoid treating a Civitai "primary" file as canonical when its size or metadata
is suspicious for the model family. Explain the discrepancy and choose the
variant that best matches the source workflow or pause if uncertain.

## Reference Workflow Selection

Browse the available source workflows or source images. If there is only one
usable source workflow, inspect it. If there are multiple image examples, inspect
the first one first.

Use a source workflow when it meets these requirements:

- it uses the canonical or clearly mapped target model option;
- it has no required img2img/reference input unless that input is available and
  intended for the local reference;
- it has no extra LoRAs or models beyond the target source and normal support
  files, unless those dependencies are part of the target source context;
- the initial generation path is clear enough to reproduce locally.

If the first workflow does not meet these requirements, inspect a few of the
first source images/workflows and look for a clean example that can be adapted.

Pause and report to the user when:

- every candidate needs unavailable image/reference inputs;
- every candidate depends on unrelated LoRAs or extra models;
- source-local filenames cannot be mapped confidently;
- examples are dominated by postprocessing/upscalers and the initial generation
  path cannot be separated;
- the best candidate uses a heavily quantized or otherwise suspicious model file
  and the canonical mapping is ambiguous;
- no source workflow or workflow-bearing reference image is available.

## Implementation Shape

When requirements are met:

- archive source/reference artifacts under `/mnt/data/comfyui/models` following
  `MODEL_SUMMARY_RULES.md`;
- download required model files into `/mnt/data/comfyui/models`, keeping weights
  out of git and documenting repeatable download commands in this repo when
  useful;
- create a simplified local workflow in `workflows/` that uses plain nodes where
  practical and produces the selected reference image as closely as practical;
- preserve exact source prompt, seed, sampler, steps, CFG, dimensions, model
  mapping, VAE/text encoder choices, and negative conditioning where possible;
- document intentional substitutions, such as local filename mappings or a
  missing source VAE replaced by an available local VAE;
- keep `.work.json` copies local and ignored unless explicitly asked to track
  them.

Pixel-perfect reproduction is not required. The local workflow should generate
the same image in the practical sense: same subject, composition, style, and
settings, with differences explained by model-file, VAE, precision, runtime, or
postprocessing substitutions.

## Validation

Smoke test the simplified local workflow in ComfyUI when practical. Keep tests
small enough for the target GPU and record the result in the relevant model doc.
If the workflow cannot be smoke tested, record the reason and the next action.

After the smoke test, stop for human review unless the user has asked for
commits or further automation.
