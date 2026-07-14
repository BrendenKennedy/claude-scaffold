---
name: testing
description: >
  How verification actually works in THIS repo — the cheapest-to-costliest confidence ladder and the
  exact commands that work TODAY (not the ones you'd assume). Carries the real test runner and its
  invocation, the offline-safe rule (unit tests mustn't need env, a live service, network, or a GPU —
  stub the boundary), the ML confidence checks (tiny-data smoke: a forward pass + one train step on a
  2-sample fixture; determinism; split-leakage; metric sanity), the live/GPU-smoke pattern (skips
  cleanly when its dependency — a service, or CUDA — is down, and self-cleans), the readiness check for
  any service a test needs, and the environment preconditions. Reach for it BEFORE running or writing a
  test, verifying a change, or claiming something works. Use for: running the suite, adding a test,
  checking a change end-to-end, or wiring CI later. Triggers: run tests, run the tests, how do I test,
  verify, does this work, test this change, is it passing, <PLACEHOLDER: the runner name, e.g. pytest /
  jest / go test>, offline test, smoke test, readiness check, is the service up, integration test, CI,
  forward-pass smoke, shape mismatch, device/dtype bug, determinism test, leakage test, overfit one
  batch, does the model train, cuda available.
---

# Testing & verification — how this repo actually checks a change

> On-demand: load this before running or writing a test, or before saying a change works. It carries
> the commands that work **today** — don't assume a runner or command that isn't wired up yet.

> **Fill this in for your project.** The value of this skill is the *specifics* — the exact commands,
> the one surprising fact about how tests run here, the preconditions. Strip the `<PLACEHOLDER>`s and
> keep it honest: a green-looking command that never actually ran is worse than no test.

## When this applies
Running the suite, adding a test, verifying a change end-to-end, or wiring CI later.

## Critical fact (the thing that surprises people)
<PLACEHOLDER — e.g. "the obvious runner isn't installed; tests run as standalone scripts" or "you must
build first" or "delete this section if nothing here is surprising".>

## The verification ladder (cheapest → costliest)
> Run every command below through **`uv run`** so it executes inside the locked env (see `env-uv`). The
> `<PLACEHOLDER>`s are the *runner* — this scaffold doesn't fix pytest vs. standalone scripts; fill in
> whichever your project wires up (e.g. `uv run <PLACEHOLDER: pytest / python tests/...>`).

1. **Compiles / imports + format (offline, no side effects).**
   `<PLACEHOLDER: build/typecheck/import command>` · `<PLACEHOLDER: formatter + linter>`
   (the `validate-python` — or your language's — hook may already run the formatter on edited files.)
2. **Unit tests (offline — no env, service, network, or GPU).**
   `<PLACEHOLDER: how to run the unit suite; how to run one file/test>`
3. **Tiny-data smoke (offline, CPU-fallback — the ML unit of confidence).** A forward pass + one
   optimizer step on a **2-sample fixture** — catches shape / device / dtype bugs in seconds without
   touching real data or a GPU. See *ML confidence checks* below.
   `<PLACEHOLDER: how to run the tiny-data smoke>`
4. **Integration smokes (need a service up, or a real GPU).** Live round-trips that **skip cleanly if
   the dependency is unreachable** — a service that's down, or `torch.cuda.is_available()` False — and
   delete anything they create:
   `<PLACEHOLDER: smoke command>` plus a readiness probe: `<PLACEHOLDER: how to check the service is up>`.
5. **Run it for real.** `<PLACEHOLDER: bring up services / apply migrations / run the app end-to-end>`.

## ML confidence checks (the cheap ones that catch the expensive bugs)
These are fast, offline, and CPU-only — they belong in the unit tier and buy far more confidence per
second than a full training run. Author them as `<PLACEHOLDER: unit-test file/pattern>`.

- **Tiny-data smoke.** Build the model and a **2-sample** fixture (random tensors of the real shape, or
  two tiny real records), run one forward pass and one `loss.backward()` + `optimizer.step()`. Assert the
  output shape/dtype, that the loss is finite, and that at least one parameter's `.grad` is non-None. This
  catches shape mismatches, device/dtype errors, and broken graphs in seconds. Keep it on **CPU** — never
  require a GPU.
- **Overfit one batch** (same fixture). Loop the tiny-data step ~50–100 iterations on **one** batch and
  assert the loss drops to near-zero. If a model can't memorize a single batch, the training path is
  wired wrong — cheaper to catch here than after a real run.
- **Determinism.** Seed everything (`<PLACEHOLDER: your seed helper — RNGs + framework>`), run the
  forward/one-step twice, and assert **identical** output/loss. A drift means an unseeded RNG or
  nondeterministic op — reproducibility is an always-on convention here, so this is a real test, not a
  nicety.
- **Split-leakage assertion.** Assert the train / val / test **index sets are pairwise disjoint** (and,
  where identity matters, that no group/patient/scene straddles splits). This ties to the `datasets`
  skill, which owns how splits are defined; the test enforces that they stay separate.
- **Metric sanity.** Feed a **known input** to the metric and assert the **known output** (e.g. a perfect
  prediction ⇒ metric at its ceiling, a fixed confusion case ⇒ the hand-computed value). Guards against a
  metric that silently returns a plausible-but-wrong number.

## Preconditions
- `<PLACEHOLDER: any service/endpoint/env that must be available, and how to bring it up>`.
- `<PLACEHOLDER: config/.env setup, migrations, seed data>`.
- Live checks gate on availability: if the dependency isn't up, smokes/readiness **skip** — they don't fail.

## Conventions
- Tests live in `<PLACEHOLDER: dir>`, named `<PLACEHOLDER: pattern>`.
- **Offline-safe is non-negotiable for unit tests.** Drive external boundaries through a stub/mock
  (`<PLACEHOLDER: the mocking approach — e.g. a fake transport, in-memory fixture>`) — mock the
  **data/model boundary** so no unit test hits the network, a dataset on disk, or a required GPU. Tiny
  tensors on CPU stand in for real batches. Put anything live in a smoke that skips cleanly.
- **GPU/CUDA tests skip cleanly.** A test that genuinely needs the device guards on
  `torch.cuda.is_available()` and **skips (exit 0), never fails**, when it's False — the same
  skip-when-the-dependency-is-down pattern the live smokes use, so the suite stays green on a CPU box.
- Assert the **contract AND every rejection mode** (bad input, missing field, wrong type), and
  **round-trips** where they apply.
- Test-time knobs: override a module constant / inject a fake, and **restore it in a `finally`**.

## Adding a runner / CI later
`<PLACEHOLDER: how you'd add a real test runner or CI, and what stays true (e.g. existing tests keep
working unchanged).>`

## Gotcha
Do not run a command as if it works when it doesn't yet. This skill is how you **run** the checks; the
authoring rules for tests (where they live, the mock pattern) are a code convention — keep those in the
policy canon (`.claude/memory/policy/`, via the `governance` skill), not restated here.
