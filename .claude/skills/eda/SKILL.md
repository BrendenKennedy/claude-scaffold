---
name: eda
description: >
  Exploratory data analysis with discipline — understand the data before modeling it, without
  spending the test set. Carries: the first-look checklist (schema/dtypes, missingness pattern,
  duplicates + near-duplicates, ranges/units, class balance, per-group counts, target
  relationship), split-aware EDA (split first; modeling decisions come from TRAIN only),
  leakage-hunting during EDA (suspiciously predictive features, IDs that encode the label),
  image-data EDA (sample grids, size/brightness distributions, label overlays), and the rule that
  unrecorded findings get re-discovered — EDA feeds P2's data-quality notes, the risk register,
  and the feature dictionary. Load at P2/P3 before any modeling, or whenever the data smells
  wrong. Triggers: EDA, explore the data, exploratory analysis, first look, profile the data,
  missingness, distributions, outliers, duplicates, class balance, correlation, look at the data,
  sanity check the data, data quality, what's in this dataset, predictive signal, signal screen,
  is there enough signal, single-feature AUC, mutual information, go/no-go before modeling.
---

# eda — looking at the data before trusting it

> On-demand: load this before modeling starts (P2/P3) or when results smell wrong late. Medium:
> `notebooks` (thin, promoted). Split mechanics: `datasets`. Charts: `visualization`. The
> deliverable is **written findings**, not a scrolled-past notebook — EDA that isn't recorded in
> P2's data-quality notes / risk register gets silently redone by the next person (or you).

## The split-aware rule (EDA's own leakage mode)
A one-time *audit* of the full dataset (schema, corruption, counts, licensing red flags) is fine
and necessary. But once exploration starts informing **modeling decisions** — features to build,
transforms, thresholds, what to exclude — do it on **train only**, post-split. Patterns you
"discovered" on the full set were partly discovered on your test set, and the eval quietly
inflates. If the split doesn't exist yet, make it first (`datasets`) — EDA is not a reason to
delay the split; it's the reason to hurry it.

## First-look checklist (run it all; surprises live in the boring ones)
- **Schema & units:** dtypes as expected; numeric-as-string; timezone/units declared or guessed;
  categorical cardinality (a 10k-level "category" is an ID, not a feature).
- **Missingness:** rate per column AND pattern — missing-at-random vs structurally missing
  (only for one site/period/class). The pattern is a feature or a bug; the rate alone says neither.
- **Duplicates + near-duplicates:** exact dupes, same-entity rows, and (images) perceptual
  near-dups — these silently straddle splits later; flag them to `datasets` for group-splitting.
- **Ranges & impossible values:** negatives where impossible, sentinel values (-999, 1970-01-01,
  0 meaning null), unit mixups (a bimodal distribution is often two units).
- **Class balance & per-group counts:** per class, per site/source/period. Groups with a handful
  of samples will be invisible in aggregates and broken in slices — log them as risks now.
- **Target relationship (train only):** per-class feature distributions, correlations. Anything
  *too* predictive is a leakage suspect before it's a discovery — ask "would this exist at
  prediction time?" (an ID range, a timestamp, an admin field set after the outcome).

## The predictive-signal screen (go/no-go before the modeling spend)
Data quality and quantity are necessary, not sufficient — a clean, big dataset can still carry no
learnable signal for your target. Before P4 feature engineering and the P5 modeling sweep are
funded, run a **cheap, train-only screen** and write down a go/no-go: *is there enough signal here
to justify the spend?* This is the check that would have saved the dogfood project a full modeling
pass (it confirmed a near-random ceiling *late*, after P4/P5, when a screen at P3 would have caught
it — see the scaffold journal).

Run it on **train only** (post-split; a screen on the full set spends your test set):
- **Single-feature strength vs the target:** univariate AUC / mutual information per candidate
  feature (classification), or per-feature correlation / MI (regression). A slate where the *best*
  single feature barely clears chance is a loud warning.
- **A quick multivariate read:** a cross-validated logistic/linear or a shallow gradient-boosting
  model on the raw candidate columns — not to tune, just to see whether *combined* signal clears
  the trivial baseline (`datasets`' base-rate / naive forecast) by a margin the success metric can
  actually use.
- **State the ceiling honestly.** Compare that margin against the threshold the P1 success metric
  needs, and against `statistics`' "can the test set even resolve this difference?" back-of-envelope.

Two failure modes this screen does **not** catch — name them so it isn't oversold: (1) an
adversarially-balanced target (signal drained by design, e.g. counter-picked drafts), and (2)
distribution shift across the split (a feature strong in-sample that collapses out-of-period). Those
surface at the **baseline** step, which is the true signal test — so a weak screen is a stop-and-
rethink, but a strong screen is *not* a green light to skip disciplined baselines.

## Image-data EDA (the CV lane's version)
Random **sample grids** per class/source (look at the actual pixels — metadata lies), size /
aspect / brightness / blur distributions (a resolution cluster = a different camera = a group
key), label overlays on samples (boxes/masks rendered — catches format bugs before training
does), and near-duplicate frames from video (group-split territory).

## Where findings go
Each finding lands where it acts: quality issues → P2 data-quality notes; threats to validity →
risk register (T4); feature ideas + their causal story → feature dictionary (T5); split
constraints (groups, time order) → `datasets`' split manifest design; the predictive-signal
screen's go/no-go → the **P3 exit gate** (the chokepoint before P4/P5 spend); anything else
gate-relevant → it IS the P2 gate evidence. The notebook is scratch; the record is the deliverable.
