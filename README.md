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
# From the project you want to scaffold:
~/dev/projects/claude-scaffold/install.sh .

# then, inside Claude Code in that project:
/intake
```

`install.sh` copies `.claude/` + `CLAUDE.md` into the target and **never overwrites existing files**
(safe to re-run; it reports what it skipped) and marks hooks executable. `/intake` then interviews you
for your stack and configures the rest (below).

## The one idea that makes this work: `/intake` + two-tier skills

Skills come in two tiers:

- **Always-on** — the *chassis* (`governance`, `memory`, `testing`, `wave-planning`) and the
  *workflow* skills (`datasets`, `training`, `evaluation`, `notebooks`). Tool-agnostic; they describe
  the CV/DS work itself and reference whichever tool you chose.
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
│   ├── notebooks/            # Jupyter hygiene — logic in modules, strip outputs
│   └── _example/             # how to write a skill (the description/triggers contract)
├── commands/
│   ├── intake.md             # /intake — one-time stack onboarding
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
   and fills the placeholders it can.
2. **Fill the remaining `<PLACEHOLDER>`s** `/intake` lists — test commands, the architecture doc for
   `software-architect`, any dataset paths.
3. **Build real skills/agents** from `_example` / `_TEMPLATE`, then delete the leftovers.

## Conventions for placeholders

- `<PLACEHOLDER>` — fill in (`/intake` resolves the stack-dependent ones).
- `_TEMPLATE.md` / `_example/` — copy to a real name, then delete the original.
- Anything in an HTML comment (`<!-- ... -->`) is authoring guidance; delete it in real files.
