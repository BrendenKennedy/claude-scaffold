---
name: timeseries
description: >
  Time-series / forecasting discipline — where random splits and vanilla metrics lie hardest.
  Carries: temporal splits only (train on past, evaluate on future; rolling-origin backtesting,
  `TimeSeriesSplit`, an embargo gap for autocorrelation), the leakage traps (lag/rolling features
  crossing the boundary, scalers fit on the future, covariates not actually known at forecast
  time), naive baselines as gates (last-value, seasonal-naive — beat them before anything fancy),
  metrics that survive zeros and scale (MASE, sMAPE, pinball loss for quantiles — not plain
  MAPE), the forecast horizon as a written contract, and global-vs-per-series models. Load for
  any forecasting or time-ordered modeling task. Triggers: time series, forecast, forecasting,
  backtest, backtesting, rolling origin, walk-forward, TimeSeriesSplit, lag features, rolling
  window, seasonality, seasonal naive, ARIMA, prophet, horizon, MASE, sMAPE, pinball, exogenous,
  future leakage.
---

# timeseries — forecasting without borrowing from the future

> On-demand: load this when the data has a time arrow. The general split/metric discipline
> (`datasets`, `evaluation`) still applies but its *random-split instincts are actively wrong
> here* — this skill replaces them. Tabular mechanics (pipelines, boosting) still come from
> `tabular` when forecasting with regressors.

## Splits: the future is the only honest test set
- **Train on the past, evaluate on the future. Always.** A shuffled split lets autocorrelated
  neighbors answer for each other — accuracy that evaporates in production.
- **Backtest with rolling origin** (walk-forward): fit on `[0, t]`, forecast `(t, t+h]`, roll `t`
  forward, aggregate. sklearn's `TimeSeriesSplit` is the simple version; report the *distribution*
  across folds, not one lucky window.
- **Leave a gap (embargo) between train end and test start** when features use rolling windows —
  a 7-day rolling mean at the boundary contains test-period information otherwise.
- The final holdout is the most recent horizon-length window, touched once — same
  touch-test-once rule as everywhere.

## The leakage traps (this lane's specialty)
- **Lag/rolling features must be computed causally** — `shift(1)` before any rolling op; a
  same-row rolling mean includes today's target. Compute features within the training window,
  never on the concatenated full series.
- **Scaling/decomposition fit on train only** — a scaler or STL fit on the full series has seen
  the future's level and trend.
- **Covariates must be known at forecast time.** Weather *forecasts* are legitimate features;
  actual weather is not (you won't have it when predicting). Audit every exogenous feature with
  "is this available at prediction time for the horizon?" — the same question as P4's leakage
  review, sharpened.

## Baselines are gates
Naive last-value (`y[t+h] = y[t]`) and seasonal naive (`y[t+h] = y[t+h-season]`). These are
embarrassingly strong on real business series; a model that can't beat seasonal-naive on the
backtest is negative value, and MASE (below) bakes this comparison into the metric.

## Metrics that survive the domain
- **MASE** — error scaled by the naive baseline's error; `<1` literally means "beats naive."
- **sMAPE** over plain MAPE — MAPE explodes near zero actuals and asymmetrically punishes
  over-forecasting.
- **Pinball (quantile) loss** when the consumer needs intervals or asymmetric costs — most
  operational forecasts do; a point forecast hides exactly the risk the decision cares about.
- Slice the backtest by series, season, and horizon step (h=1 vs h=30 degrade differently) —
  the `evaluation` skill's error-analysis ethos, on time axes.

## Model shape notes
- **Horizon, granularity, and update cadence are P1 contract items** — "forecast demand" is not a
  problem statement; "daily, 14 days ahead, refit weekly" is.
- **Many related series → try one global model** (boosted trees on lag features across series,
  with series-id features) before per-series classical fits; it usually wins on short/sparse
  series. Statistical baselines (ARIMA/ETS) remain excellent honest yardsticks.
- Refit-vs-fine-tune cadence is part of the backtest: evaluate the *policy* (refit weekly) not
  just the model, so production behavior is what you measured.
