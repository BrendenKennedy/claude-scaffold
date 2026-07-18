# Scaffold journal — how the `.claude/` config itself is holding up

The longitudinal record of how the **scaffold** (skills · agents · commands · hooks · the process
docs) performs *in use* — the tooling's own quality signal, kept separate from the project work
(that lives in `sessions/`). This is the data behind the scaffold's meta-loop: the mirror of
`PROCESS.md` Part V, which versions the *methodology* — this versions the *tooling*.

> **Why this exists:** the most valuable dogfooding signal (a skill that didn't surface when it
> should have, an agent handoff that dropped context, a hook that fought you, a command you wished
> existed) is exactly the signal that evaporates — session notes track the project, not the scaffold.
> This file catches it so it becomes a decision instead of a vague memory.

## Capture discipline
- **Log the moment it bites.** When the scaffold helps or hurts mid-session, add a row *now* — same
  rule as the risk register. Reconstructing friction at wrapup loses the specifics.
- **Backstop at wrapup.** The `/wrapup` close-out asks for a scaffold check; "none this session" is a
  valid, common answer. Don't manufacture entries — an empty session is fine.
- **One home.** Scaffold-quality signal lives *here*. Forward feature ideas still go to
  `roadmap.md`; this file is *observed* friction/wins, which `/scaffold-retro` later promotes into
  roadmap/CHANGELOG items.

## Kinds
| Kind | Means |
|---|---|
| `works` | a component clearly helped — a pattern worth keeping or extending |
| `friction` | something was clunky, slow, noisy, or fought the work |
| `coordination` | an inter-component handoff (skill↔skill, agent↔main-session, command↔skill, hook×hook) that worked or didn't — the subtle failure mode |
| `missing` | a wished-for skill / command / hook / doc that doesn't exist |
| `improved` | a shipped change that resolved a prior entry (ties friction → the version that fixed it) |

## Themes / recurring
_Maintained by `/scaffold-retro`: clusters of open entries that keep recurring = what to build or
fix next. Empty until the first retro._

_None yet._

## Log
_Newest-last. Keep cells terse; `Status` is `open` or `resolved (vX.Y / commit)`._

| Date | Kind | Component(s) | Observation | Proposed action | Status |
|------|------|--------------|-------------|-----------------|--------|
| 2026-07-18 | coordination | `/wrapup` × `memory` skill | The wrapup command restates the memory skill's step list, so adding the scaffold-check step meant editing *both* — they can silently drift. It's a deliberate tension (the skill says "don't reconstruct from context", hence the restatement). | Watch for real drift; if it bites, make `/wrapup` reference the skill's numbered steps instead of copying them. | open |
| 2026-07-18 | works | `check-scaffold.sh` (drift + reference checks) | While adding `/scaffold-retro`, the drift check forced it into CLAUDE.md + README and the reference check caught the stale REFERENCE.md — doc/territory consistency held automatically during the loop's own construction. | Keep; pattern worth relying on when adding any command/skill/agent. | open |
