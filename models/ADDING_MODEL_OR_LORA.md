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
- `/mnt/data/comfyui/models/MODEL_SUMMARY.md`

The control repo and `/mnt/data/comfyui/models` have different jobs. Keep source
artifacts in the model archive according to its rules, and keep local runnable
workflow references in this repo.

## Start With Research Only

When asked to add a model or LoRA from only a URL or a loose target, start with
a research-only phase. In this phase, read the relevant instructions and source
pages, inspect available metadata/workflows, and identify likely local scope.
Do not download weights, create sidecars, edit workflows, rename files, delete
files, stage files, or commit.

Temporary files under `/tmp` are acceptable for inspecting source metadata or
downloaded reference artifacts during research. Do not create durable repo files
or model-archive files until the research plan is accepted or the user gives an
explicit implementation instruction.

End the research phase with a concise proposed plan and scope manifest:

```text
Candidate:
- URL:
- Model or LoRA name:
- Exact version:
- Base model:
- Official/source page:
- Best source image or workflow:
- Has embedded workflow metadata:
- Extra models or LoRAs required:
- Local files likely needed:
- Proposed canonical workflow path:
- Proposed archive sidecars:
- Risks or ambiguities:

Proposed scope:
control repo:
- ...

model archive:
- ...

Out of scope:
- ...
```

The scope section should be concrete enough to guide staging and review. Include
shared-file hunk limits and explicit exclusions when nearby work may exist. For
example:

```text
TASK: Add MCNL original Qwen workflow

IN SCOPE
control repo:
- models/qwen-image/base/nsfw/qwen-mcnl.md
- workflows/qwen-image/base/nsfw/image_qwen_lora_mcnl.json
- scripts/download_models/qwen-image.sh

model archive:
- diffusion_models/qwen_image_fp8_e4m3fn.md
- diffusion_models/qwen_image_fp8_e4m3fn.html
- diffusion_models/qwen_image_fp8_e4m3fn.json
- loras/qwen_MCNL_v1.0.md
- loras/qwen_MCNL_v1.0.png
- MODEL_SUMMARY.md, only MCNL/Qwen FP8 hunks
- .gitignore, only qwen_image_fp8_e4m3fn weight ignore

OUT OF SCOPE
- SNOFS
- Qwen4Play
- `.work.json`
- fallback workflows
- memory unless explicitly requested
- any weights in git
```

Implementation may begin only after this proposed scope is accepted, modified,
or superseded by a clear user instruction. If the user already provides an
explicit implementation plan, follow it, but still keep edits and staging within
that stated scope.

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

When using a workflow-bearing image as the reference, first save or extract the
exact source artifact that contains the workflow metadata. Use that extracted
workflow as the source of truth before editing the local simplified workflow. Do
not rely only on website summary metadata when full workflow metadata is
available.

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
- after downloading a source/reference image, verify the actual file type from
  its file header and use the matching extension; do not trust the source URL
  extension;
- download required model files into `/mnt/data/comfyui/models`, keeping weights
  out of git and documenting repeatable download commands in this repo when
  useful;
- create a simplified local workflow in `workflows/` that uses plain nodes where
  practical and produces the selected reference image as closely as practical;
- save canonical workflow `.json` files pretty-printed with 2-space indentation
  (the ComfyUI GUI "Save" default, matching the rest of `workflows/`). When
  editing an existing workflow, preserve its formatting and change only the
  needed nodes; do not `jq`/reserialize a whole workflow just for a small edit,
  as that produces noisy diffs;
- diff the exact source workflow against the local workflow while simplifying,
  and account for generation-affecting differences that remain;
- preserve exact source prompt, seed, sampler, steps, CFG, dimensions, model
  mapping, VAE/text encoder choices, and negative conditioning where possible;
- document intentional substitutions, such as local filename mappings or a
  missing source VAE replaced by an available local VAE;
- add a ComfyUI `Note` node to the local workflow containing the reference image
  URL and any model or LoRA activation/trigger keywords, even when the source
  says no trigger word is required. Keep this workflow note to those facts only;
  if more information seems useful there, ask the human first;
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

After staging model-archive files and before asking the human for review or
committing, re-read `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md` and
execute its staged changes checklist against the staged/index version of the
files.
