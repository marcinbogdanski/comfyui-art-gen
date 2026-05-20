# Agent Notes

This repo manages a Docker-based ComfyUI server for host `x399`.

Operational preferences:

- Use manual `docker run --rm -it` via `./run_comfyui.sh`; do not introduce Docker Compose unless requested.
- Do not install CUDA Toolkit, PyTorch, ComfyUI, or model dependencies on the host.
- Persistent ComfyUI data lives under `/mnt/data/comfyui`.
- Keep model files out of git; document model download commands instead.
- Default access URL is `http://x399.lan:8188/`.
- Start with one GPU per ComfyUI instance; default wrapper uses GPU 0.
- Do not expose ComfyUI directly to the public internet.

Image setup:

- Base image is the official PyTorch CUDA runtime image.
- Switch from `runtime` to `devel` only if custom nodes need native/CUDA compilation.

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
- Do not duplicate details that are already captured in committed docs, scripts, workflows, or git history; reference the relevant repo file instead.
- Do not restate technical findings, settings, file lists, commands, or implementation details that are already captured in committed repo files or git history.
- Put durable process lessons or stable operating rules in the repo proper, such as `AGENTS.md`, `MEMORY.md`, model docs, or scripts — not in dated entries.
- Prefer appending sections to the end of the current memory file, unless cleanup or structure clearly requires insertion elsewhere.

## Tools

### GitHub CLI

- The `gh` CLI is available and pre-authenticated for agent access.
- GitHub permissions are scoped to selected repositories.
- Do not force-push or delete the main branch.
