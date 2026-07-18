---
description: >
  Assess how the `.claude/` scaffold itself is performing — read the scaffold journal, cluster
  recurring friction/wins/gaps into themes, and with the user promote the ones worth acting on into
  roadmap/CHANGELOG items. The scaffold's meta-loop (mirror of PROCESS.md Part V), run periodically —
  at a release boundary or every several sessions, not per-session.
argument-hint: [optional focus e.g. hooks, coordination]
---

Run a **scaffold retrospective** — turn accumulated dogfooding signal into decisions about the
tooling. This assesses the `.claude/` config (skills · agents · commands · hooks · process docs),
not the data-science project. It **proposes, the user decides** — like `/gate`, it does not act
unilaterally.

1. **Load the signal.** Read `@.claude/memory/scaffold-journal.md` (the observed record),
   `@.claude/memory/roadmap.md` (existing backlog — don't duplicate), and the `[Unreleased]` section
   of `@CHANGELOG.md` (what's already queued to ship). If `$ARGUMENTS` names a focus (e.g. `hooks`,
   `coordination`), scope the retro to entries touching it.

2. **Cluster into themes.** Group the journal's **open** entries by what they're really about — a
   component, a workflow seam, a recurring coordination failure. A theme is a pattern across ≥2
   entries *or* a single high-severity one. Name what keeps recurring; that is the signal. Note any
   `works` entries too — patterns worth extending are as actionable as friction.

3. **Propose an action per theme**, each as exactly one of:
   - **Fix now** — a concrete scaffold change (which file, what edit). Small + clear → offer to do it
     in this session on a branch.
   - **Roadmap it** — larger or lower-priority → a `roadmap.md` line.
   - **Leave it** — with a one-line reason (accepted friction, too rare, by-design). Recorded so it
     isn't re-litigated.
   Cross-check against the roadmap/CHANGELOG so nothing is proposed twice.

4. **Decide with the user.** Walk the proposals; the user picks Fix / Roadmap / Leave for each.
   Don't promote on your own judgment — this is the human-in-the-loop step the architecture depends on.

5. **Record the outcome:**
   - Chosen **fixes** applied this session → mark those journal entries `resolved (vX.Y / commit)` and
     add a `CHANGELOG.md` `[Unreleased]` line; an `improved` journal row may capture the resolution.
   - Chosen **roadmap** items → add to `roadmap.md`, and note the journal entry as promoted (still
     `open` until shipped).
   - **Leave** decisions → annotate the entry with the reason; keep it, don't delete.
   - Refresh the journal's **Themes / recurring** section to the current clustering.

6. **Report:** themes found, actions taken vs. deferred, and the trail of `friction → improved` (what
   the scaffold has fixed about itself since the last retro — the "self-improving" ledger).

Keep it proportionate: a handful of themes, terse proposals. An empty or thin journal → say so and
stop; there's nothing to retro yet.
