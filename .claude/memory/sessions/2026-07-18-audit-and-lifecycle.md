# Session: Final audit + the 1.0 runway (v0.8.0 → v0.11.0)

**Date:** 2026-07-18 · **Focus:** infrastructure lanes, adversarially-verified audit, upgrade lifecycle

## Summary
Third arc of the day (same conversation as the process/efficiency and comprehensiveness arcs).
Shipped the infrastructure story both directions (AWS behind a least-privilege IAM boundary;
self-hosted twins via MinIO/CVAT/Postgres), the resource matrix, then ran a 58-agent
adversarially-verified audit (45 findings, 0 refuted, all fixed) and built the 1.0 runway:
`/upgrade`, checker hardening, the stability contract. Next step is the user's: dogfooding.

## Changes & artifacts
- **v0.8.0** — `infra-aws` (S3+Redshift; starter IAM policy with self-widening structurally
  denied; first-time setup walkthrough with human/agent split), `containers` (Docker/Compose;
  k8s parked), validate-bash A6/A7 tiers, security-canon cloud section
- **v0.9.0** — `local-stack` (MinIO endpoint-url twins, CVAT pinned+shared-storage, Postgres
  init-script reproducibility, pgvector/Timescale/PostGIS/AGE matrix)
- **Resource matrix** — `memory/process/resources.md`; provisioning updates matrix +
  `.env.example` same-commit; CVAT and DVC share one recorded MinIO bucket
- **v0.10.0** — the audit pass: 11 dimensions, 58 agents, 45 confirmed findings fixed (two
  invalid YAML frontmatters, escaped home-wipe patterns in B1, leakage-hook exit-5 false
  positive, missing `.env` in shipped .gitignore, ~35 staleness/contradiction items); tags
  v0.4–v0.9 re-created annotated
- **v0.11.0** — `/upgrade` (stamp→CHANGELOG delta, three-way add/replace-unmodified/ask-on-
  edited, state never clobbered), check-scaffold 2b (YAML validity + 1,536 budget +
  delisting, negative-tested), stability contract in CONTRIBUTING

## Key decisions
- Cloud boundary = IAM policy the agent cannot widen (Deny iam:*), not prompt-trust
- K8s parked; Compose covers support services at this scaffold's scale
- Resource matrix lives in memory/process/ (data), not policy/ (governance doctrine)
- 1.0 gate = a real project shipped through the scaffold, not more features

## State
- `main` at v0.11.0, tags annotated v0.1→v0.11, GitHub releases current, all checks green
  (incl. new 2b), tree clean and synced

## Follow-ups
- **Dogfooding begins** (user-driven): first real project through `/setup` → gates → `/report`;
  its retro produces PROCESS.md 0.3.0 and the real README walkthrough → 1.0
- Multi-archetype `/bootstrap` skeletons in 1.x (tabular cheapest first) → `../roadmap.md`

## Related
- [2026-07-18-process-and-efficiency](2026-07-18-process-and-efficiency.md) ·
  [2026-07-18-comprehensiveness-releases](2026-07-18-comprehensiveness-releases.md)
