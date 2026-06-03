# Durable Notes

- For Vast instances, the account SSH key `marcin.bogdanski@gmail.com` is the
  user-facing key and should be attached to new instances so Marcin can tunnel
  from his machine normally. Do not give the user `codex-vast-*` key paths; those
  are temporary agent-local keys only. If a temporary key is needed for agent
  access, also ensure the account key is attached.
- If a `sshN.vast.ai` proxy host/port times out, check `vastai ssh-url <id>`;
  Vast may expose a direct public IP/port that works even when the proxy mapping
  is stale or unreachable.
- BigLove/FLUX.2 Klein multi-reference is useful for identity/style transfer and
  simple composition, but experiments showed quality drops as references and
  body-contact complexity increase. One character plus pose/location references
  is more workable than four references; two characters are acceptable for simple
  low-contact activities but explicit multi-body contact, bondage, and unusual
  poses often produce anatomy failures. Prefer HunyuanImage or a structural
  ControlNet-style stage for harder pose/contact transfer.
- Preserve the file-placement split during model documentation: repo
  `workflows/` holds tested workflows that work locally;
  `/mnt/data/comfyui/user/default/workflows/` is live ComfyUI operational state;
  `/mnt/data/comfyui/models/...` holds weights plus sidecar `.md` and original
  source/verification artifacts only. Do not put repo `.work.json` convention
  files in model sidecar folders.
- For Flux/ComfyUI model work, use exact filenames and paths in discussion and
  docs. Avoid shorthand such as "qwen3", "base", "mixed", or "original" unless
  the exact file is defined in the same sentence. Before touching or staging
  model archive files, reread `AGENTS.md` and
  `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md`; the archive stores
  upstream/source reference artifacts only, not adapted control-repo workflows.
- When downloading model weights, prefer the canonical or most popular upstream
  source first, especially when Marcin names or hints at one such as Unsloth.
  Use mirrors/forks only after verifying why the canonical source is unsuitable,
  and record hash/source equivalence if keeping a workflow-compatible local
  filename.
- For ComfyUI Python/custom-node dependencies, make Dockerfile changes and
  rebuild/recreate the affected container instead of relying on packages
  installed into a live container. Live-container installs are acceptable only
  as a temporary diagnosis step and must be reconciled back into the image.
