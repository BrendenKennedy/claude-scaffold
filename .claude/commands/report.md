---
description: >
  Draft a deliverable — technical report, white paper, stakeholder summary, or model card —
  assembled from the repo's own records (project definition, decision log, tracker runs, session
  notes), with every claim traced to evidence and gaps flagged instead of filled in.
argument-hint: [report | whitepaper | stakeholder | model-card] [slug]
---

Draft the deliverable `$1` (default: `report`). **Load the `reporting` skill and follow it** —
skeleton, claim-evidence rule, honesty rules, audience variant. Load `statistics` before writing
any number and `visualization` before referencing any figure.

1. **Gather the evidence, in this order** (read; don't reconstruct from conversation memory):
   - `.claude/memory/process/project-definition.md` + `phase-state.md` — the problem (T1) and how
     far the work actually got (gate history is the honest progress statement).
   - `.claude/memory/process/decision-log.md` + the domain logs in `memory/policy/` — the "why"
     behind every choice the report must explain.
   - The tracker — `mlflow.search_runs(...)` (or the active tracker's equivalent) for the runs,
     metrics, and artifacts that will back each claim; eval reports and figures among the run
     artifacts.
   - `.claude/memory/sessions/` — the narrative arc, dead ends included.
2. **Draft** to `reports/<today>-<$2 or slug-from-title>.md` per the `reporting` skeleton, at the
   depth the audience variant demands. Every quantitative claim cites its run id inline (a
   footnote or bracketed ref); every figure reference names the script or run artifact that
   regenerates it.
3. **The gap pass — the step that keeps this honest.** Re-read the draft hunting for claims with
   no evidence behind them. Each becomes `[TODO: evidence — <what's missing>]`, and the draft
   ends with a **Gaps** list of them. Never fill a gap with a plausible number; an invented
   metric in a credible-looking report is the worst artifact this repo could produce.
4. **Offer the follow-ups, don't assume them:** regenerating missing figures, running the
   missing eval, or (model-card variant) attaching the card to the registry entry
   (`tracking-mlflow`). Recording the draft in the session note happens at `/wrapup` as usual.

Report back: the draft path, the evidence actually used (runs, files), and the gap list.
