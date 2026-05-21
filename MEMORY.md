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
