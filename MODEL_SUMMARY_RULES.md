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
- an optional raw source description page, `.html`
- an optional source/reference image, `.png`, `.jpeg`, or `.jpg`
- an optional raw upstream workflow, `.json`
- an optional source metadata text file, `.txt`

No other companion/reference file types should be created in external model
folders for single-file model/LoRA source sets unless the user explicitly asks
for that specific file.

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
into the `.md` sidecar and/or save raw source description HTML as `.html`.

## Mandatory Markdown

Every external single-file model/LoRA source set must have a Markdown sidecar.

The `.md` file should include:

- source URL or URLs
- what weight file the sidecar describes
- what source/reference artifacts are present next to the weight file
- whether a source workflow was found
- if a workflow was not found, a clear note saying that no workflow was found
  and what source/reference artifact was kept instead
- important usage information from the source page, such as trigger words,
  model family, recommended settings, or important warnings
- enough context that the model can still be understood if the source page is
  removed

The `.md` should be curated, readable, and useful. It should not be a raw API
dump.

If no `.html` is saved, preserve as much useful information from the source page
or API description as feasible in the `.md`.

If `.html` is saved, avoid duplicating long overlapping tutorial or description
content in the `.md`. In that case, the `.md` should summarize/index the source,
point to the raw `.html` for full details, and keep only the most useful
non-overlapping local notes.

## Raw HTML

The `.html` file is optional.

When present, it should be raw source/API description HTML. Do not clean,
rewrite, restyle, or otherwise modify it unless the user explicitly asks.

The `.html` exists to preserve the raw source description or tutorial when that
content is long enough that copying it into Markdown would be noisy or lossy.

The `.md` should mention the `.html` file when it exists.

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

Do not use `.parameters.txt` or other more specific suffixes for future files.

Existing older files may not all follow this rule, but new work should.

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
- optionally save raw source/API description HTML as `.html`
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
- optional raw `.html`
- optional source/reference image
- optional raw source workflow `.json`
- optional source metadata `.txt`

Never keep raw Civitai API JSON, `.api.json`, `.work.json`, or
`.workflow.json` in the external model folder.

Remember: external model folders preserve upstream/source reference context.
This repo's workflow files are separate local runnable references.
