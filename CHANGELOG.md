# Changelog

All notable changes to claude-scaffold. Format follows [Keep a Changelog](https://keepachangelog.com/);
versions follow [SemVer](https://semver.org/). Installed projects can compare their
`.claude/scaffold-version` stamp against these entries to see what they're missing.

## [Unreleased]

### Fixed
- `install.sh` no longer ships stray `__pycache__/*.pyc` from a dirty working tree; the file filter
  is mirrored in `check-scaffold.sh` so a future mismatch fails CI.
- `settings.json` `permissions.allow` now covers what `/wrapup` (commit/branch/merge) and
  `/bootstrap` (uv, pytest, ruff) actually run — the two headline flows no longer prompt per step.
- CLAUDE.md no longer implies `.mcp.json` ships with the scaffold.

### Changed
- README front door: plain-language problem statement, prerequisites, badges, a lifecycle diagram,
  a **Daily usage** section (skills auto-surfacing, `/review`, `/wrapup`), the post-`/bootstrap`
  project tree, and a Troubleshooting section.
- Skill-tier vocabulary settled everywhere: two tiers (always-on / tool-gated); the always-on tier
  has two groups, chassis (process) and workflow (CV/DS domain).

## [0.1.0] — 2026-07-14

First tagged release.

### Added
- The CV/DS `.claude/` scaffold: two-tier skills (chassis + workflow always on; tool skills gated by
  `skillOverrides`), five subagents, governance canon, session memory.
- `/intake` (stack) + `/bootstrap` (shape) one-time onboarding, including anomaly-detection
  ("fit-not-trained") and multi-stage-pipeline skeletons.
- `install.sh` — never-clobber drop-in installer; stamps `.claude/scaffold-version` into targets.
- CI: `check-scaffold.sh` self-consistency suite (docs↔disk drift, frontmatter, hook wiring,
  install idempotency) + shellcheck.
- MIT license.
