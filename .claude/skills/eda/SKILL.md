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
  sanity check the data, data quality, what's in this dataset.
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

## Image-data EDA (the CV lane's version)
Random **sample grids** per class/source (look at the actual pixels — metadata lies), size /
aspect / brightness / blur distributions (a resolution cluster = a different camera = a group
key), label overlays on samples (boxes/masks rendered — catches format bugs before training
does), and near-duplicate frames from video (group-split territory).

## Where findings go
Each finding lands where it acts: quality issues → P2 data-quality notes; threats to validity →
risk register (T4); feature ideas + their causal story → feature dictionary (T5); split
constraints (groups, time order) → `datasets`' split manifest design; anything gate-relevant →
it IS the P2 gate evidence. The notebook is scratch; the record is the deliverable.
