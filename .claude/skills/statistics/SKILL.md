---
name: statistics
description: >
  The statistical honesty layer — uncertainty on every reported number and comparisons that mean
  something. Carries: variance from the pipeline itself (≥3 seeds, report mean ± sd — the
  cheapest honest interval), bootstrap CIs on eval metrics (resample the test set), whether the
  test set can even resolve the difference you're claiming (binomial back-of-envelope), comparing
  models properly (same split, paired per-item comparison, improvement vs seed-noise), A/B test
  basics (randomization unit, pre-registered metric + horizon, no peeking without correction),
  and multiple-comparisons discipline (test many slices/ablations and some "wins" are noise —
  correct or replicate). Load when reporting a number, claiming an improvement, comparing runs,
  or designing an A/B test. Triggers: significant, significance, p-value, confidence interval,
  error bars, bootstrap, seed variance, is the difference real, A/B test, hypothesis test,
  sample size, power, multiple comparisons, noise or signal, uncertainty.
---

# statistics — is the difference real?

> On-demand: load this whenever a number is about to be reported or two runs compared. It backs
> `evaluation` (intervals on metrics), `reporting` (claims carry uncertainty), `visualization`
> (error bars), and the P5 gate. The theme: most "improvements" die when you ask two questions —
> *how much does this number move on its own?* and *could this test set even detect the claim?*

## Seed variance first — the cheapest honest interval
Before comparing anything, run the SAME config with ≥3 seeds and report **mean ± sd**. That sd
is the noise floor of your whole pipeline (init, shuffling, augmentation, cuDNN). An
"improvement" smaller than it is not a result — it's a seed. This one habit kills most false
wins and costs three training runs.

## Can the test set resolve the claim?
Back-of-envelope for any proportion-like metric (accuracy, recall@op):
`se ≈ sqrt(p(1-p)/n)`, and the 95% CI is ± ~2·se.
- n=500, p=0.90 → ± 2.7 points. A "1.5-point gain" on that set is **unresolvable**.
- n=5000, p=0.90 → ± 0.85 points.
Run this before celebrating — and before *building* the test set (it's a P1/P2 sizing input:
the metric's target margin dictates n, not the other way around).

## Bootstrap CI on any eval metric
Resample the test set with replacement (~1000×, seeded), recompute the metric, take the 2.5/97.5
percentiles. Works for mAP, F1, calibration error — anything computed per-item. For detection,
resample **images**, not boxes (boxes within an image aren't independent). Report it next to the
point estimate; `visualization` puts it on the figure.

## Comparing two models (the paired trick)
Same split, always. Then compare **per-item**: bootstrap the *difference* on paired predictions,
or McNemar for classifiers — pairing removes shared item-difficulty variance, so it detects real
-but-small gains that unpaired comparison misses. Combine with seed variance: the claim
"B > A" needs the gap to clear BOTH the paired CI and the seed noise floor. Model selection
across many trials (HPO) then confirms on test **once** (`hpo-optuna`'s protocol).

## A/B tests (when the model meets users)
Randomize on the right unit (user, not request, when experiences persist); pre-register metric,
horizon, and n (power analysis before launch, not after); **no peeking** — repeatedly checking
significance until it appears guarantees false positives (use fixed-horizon or sequential
methods, not vibes); randomization-unit ≠ analysis-unit inflates significance (cluster the
errors). The decision at the end goes in the decision log with the numbers.

## Multiple comparisons — the slice-analysis tax
Twenty slices at α=0.05 ⇒ one "significant" regression by luck. When scanning many
slices/ablations/features: correct (Bonferroni for a handful, Benjamini-Hochberg FDR for many)
or treat scan hits as **hypotheses to replicate**, not findings. Error analysis (`evaluation`)
generates leads this way; `reporting` may only print the ones that survive.

## Misuse traps
p=0.04 is not "96% chance it's real"; non-significant ≠ no effect (usually underpowered);
CIs on wildly different n's are not comparable by eyeball; and a metric improved by removing
"outliers" post-hoc is a decision-log entry, not a cleanup.
