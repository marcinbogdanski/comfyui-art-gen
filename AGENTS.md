# Agent Notes

This repo manages a Docker-based ComfyUI server for host `x399`.

## Asking questions

- Never use any "ask the user a question" interactive/modal tool, whatever it is
  called in the current harness (e.g. `AskUserQuestion` and any renamed or
  equivalent successor). Always ask questions as plain text in the chat instead.

Operational preferences:

- Use manual `docker run --rm -it` via `./run_comfyui.sh`; do not introduce Docker Compose unless requested.
- Do not install CUDA Toolkit, PyTorch, ComfyUI, or model dependencies on the host.
- Persistent ComfyUI data lives under `/mnt/data/comfyui`.
- Keep model files out of git; document model download commands instead.
- Hugging Face and Civitai API credentials may be available from `~/.bashrc`
  (`HF_TOKEN` and `CIVITAI_API_KEY`). Source that file when authenticated model
  or source-metadata downloads are needed, but never print or commit token
  values.
- If an authenticated Hugging Face download fails because the token/account has
  not accepted a model license, gated terms, or access agreement, stop and ask
  the human to accept access. Provide the exact model page link and do not treat
  the missing file as a final blocker until the human has had a chance to accept
  the license.
- When searching for models or LoRAs, choose sources in this order:
  1. A link explicitly provided by the user.
  2. The most official or most popular upstream source.
  3. Other mirrors, forks, or reuploads only when the above are unavailable or
     unsuitable, and document why.
- Default access URL is `http://x399.lan:8188/`.
- Start with one GPU per ComfyUI instance; the local wrapper uses watercooled
  GPU 1 for ComfyUI. The local llama.cpp wrapper uses watercooled GPU 3.
- Do not expose ComfyUI directly to the public internet.
- Before creating, renaming, or cleaning sidecar/reference files under
  `/mnt/data/comfyui/models`, read
  `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md` and
  `/mnt/data/comfyui/models/MODEL_SUMMARY.md`. The rules file is authoritative
  policy; the summary file records current archive state. Those external
  model-folder rules are separate from this repo's workflow rules.
- After staging model-archive changes and before asking the human for review or
  committing, re-read `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md` and
  execute its staged changes checklist against the staged/index version of the
  files.
- Workflow `.work.json` files are local GUI work copies. It is fine to create
  or sync them in the working tree when requested, but do not stage, force-add,
  track, or commit `.work.json` files unless the user explicitly asks to track
  the `.work.json` file itself. Phrases such as "stage related files" or
  "commit the workflow" mean the canonical no-suffix workflow files and docs,
  not ignored `.work.json` copies.
- When adding a new model or LoRA with a reproducible reference workflow, first
  read `models/ADDING_MODEL_OR_LORA.md` and confirm the plan before downloading
  or editing files, unless the user has already provided an explicit plan.

Image setup:

- Base image is the official PyTorch CUDA runtime image.
- Switch from `runtime` to `devel` only if custom nodes need native/CUDA compilation.
- Permanent Python/custom-node dependencies belong in the Dockerfile and must be
  tested by rebuilding the image and restarting/recreating the affected
  container. Installing into a running container is allowed for quick diagnosis
  or smoke tests, but reconcile successful dependency changes back into the
  Dockerfile.

## Memory files

This is your memory system. By agents for agents. Use to maintain continuity. Major items only.

- If present, read `MEMORY.md` and recent `memory/YYYY-MM-DD.md` entries for session continuity.
- `MEMORY.md`, if present, is for durable cross-session context and repo-level decisions that do not belong in a more specific repo doc. It is not the authoritative store for domain facts the repo already tracks elsewhere.
- `memory/YYYY-MM-DD.md` is a compact executive progress journal: major work only, what changed, what worked or failed, important decisions, and likely next steps.
- Use the human/logical day, not strict midnight, when naming entries; if work happens after midnight but before Marcin sleeps, use the previous calendar date.
- Cadence is event-driven, not daily. No entry is required on quiet days, and multiple entries in one day are fine when separate work warrants it.
- Write dated memory files only after a meaningful work task is completed (like merged PR) or when the user indicates end of day.
- Keep dated memory entries very compact: they should read like an executive summary for major and relevant work items, not a detailed work log.
- Record only material context that helps future agents regain continuity: what was tried, what worked or failed, important decisions, and likely next steps.
- When capturing memory after a long session, check recent git history in this repo and the model archive repo so the summary covers the actual committed models, workflows, and docs, not just the latest topic discussed.
- Do not duplicate details that are already captured in committed docs, scripts, workflows, or git history; reference the relevant repo file instead.
- Do not restate technical findings, settings, file lists, commands, or implementation details that are already captured in committed repo files or git history.
- Put durable process lessons or stable operating rules in the repo proper, such as `AGENTS.md`, `MEMORY.md`, model docs, or scripts — not in dated entries.
- Prefer appending sections to the end of the current memory file, unless cleanup or structure clearly requires insertion elsewhere.

## Tools

### GitHub CLI

- The `gh` CLI is available and pre-authenticated for agent access.
- GitHub permissions are scoped to selected repositories.
- Do not force-push or delete the main branch.
