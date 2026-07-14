# `.claude/memory/policy/` — the policy canon

The **authored source of truth** for how this repo's code and data must be built — the rules a change
has to obey. This directory is the DATA (the canon); the **`governance` skill** is the access PROTOCOL
over it (locate → load → apply → record). Policy text lives here in exactly one place and is never
copied into a skill or CLAUDE.md — those only *point* at it.

> Scaffolded empty on purpose. Add one canon file per **governed domain** your project has, then
> register it in the `governance` skill's Policy index. Do NOT invent domains you don't need yet.

## The pattern
- **Canon** = a version-controlled `<domain>.md` here. A human authors it; code is written and data is
  shaped *from* it. It wins on any conflict.
- **Decision log** (optional, per domain) = an append-only `<domain>-decision-log.md` beside the canon,
  recording each irreducible judgment call: *what / which rule / why*. Add one only for domains that
  make case-by-case calls over time (a prescriptive style guide needs none).

## Typical domains (fill in the ones you have)
| Domain | Canon file | Governs | Needs a decision log? |
|---|---|---|---|
| `<code conventions>` | `<code-conventions.md>` | the idioms every source module follows | usually no (prescriptive) |
| `<data / schema>` | `<data-model.md>` | the data model — entities, fields, invariants | yes, if shape calls recur |
| `<security>` | `<security.md>` | secrets, sensitive data, egress / threat model | as needed |
| `<...>` | `<...>` | `<what it governs>` | `<yes/no>` |

## Adding a domain
1. Author the canon at `policy/<name>.md`.
2. Register a row in the `governance` skill's Policy index and fold that domain's sharp trigger words
   into the skill's `description` so a governed change auto-surfaces it.
3. If the domain makes judgment calls over time, add a decision log beside its canon.

Keep policy in ONE skill (`governance`) indexing MANY canon files here — don't spawn a skill per
domain.
