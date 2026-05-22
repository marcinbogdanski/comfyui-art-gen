# Model Summary Rules

This file defines the rules for external ComfyUI model reference files under
`/mnt/data/comfyui/models`.

These rules are intentionally limited to the external ComfyUI model folders.
They do not define the purpose, naming, or tracking policy for this repo's
`workflows/` directory. The external model folders and this repo are separate
resources with different jobs.

## Purpose

External ComfyUI model folders are source/reference archives for downloaded
single-file models and LoRAs.

They should preserve enough upstream context to understand where a weight file
came from, how it was intended to be used, and what source workflow or source
metadata was available at download time.

They are not a working area for local workflow development, API prompt graphs,
repo-specific workflow edits, or ComfyUI GUI scratch files.

The external folder must make sense on its own. Do not assume this git repo
exists when deciding what belongs next to a model file in
`/mnt/data/comfyui/models`.

## Scope

These rules apply to single-file model and LoRA assets stored in external
ComfyUI model folders, including typical locations such as:

- `/mnt/data/comfyui/models/checkpoints`
- `/mnt/data/comfyui/models/loras`
- `/mnt/data/comfyui/models/diffusion_models`
- other `/mnt/data/comfyui/models/...` folders when they contain single-file
  downloaded weights

These rules do not apply to:

- this git repo's `workflows/` directory
- ComfyUI live workflow state under `/mnt/data/comfyui/user/default/workflows`
- generated images under `/mnt/data/comfyui/output`
- input images under `/mnt/data/comfyui/input`
- custom nodes under `/mnt/data/comfyui/custom_nodes`
- full Hugging Face model repository directories, except where explicitly
  stated below

## Separate From Repo Workflows

The external ComfyUI model folders and this repo's `workflows/` directory serve
different purposes.

External model folders are upstream/source reference archives for model files.

Repo `workflows/` files are local runnable workflow references tracked by git.

There may be overlap. A workflow kept in this repo may be copied from, identical
to, or adapted from a source workflow stored in an external model folder. That
does not merge the two policies. Once a workflow is in this repo, it is governed
by repo workflow rules, not by this external-folder policy.

From the external folder perspective, this repo does not exist.

## Allowed Files

For a single-file model or LoRA source set, external model folders may contain
only these kinds of companion/reference files:

- the weight file, such as `.safetensors` or another actual model/LoRA weight
  file
- a mandatory Markdown sidecar, `.md`
- a mandatory raw source description page, `.html`
- an optional source/reference image, `.png`, `.jpeg`, or `.jpg`
- an optional raw upstream workflow, `.json`
- an optional source metadata text file, `.txt`

No other companion/reference file types should be created in external model
folders for single-file model/LoRA source sets unless the user explicitly asks
for that specific file.

## Companion File Naming

Companion/reference files for a single-file model or LoRA should use the exact
weight-file stem plus the companion extension by default.

When a model has multiple canonical source/reference artifacts, or when a
workflow is shared by a paired model set, the `.md` JSON `workflows` array is
the authority. In that case, use the exact filenames listed there and keep them
in the same folder.

For a weight file named:

```text
cyberrealisticPony_v180Coreshift.safetensors
```

valid same-stem companion names are:

- `cyberrealisticPony_v180Coreshift.md`
- `cyberrealisticPony_v180Coreshift.html`
- `cyberrealisticPony_v180Coreshift.png`
- `cyberrealisticPony_v180Coreshift.jpeg`
- `cyberrealisticPony_v180Coreshift.jpg`
- `cyberrealisticPony_v180Coreshift.json`
- `cyberrealisticPony_v180Coreshift.txt`

Do not add descriptive suffixes between the model stem and extension unless the
file is explicitly listed in the `.md` JSON `workflows` array because it is a
separate canonical artifact.

Invalid examples:

- `cyberrealisticPony_v180Coreshift_reference.jpeg`
- `cyberrealisticPony_v180Coreshift_reference.parameters.txt`
- `cyberrealisticPony_v180Coreshift.workflow.json`

## Forbidden Files

Never save raw Civitai API dump JSON in an external model folder.

Do not create these files in external model folders for single-file model/LoRA
source sets:

- `.api.json`
- `.work.json`
- `.workflow.json`
- `.civitai.json`
- `-description.json`
- raw API response JSON under any other name
- repo-specific workflow variants
- temporary conversion files
- local testing artifacts

If raw API JSON is needed while researching a source, use it transiently outside
the external model folder, such as in `/tmp`, then copy only the useful facts
into the `.md` sidecar and save raw source description HTML as `.html`.

## Mandatory Markdown

Every external model/workflow source record must have a Markdown sidecar. A
record describes a source page plus the workflow/reference artifacts and model
files needed to run that source context.

The `.md` is no longer strictly a one-weight sidecar. It may list multiple
weights or supporting model files when the canonical workflow needs them, such
as paired diffusion model branches, LoRAs, VAEs, CLIP/text encoders, or obvious
weight variants.

