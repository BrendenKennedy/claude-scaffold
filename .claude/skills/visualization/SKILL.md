---
name: visualization
description: >
  Charts that inform instead of mislead — for EDA, training diagnostics, and deliverables.
  Carries: chart-for-question mapping (distribution → histogram/ECDF; comparison → dot plot or
  bars-from-zero; relationship → scatter + trend; trend → line; almost never pie), the honesty
  rules (bar axes start at zero, shared axes across compared panels, error bars or intervals on
  every estimate, n stated on the figure), perceptual rules (viridis-family colormaps — never
  jet/rainbow; colorblind-safe categorical palettes; log scales labeled), figures-as-code
  (scripted + seeded, saved as tracker artifacts — no hand-tweaked screenshots), and the standard
  diagnostics set (learning curves, PR/calibration curves, confusion matrices, residuals,
  worst-case prediction grids). Load before making any figure. Triggers: plot, chart, figure,
  graph, visualize, matplotlib, seaborn, histogram, scatter, heatmap, colormap, colorblind,
  error bars, learning curve, plot the results, make a figure.
---

# visualization — figures that carry evidence

> On-demand: load this before writing plotting code. Figures here are *artifacts of record* —
> they land in the tracker, reports (`reporting`), and error analyses (`evaluation`) — so they
> follow the same reproducibility rules as any result. Uncertainty shown on figures comes from
> `statistics`.

## Chart follows question
| Question | Reach for | Not |
|---|---|---|
| How is X distributed? | histogram (+ ECDF when comparing) | a bar of the mean — it hides everything |
| Is A bigger than B? | dot plot with intervals; bars **from zero** | truncated-axis bars |
| How do X and Y relate? | scatter (+ trend, density for large n) | dual-axis line charts |
| How did it change over training/time? | line, one series per run | stacked anything for >4 series |
| Where does the model fail? | confusion matrix, PR curve, per-slice dot plot, worst-case image grid | a single aggregate number |
Composition with >3 parts: sorted horizontal bars, not pie.

## Honesty rules (the figure IS a claim)
- **Bars start at zero.** Zoomed comparisons use dot plots with intervals instead — showing the
  interval is the honest way to magnify.
- **Compared panels share axes.** Two panels with different y-scales is how "identical" reads as
  "improved."
- **Every point estimate carries its uncertainty** — error bars / bands / n, from `statistics`
  (seed variance or bootstrap). A metric point without an interval is a vibe.
- **State n and the split** on the figure (title or caption), and label log scales loudly.

## Perception rules
- Sequential data → **viridis/magma family**; never jet/rainbow (fake perceptual boundaries).
  Diverging data (± around zero) → a diverging map centered at zero.
- Categorical → colorblind-safe palette, ≤6-8 distinguishable categories, then facet instead.
- Dense scatters: alpha or hexbin — an opaque blob answers nothing.

## Figures as code
Every report-bound figure is produced by a **script/function from tracked data** (seeded when
sampling), styled once via a shared `mpl` style, saved as both PNG (viewing) and PDF/SVG
(documents), and logged as a run artifact via the active tracker skill — so any figure can be
regenerated when the data or model version bumps. A screenshot of a notebook cell is not a
figure; it's a rumor.

## Standard diagnostics per task
Training: train/val loss + LR schedule (`training`). Classification: confusion matrix, PR curve
with the chosen operating point marked, calibration plot. Detection/segmentation: PR by class,
prediction-vs-GT overlay grids, worst-K cases (`evaluation`'s error-analysis ethos). Regression:
residuals vs prediction, residuals vs key features. Forecasting: backtest fan across origins
(`timeseries`). These are the figures a reviewer asks for — produce them before being asked.
