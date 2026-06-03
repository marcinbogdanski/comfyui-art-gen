# Claude CLI Sub-Agent Notes

Do not use this file unless the human explicitly points an agent to it.

## Gate

- Do not run the `claude` CLI unless the human explicitly says:
  `Use Claude CLI as subagent`.
- A general request for review, validation, audit, a second opinion, or a
  sub-agent does not authorize Claude CLI use. Use the current harness's normal
  sub-agent mechanism instead.

## Invocation

- Before relying on Claude CLI in a new session, run `claude --help` and verify
  the local flags; CLI behavior can change.
- Use noninteractive print mode with live progress for Claude CLI checks:

  ```bash
  claude --print --verbose --output-format stream-json \
    --include-partial-messages \
    --dangerously-skip-permissions \
    < /tmp/review-prompt.txt
  ```

- `--add-dir /mnt/data/comfyui/models` is not needed when using
  `--dangerously-skip-permissions`; use `--add-dir` only for permission-checked
  runs where Claude needs to inspect the companion model archive repo from this
  control repo.
- Put the review instructions in a prompt file under `/tmp` and make the prompt
  explicitly audit-only: do not edit, write, stage, unstage, commit, delete, or
  clean files.

## Audit Prompt Shape

- For model or LoRA readiness audits, ask Claude to start from the repo roots,
  read this repo's `AGENTS.md` and the companion archive's
  `/mnt/data/comfyui/models/MODEL_SUMMARY_RULES.md` and
  `/mnt/data/comfyui/models/MODEL_SUMMARY.md`, then discover the changed,
  staged, unstaged, and untracked scope itself with `git -C ... status` and
  diffs. Do not give Claude a curated file list to merely confirm.
- In those Claude review prompts, explicitly demand extreme attention to detail:
  every filename, repo boundary, sidecar reference, staged file, untracked file,
  and instruction source must be checked literally, not skimmed or assumed.
- Use `--output-format stream-json` for Claude CLI checks so progress is visible
  while the check runs. It requires `--verbose` and produces noisy output;
  summarize the final verdict back to the human.
- Avoid asking Claude to run shell commands via `cd ... && ...` when permissions
  are not bypassed. Prefer `git -C /path ...` in prompts and allowed-tool
  patterns.
- If Claude is being used because the human requested an independent check, do
  not narrow the prompt to only the already-staged files. Ask it to verify both
  the staged file set and the surrounding unstaged/untracked state so it can
  catch over-staging or missed related files.