The `.md` file must start with a fenced `json model_summary` block. Do not use
YAML front matter.

The JSON object must contain:

- `source`: non-empty source URL
- `html`: exact same-folder raw source description/tutorial HTML filename
- `model_files`: non-empty array of paths relative to `/mnt/data/comfyui/models`
  for all model files needed by the canonical workflow or source context
- `workflows`: non-empty array of exact same-folder filenames, or
  `["not_available"]` when no source workflow/reference artifact is available

The JSON object may also contain:

- `applies_to`: array of paths relative to `/mnt/data/comfyui/models` for
  canonical local model files or model-family files this LoRA is intended to be
  used with
- `references`: array of exact same-folder `.png`, `.jpeg`, or `.jpg` filenames
  that visually illustrate a LoRA or model but are not source workflow artifacts

The `source` value must be a URL. Do not point `source` at another local `.md`.

Example:

````md
```json model_summary
{
  "source": "https://civitai.red/models/443821/cyberrealistic-pony?modelVersionId=2884631",
  "html": "cyberrealisticPony_v180Coreshift.html",
  "model_files": [
    "checkpoints/cyberrealisticPony_v180Coreshift.safetensors"
  ],
  "workflows": [
    "cyberrealisticPony_v180Coreshift.png"
  ],
  "applies_to": [],
  "references": []
}
```
````

The `.md` file should include:

- source URL or URLs, matching or expanding on the JSON `source`
- what model files the sidecar describes
- for LoRAs, what the LoRA is for and which base model family it applies to
- what source/reference artifacts are present next to the `.md` record
- whether a source workflow was found
- if a workflow was not found, a clear note saying that no workflow was found
  and what source/reference artifact was kept instead
- important usage information from the source page, such as trigger words,
  model family, recommended settings, or important warnings
- enough context that the model can still be understood if the source page is
  removed

The `.md` should be curated, readable, and useful. It should not be a raw API
dump.

Because the raw source description is preserved in `.html`, avoid duplicating
long overlapping tutorial or description content in the `.md`. The `.md` should
summarize/index the source, point to the raw `.html` for full details, and keep
only the most useful non-overlapping local notes.

## Model Files

The `model_files` array lists the model files used by the canonical workflow or
source context.

Entries must be paths relative to `/mnt/data/comfyui/models`, for example:

- `checkpoints/example.safetensors`
- `diffusion_models/WanVideo/2_2/example.safetensors`
- `loras/example.safetensors`
- `vae/example.safetensors`
- `text_encoders/example.safetensors`

The checker verifies that every listed file exists, but it does not require
those files to live in non-ignored folders. This allows records to document
which CLIP, VAE, text encoder, or upscale model a workflow needs while still
keeping those support folders out of dangling-file checks.

Do not use `not_available` in `model_files`. If a source context is documented,
it must list at least one real model file.

## LoRA Applicability

For LoRA records, `model_files` lists the LoRA file itself.

Use `applies_to` to identify the base model or model-family files the LoRA is
intended for. Entries must be paths relative to `/mnt/data/comfyui/models`.
Prefer the most specific canonical local model file that defines the family or
stage, for example a Wan 2.2 HIGH branch file for a Wan high-noise LoRA.

The readable `.md` body must describe what the LoRA is for, including trigger
words, concept/style/subject, recommended strength, base model family, and other
source guidance when known.

## Visual References

Use `references` for same-folder `.png`, `.jpeg`, or `.jpg` images kept only to
show what a LoRA or model looks like.

Reference images are different from `workflows` entries. A `references` image
does not need embedded ComfyUI workflow metadata or A1111 generation parameters.
If an image is being kept as a source workflow artifact or source generation
metadata artifact, list it in `workflows` instead.

Use an empty `references` array when a LoRA has no saved reference image.

## Raw HTML

Every external model/workflow source record must have a same-folder `.html`
file.

The `.html` should be raw source/API description HTML. Do not clean, rewrite,
restyle, or otherwise modify it unless the user explicitly asks.

The `.html` exists to preserve the raw source description or tutorial when that
content is long enough that copying it into Markdown would be noisy or lossy.

The `.md` JSON block must list the `.html` file in `html`, and the readable
Markdown should mention it.

For Civitai sources, use the API only transiently to extract the raw
description HTML. Do not save the API JSON in the external model folder.

## Source Workflow Preference Order

When preserving source workflow/reference material for a single-file model or
LoRA, use this order of preference:

1. `.png`/`.jpeg`/`.jpg` with embedded workflow metadata
2. `.png`/`.jpeg`/`.jpg` without embedded workflow metadata, plus raw workflow
   as `.json`
3. `.png`/`.jpeg`/`.jpg` without embedded workflow metadata, plus source
   metadata as `.txt`
4. raw workflow `.json` only
5. source metadata `.txt` only

The Markdown sidecar is always required regardless of which source workflow or
metadata artifacts are available.

