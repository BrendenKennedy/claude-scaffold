# templates — delivery files for the TARGET project

These are not scaffold config — they're starter files for the *project being scaffolded*.
`/bootstrap` (§3d) copies the delivery rows below to their destinations and fills the marked slots
(never-clobber applies). `aws-iam-policy.json` is the exception: the `infra-aws` lane consumes it at
role-setup time — the human reviews and attaches it; nothing copies it automatically.

| Template | Destination in the target | What it is |
|---|---|---|
| `dot-env.example` | `.env.example` | the env vars the entry points read (copy to `.env`, fill in; synced with the resource matrix) |
| `pre-commit-config.yaml` | `.pre-commit-config.yaml` | ruff + nbstripout + gitleaks on human commits (`uvx pre-commit install`) |
| `project-ci.yml` | `.github/workflows/ci.yml` | offline tier in CI: uv sync --frozen → ruff → pytest |
| `aws-iam-policy.json` | (not copied — attached in AWS by the human) | least-privilege starter policy for the `claude-for-datascience` role (`infra-aws` skill) |
