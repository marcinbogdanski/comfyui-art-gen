# Durable Notes

- For Vast instances, the account SSH key `marcin.bogdanski@gmail.com` is the
  user-facing key and should be attached to new instances so Marcin can tunnel
  from his machine normally. Do not give the user `codex-vast-*` key paths; those
  are temporary agent-local keys only. If a temporary key is needed for agent
  access, also ensure the account key is attached.
- If a `sshN.vast.ai` proxy host/port times out, check `vastai ssh-url <id>`;
  Vast may expose a direct public IP/port that works even when the proxy mapping
  is stale or unreachable.