Every preserved workflow/reference artifact must be listed explicitly in the
`.md` JSON `workflows` array. The checker uses this array as the authority for
which `.png`/`.jpeg`/`.jpg`/`.json`/`.txt` files belong to the model.

If a source image does not contain embedded workflow metadata, it may still be
kept when it is the best available source/reference image. The `.md` must note
that no embedded workflow was found.

If no workflow was found but source generation metadata was found, the metadata
may be saved as `.txt`. The `.md` must note that no workflow was found and that
the `.txt` is source metadata rather than a ComfyUI workflow.

## Raw Workflow JSON Naming

Raw upstream workflow JSON kept in an external model folder must be named with a
plain `.json` extension.

Do not use `.workflow.json`.

This rule applies even if the upstream file or an earlier local copy used a
`.workflow.json` suffix. Rename the external reference copy to `.json`.

## Metadata Text Naming

When source generation metadata is saved because no workflow was found, save it
as a plain `.txt` file.

Do not use `.parameters.txt` or other more specific suffixes.

Existing older files may not all follow this rule yet. When encountered, they
should be renamed to the exact same-stem `.txt` form if they are kept.

## Source Images

Source/reference images may be kept even when they do not contain embedded
workflow metadata.

If an image contains embedded workflow metadata, the external folder should keep
the image. Do not also extract that embedded workflow into a separate external
`.json` just for the external folder. The image is the source artifact.

If an image does not contain embedded workflow metadata, keep it only when it is
the best available source/reference image. Then preserve the workflow or source
metadata separately according to the preference order above.

The `.md` should identify whether the image is:

- a workflow-bearing source image
- a reference/source image without embedded workflow metadata
- another source image kept for context

## Downloadable Raw Workflow JSON

If the upstream source provides a raw downloadable workflow JSON, the external
folder may keep that raw workflow as `.json`.

The external folder stores the raw source reference. It does not need to know or
care whether this repo also stores a runnable reference workflow copied or
adapted from the same upstream workflow.

If the same workflow is later added to this repo, that repo copy is independent
and governed by repo workflow rules.

## Multiple Source Artifacts

Keep only source/reference artifacts that are useful for understanding or
reconstructing use of the model/LoRA.

Do not create extra local derivative artifacts in the external model folder.

When multiple source artifacts are kept, the `.md` must explain what each one
is and why it is present.

## Civitai API Usage

It is acceptable to use the Civitai API to discover source facts, source
description HTML, download URLs, hashes, model metadata, or image metadata.

It is not acceptable to save the raw Civitai API response JSON in the external
model folder.

For Civitai sources:

- save useful human-facing source information in `.md`
- save raw source/API description HTML as `.html`
- optionally save source/reference images as `.png`, `.jpeg`, or `.jpg`
- optionally save raw upstream workflow JSON as `.json`
- optionally save generation metadata as `.txt` when no workflow exists
- never save API response JSON as `.json`

## Hugging Face Repository Exception

Full Hugging Face model repository directories are explicitly outside the
single-file model/LoRA sidecar rules.

Current explicit exception:

- Hunyuan / `HunyuanImage-3.0-Instruct-Distil-NF4-v2`

For these repository-style model directories, files such as JSON configs,
tokenizers, Python files, model indexes, README files, and source reference
subdirectories may be part of the model repository itself. They are allowed
because they are model-repository contents, not sidecars for a single-file
model/LoRA.

Do not use the Hunyuan exception to justify extra files next to ordinary
single-file checkpoints or LoRAs.

## Cleanup Rules

When touching an external single-file model/LoRA source set, remove accidental
files that violate these rules if they are clearly generated metadata dumps or
repo/workflow scratch files.

Examples of files to remove from external single-file model/LoRA folders when
encountered:

- `*.civitai.json`
- `*.api.json`
- `*.work.json`
- `*.workflow.json` when it is a raw workflow reference that should simply be
  renamed to `.json`
- `*-description.json`

Do not delete actual model weight files.

Do not delete source/reference images, raw source `.html`, valid raw source
workflow `.json`, valid metadata `.txt`, or `.md` sidecars unless the user
explicitly asks.

When unsure whether a file is a real source artifact or a generated local
artifact, inspect it first. If still unsure, ask before deleting.

## File Permissions

Do not intentionally create external model-folder sidecars with unusually
restrictive permissions unless the user explicitly asks.

Normal readable file permissions are preferred so the user can open and inspect
the files from the host.

## Summary

For single-file models and LoRAs in `/mnt/data/comfyui/models`, keep only:

- weights
- mandatory `.md`
- mandatory raw `.html`
- optional source/reference image
- optional raw source workflow `.json`
- optional source metadata `.txt`

Never keep raw Civitai API JSON, `.api.json`, `.work.json`, or
`.workflow.json` in the external model folder.

Remember: external model folders preserve upstream/source reference context.
This repo's workflow files are separate local runnable references.
