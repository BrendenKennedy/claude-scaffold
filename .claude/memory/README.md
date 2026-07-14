# `.claude/memory/` — agent working memory (data store)

The **stored notes** that let a new session resume with the last one's context — refined summaries,
never raw transcripts. This directory is the DATA; the **record/recall protocol + branch workflow** is
the **`memory` skill** (so the process surfaces when you start, branch, or wrap up work — not on every
session). Pulled in on demand, never auto-loaded.

## Layout
| Path | Holds |
|---|---|
| `sessions/` | dated refined summaries of each substantive session (`YYYY-MM-DD-<slug>.md`, newest-last); start from `sessions/_template.md` |
| `reference/` | stable "how we do X" notes that recur but don't warrant a full skill |
| `roadmap.md` | the living backlog: next · in-progress · done-recent |
| `policy/` | authored governance policy canon + decision logs (accessed via the `governance` skill) |

## Not to be confused with
- **Repo-root `docs/`** — human/project documentation (READMEs, design contracts). That's project
  data; this is agent working memory.
- **The personal auto-memory at `~/.claude/projects/**/memory/`** — per-user and cross-project. This
  store is in-repo, git-tracked, and project-scoped.

## What goes where (so it stays consistent)
- **Deep domain knowledge with discovery triggers** → make it a **skill** (`.claude/skills/`), not a note here.
- **Reusable "how we do X in this repo"** → `reference/`.
- **What happened / current state** → `sessions/`.
- **What's next** → `roadmap.md`.
- **Rules the code/schema must obey** → `policy/` (via the `governance` skill).

If a category outgrows itself (e.g. decision history), split it out — a dedicated log beside its
canon in `policy/`, or a new subdir here, is the obvious next addition.
