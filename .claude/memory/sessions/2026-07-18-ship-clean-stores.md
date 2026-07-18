# Session: Ship clean memory stores (stop leaking dev content to consumers)

**Date:** 2026-07-18 · **Focus:** stop `install.sh` from shipping this repo's own memory content into fresh projects

## Summary
User flagged that committed session notes / memory "would confuse people." Investigation surfaced a
bigger problem than committing: `install.sh` copied *this repo's* dated session notes, dev roadmap
(release history), and scaffold-journal entries into every installed project. Fixed the shipping so a
fresh project gets **empty stores**; kept this repo's dev memory committed (user's choice — dogfooding
+ `/wrapup` depend on it). Personal `~/.claude` memory was never in scope (lives outside the repo).

## Changes & artifacts
- `.claude/templates/memory/roadmap.md`, `.claude/templates/memory/scaffold-journal.md` — **new**
  blank store templates (structure only).
- `install.sh` — excludes this repo's memory instance content (dated `sessions/[0-9]*`, live
  `roadmap.md`, live `scaffold-journal.md`) from the copy; seeds the blank roadmap + journal from the
  templates (never-clobber preserved). Exclusion globs anchored to `*/.claude/memory/…` so they don't
  also catch `templates/memory/…`.
- `.claude/scripts/check-scaffold.sh` — INSTALL file-count check reconciled: excludes dated notes
  from `src_count` (roadmap/journal exclude+reseed cancels 1:1); comment explains the reconciliation.
- `.claude/templates/README.md`, `CHANGELOG.md` — recorded the behavior (a Fixed entry).

## Key decisions
- **Keep this repo's dev memory committed; fix shipping only** — dev record + `/wrapup` commit step
  stay intact; consumers just stop receiving it.
- **Seed blanks from templates, not heredocs** — real editable files, no bash-escaping of markdown.
- **What ships vs. not:** structure ships (`process/` templates, `reference/` docs, `policy/` canon,
  session README+template, blank roadmap/journal); instance content doesn't (dated notes, dev
  roadmap/journal content).

## State
- Works now: all 7 `check-scaffold` checks pass; **verified by real install into a temp dir** —
  consumer gets blank roadmap (0 dev-history lines), empty journal, 0 dated notes; process/reference/
  policy still ship.
- **Process phase:** not started (scaffold-dev work) · **gate debt:** none.
- Known gap: blank templates' headers must stay in sync with the live stores' headers if the store
  format changes — noted in `templates/README.md`; a `/scaffold-retro`-catchable drift risk.

## Follow-ups
- If the store format ever changes, update both the live file and its `templates/memory/` blank → ../roadmap.md

- Branch: `ship-clean-stores` · commit `c42ea74`

## Related
- Completes the pre-dogfooding trilogy: [session-start-orientation](2026-07-18-session-start-orientation.md)
  (orientation in) → [scaffold-self-assessment-loop](2026-07-18-scaffold-self-assessment-loop.md)
  (capture/assess) → this (don't leak dev memory to consumers)
