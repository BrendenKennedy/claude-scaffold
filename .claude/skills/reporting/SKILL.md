---
name: reporting
description: >
  Turning finished work into deliverables — technical reports, white papers, stakeholder
  summaries, model cards — grounded in the repo's own records. Carries: the report skeleton
  (problem → data → methods → results-with-uncertainty → limitations → reproducibility appendix),
  the claim-evidence rule (every number traces to a run id + config + data version; every figure
  regenerable from a script), honest-results discipline (negative results and failure modes
  reported; no cherry-picked seeds or slices), audience layering (one-page executive summary in
  decision language up front, technical depth behind it), model cards, and where the raw material
  already lives (project-definition, decision log, tracker runs, session notes). Load when
  drafting a report, white paper, results section, model card, or stakeholder update — `/report`
  runs the assembly. Triggers: report, white paper, writeup, write it up, executive summary,
  stakeholder summary, model card, deliverable, presentation, document the results, draft the
  paper, results section.
---

# reporting — deliverables with provenance

> On-demand: load this when work becomes a document. The scaffold's records are the source
> material — a report here is **assembled from evidence, not recalled from memory**: the problem
> statement is T1, the "why we did X" is the decision log, the numbers are tracker runs, the
> journey is the session notes. Uncertainty language comes from `statistics`; figures from
> `visualization`; model-card requirements from `model-governance` (via `governance`).

## The skeleton (every deliverable is a subset of this)
1. **Executive summary** — one page, decision language: what was built, the headline result *with
   its interval*, what it means for the consumer named in T1, what's recommended next. Written
   last, placed first, readable by someone who reads nothing else.
2. **Problem** — from `project-definition.md` (T1): target, consumer, success metric + baseline,
   constraints. Don't rewrite it; the report inherits it.
3. **Data** — source, license, versions (dataset manifest), splits and WHY they're leakage-safe,
   label provenance + measured error rate (`annotation`), known biases.
4. **Methods** — what was tried, including what failed (the experiment log is the outline);
   final configs by reference, not prose-copies.
5. **Results** — vs EVERY baseline from T1, with uncertainty (`statistics`), per-slice where it
   matters, calibration if probabilities ship. Figures follow `visualization`; each caption
   names its data + run.
6. **Limitations & failure modes** — mandatory, from the error analysis: where it fails, on
   what slices, what it must not be used for. A report without this section is marketing.
7. **Reproducibility appendix** — commit SHA, data versions, env (uv.lock), run ids, the
   one-command rerun.

## The claim-evidence rule (what makes it a report, not a story)
Every quantitative claim carries a traceable source: `run id` (tracker) + config + data version.
Every figure is regenerable from a script in the repo. Drafting discipline: **a claim with no
run behind it becomes a `[TODO: evidence]`, never a plausible number** — the gap list at the end
of a draft is a feature, not an embarrassment.

## Honesty rules
- Report the **mean over seeds, not the best seed** — with the sd (`statistics`).
- Negative results and dead ends get a subsection — they're paid-for information, and their
  absence is what makes readers distrust the positives.
- Slice results survived multiple-comparisons discipline before printing.
- Baselines appear even when — especially when — the gap is small.

## Audience variants (same evidence, different depth)
**Stakeholder update:** executive summary + one figure + asks/decisions needed; no methods.
**Technical report / white paper:** the full skeleton; lineage vocabulary from PROCESS.md Part I
reads well here. **Model card:** intended use, training data, metrics + slices, limits, contacts
— per `model-governance`; required before a registry alias moves. **README results section:**
headline + reproduce-command + link to the full report.

## Where drafts live
`reports/YYYY-MM-DD-<slug>.md` in-repo (regenerable figures beside it or via tracker links);
the session note links to it; shipping one is P6 gate evidence.
