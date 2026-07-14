# claude-scaffold — a CV/DS starting point for Claude Code

An opinionated **`.claude/` configuration for computer-vision & data-science work** in
[Claude Code](https://claude.com/claude-code). Instead of a blank agent directory, you start with
skills, subagents, governance, and memory already shaped around the ML loop — datasets, training,
evaluation, experiment tracking — plus a one-command onboarding that tunes it to *your* stack.

It's also a worked example of **how to integrate coding agents into an ML workflow**: how skills
auto-surface by trigger, how a `/intake` command rewrites the config to match your tools, how policy
lives as governed canon instead of scattered rules, and how work is remembered across sessions.

> **Assumptions (v1).** PyTorch-centric CV, an **NVIDIA GPU** (local *or* a remote box you SSH into),
> and **uv** for environments. Default tools: **MLflow · Hydra · DVC** (swap them in `/intake`).
> Colab / CPU-only / Apple-MPS aren't covered yet — that's a fast-follow, not a hidden assumption.

## Quick start

```bash
# 1. Get the scaffold (clone it once; reuse it for every project):
git clone https://github.com/BrendenKennedy/claude-scaffold.git ~/dev/claude-scaffold

# 2. Drop it into the project you want to scaffold:
cd ~/path/to/my-project
~/dev/claude-scaffold/install.sh .

# 3. Then, inside Claude Code in that project — BOTH, in this order:
/intake      # picks your STACK    (tracker / config / data-versioning)
/bootstrap   # builds the SHAPE    (conf/ tree + entry points the skills describe)
```

`install.sh` copies `.claude/` + `CLAUDE.md` into the target and **never overwrites existing files**
(safe to re-run; it reports what it skipped), marks hooks executable, and stamps
`.claude/scaffold-version` so a project always knows which scaffold version it came from.

**Run both commands, in that order.** `/intake` tunes the config to your tools; `/bootstrap` generates
the project skeleton those tools are configured *for*. Skip `/bootstrap` and the skills document a
project you don't have — `config-hydra` describes a `conf/` tree that isn't there, `training` describes
a `train.py` that isn't there, and "config over constants" governs nothing.

> This repo is a **GitHub template** — you can also hit **"Use this template"** to start a new project
> from it directly, rather than cloning and installing into an existing one.

## The one idea that makes this work: `/intake` + two-tier skills

Skills come in two tiers:

- **Always-on** — the *chassis* (`governance`, `memory`, `testing`, `wave-planning`) and the
  *workflow* skills (`datasets`, `training`, `evaluation`, `pipelines`, `notebooks`). Tool-agnostic;
  they describe the CV/DS work itself and reference whichever tool you chose.
- **Tool skills** — one tool each (`env-uv`, `tracking-mlflow`, `config-hydra`, `data-dvc`, …), gated
  **on/off** by `settings.json` `skillOverrides`.

**`/intake`** is the switch: it asks which tracker / config system / data-versioning tool you use,
writes `skillOverrides` to enable those and disable the rest, and fills the placeholders your answers
determine (MLflow URI, DVC remote, the ARM torch index if you're on a Grace-Blackwell box, …). Prefer
W&B over MLflow? `/intake` flips it — no edits to the workflow skills that reference "the tracker."

## What's in the box

```
.claude/
├── settings.json            # permissions + hook wiring + skillOverrides (the profile /intake writes)
├── agents/
│   ├── code-reviewer.md      # diff review — correctness + quality + an ML/CV lens
│   ├── software-architect.md # read-only planner (fill in your architecture)
│   ├── ml-engineer.md        # builds models + train/eval loops
│   ├── eval-analyst.md       # read-only: metrics → error-analysis findings
│   ├── data-engineer.md      # dataset ingestion, labels, splits, dataloaders
│   └── _TEMPLATE.md          # copy → new subagent
├── skills/
│   ├── governance/           # policy-canon index + locate→load→apply→record
│   ├── memory/               # session memory + branch-per-session workflow
│   ├── testing/              # verification ladder + ML smokes (fill in the commands)
│   ├── wave-planning/        # decompose one goal into a collision-free parallel build
│   ├── env-uv/               # [tool] uv env + torch/CUDA matrix + GPU sanity
│   ├── tracking-mlflow/      # [tool] MLflow experiment tracking
│   ├── config-hydra/         # [tool] Hydra config composition + sweeps
│   ├── data-dvc/             # [tool] DVC data/model versioning
│   ├── datasets/             # splits, label formats (COCO/YOLO/VOC), provenance, leakage
│   ├── training/             # train/fine-tune loop — seeds, checkpoints, resume
│   ├── evaluation/           # metrics (mAP/IoU/PR), eval harness, error analysis
│   ├── pipelines/            # multi-stage cascades — the seam invariants (detect → crop → score)
│   ├── notebooks/            # Jupyter hygiene — logic in modules, strip outputs
│   └── _example/             # how to write a skill (the description/triggers contract)
├── commands/
│   ├── intake.md             # /intake — one-time stack onboarding (the STACK)
│   ├── bootstrap.md          # /bootstrap — one-time project skeleton (the SHAPE) — run after /intake
│   ├── review.md             # /review the current diff
│   ├── wrapup.md             # /wrapup — session close-out
│   └── _TEMPLATE.md
├── hooks/
│   ├── validate-python.py    # PostToolUse: ruff format + check on edited .py
│   └── validate-bash.sh      # PreToolUse: blocks rm -rf of root/home
├── scripts/                  # helper scripts called by hooks/commands (README inside)
└── memory/                   # agent working memory — pulled on demand, never auto-loaded
    ├── roadmap.md            #   living backlog
    ├── sessions/             #   dated session summaries (+ _template.md)
    ├── reference/            #   stable "how we do X" notes
    └── policy/               #   governance canon: data-governance.md · model-governance.md
CLAUDE.md                     # the glossary/map (this is what loads every session)
install.sh                    # the drop-in installer
```

## The conventions worth knowing

- **CLAUDE.md is a map, not a manual.** It stays small and points at everything else, so it never
  rots. Beyond a short *Always-on conventions* list (seed everything · never leak the eval set · config
  over constants · deps via `uv`), deep knowledge lives in skills; "what happened" lives in
  `memory/sessions/`.
- **Skills auto-surface by `description`.** Write that field for *discovery* — pack it with the words a
  user would actually type. See `skills/_example/SKILL.md`.
- **Governance, not rules.** Domain policy is authored canon in `memory/policy/`
  (`data-governance` · `model-governance`), indexed by the `governance` skill (locate → load → apply →
  record) — not scattered `rules/*.md`.
- **Reproducibility is the throughline.** Every trained model traces back to its config + code SHA +
  data version + seed + lockfile; the `training`/`evaluation`/`datasets` skills and the two policies all
  enforce it.
- **Memory across sessions.** Refined session summaries, a roadmap, reference notes, and the policy
  canon — pulled in on demand, never auto-injected. The `memory` skill owns the read/write + branch
  workflow.
- **Multi-agent builds.** `wave-planning` decomposes one goal into a collision-free set of parallel
  agent tasks (this scaffold was itself built that way).

## After installing — make it yours

1. **Run `/intake`** — pick your tracker / config / data-versioning tools; it writes `skillOverrides`
   and fills the stack placeholders.
2. **Run `/bootstrap`** — it interviews you for the **CV task** (classification · detection ·
   segmentation · anomaly detection · a multi-stage pipeline), generates the `conf/` tree and entry
   points to match, *proves they run*, and back-fills the placeholders that needed that code to exist.
   The task answer genuinely reshapes the skeleton — anomaly detection is not classification with the
   labels renamed, and a "fit-not-trained" method (PatchCore, PaDiM) gets a `fit.py` with no optimizer,
   scheduler, or epoch loop at all.
3. **Fill the remaining `<PLACEHOLDER>`s** the two commands list — these need *your* decisions, not an
   agent's guess: the architecture doc for `software-architect`, the policy domains in `memory/policy/`,
   the data-remote URL.
4. **Build real skills/agents** from `_example` / `_TEMPLATE`, then delete the leftovers.

## Conventions for placeholders

- `<PLACEHOLDER>` — fill in (`/intake` resolves the stack-dependent ones).
- `_TEMPLATE.md` / `_example/` — copy to a real name, then delete the original.
- Anything in an HTML comment (`<!-- ... -->`) is authoring guidance; delete it in real files.
