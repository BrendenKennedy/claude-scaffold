---
name: local-stack
description: >
  The self-hosted local DS stack — offline/air-gapped twins of the cloud pieces, run via Compose.
  Carries: MinIO as S3-compatible blob storage (endpoint-url wiring so DVC remotes, MLflow
  artifact stores, and boto3 work unchanged offline; credentials via `dvc remote modify --local`,
  never committed), self-hosted CVAT for annotation (its own compose stack at a pinned release
  tag, shared-storage mount so images don't upload through the browser, superuser creation,
  export to COCO immediately — tool state is not the artifact of record), local Postgres as the
  relational store (init scripts, healthchecks, volume discipline), and the extension matrix
  (pgvector, TimescaleDB, PostGIS, Apache AGE — pick the image for your primary extension;
  combining means a custom image; `CREATE EXTENSION` via init script). Compose mechanics live in
  `containers`; labeling process in `annotation`; queries in `sql`. Load when hosting services
  locally or working offline/air-gapped. Triggers: minio, cvat, self-hosted, local s3,
  s3-compatible, offline, air-gapped, endpoint url, local postgres, pgvector, timescaledb,
  postgis, apache age, create extension, local annotation server, blob storage, host it locally.
---

# local-stack — the cloud's offline twins

**Pinned:** minio, cvat, postgres (+ pgvector/timescaledb/postgis/age images) — unpinned ·
authored 2026-07-18 · run `/skill-update local-stack` against the image tags you actually pull

> On-demand: load this when services must run on your own metal — no cloud account, an
> air-gapped site, or just zero budget. Each service below is the local twin of a piece the
> scaffold already knows, so the *workflows don't change* — only endpoints do. Compose/image
> mechanics (digest pinning, named volumes, `.env` wiring, the down `-v` hazard) are the
> `containers` skill's and apply to everything here. If you're going online-first instead,
> this skill's twin is `infra-aws`. **Every service stood up here gets a row in the resource
> matrix** (`.claude/memory/process/resources.md`) + its keys in `.env.example`, same commit —
> that file is how the rest of the stack knows where everything is accessed.

## MinIO — S3 without AWS
```yaml
  minio:
    image: minio/minio:RELEASE-TAG@sha256:DIGEST
    command: server /data --console-address ":9001"
    env_file: .env                    # MINIO_ROOT_USER / MINIO_ROOT_PASSWORD live there
    ports: ["9000:9000", "9001:9001"] # 9000 = S3 API, 9001 = web console
    volumes: ["minio-data:/data"]
```
Create buckets via the console (`:9001`) or `mc` (`mc alias set local http://localhost:9000 …`,
`mc mb local/PROJECT-artifacts`). Then the one idea that makes everything work: **anything that
speaks S3 takes an endpoint override.**
- **DVC remote:** `dvc remote add -d storage s3://PROJECT-artifacts/dvc`, then
  `dvc remote modify storage endpointurl http://localhost:9000`, and credentials with
  `dvc remote modify --local storage access_key_id …` — **`--local` keeps them in
  `.dvc/config.local` (gitignored)**, the DVC equivalent of `.env`.
- **MLflow artifacts:** set `MLFLOW_S3_ENDPOINT_URL=http://localhost:9000` (in `.env`) and an
  `s3://` artifact root — the tracker (`tracking-mlflow`) needs no other change.
- **boto3/awscli:** `boto3.client("s3", endpoint_url=…)` / `aws --endpoint-url … s3 ls`. The
  `infra-aws` S3 habits (sync, versioning — MinIO supports it per-bucket) carry over.
Turn versioning on for artifact buckets (`mc version enable local/PROJECT-artifacts`) — same
undo-is-part-of-least-privilege reasoning as the cloud.

## CVAT — the local annotation server
CVAT ships its **own multi-service compose stack** (server, workers, its own Postgres + Redis)
— don't hand-roll it and don't merge it into your project compose; run it as delivered:
clone `cvat` at a **pinned release tag** (never `develop`), `docker compose up -d` from its
directory, set `CVAT_HOST` if not localhost, then create the admin:
`docker exec -it cvat_server python3 ~/manage.py createsuperuser`.
- **Mount the data as shared storage** (CVAT's mounted-share mechanism) so annotators attach
  images from the server path — uploading a 50 GB dataset through the browser is the failure
  mode. Alternatively (or additionally) wire CVAT's **cloud-storage backend at MinIO** — CVAT
  speaks S3-compatible storage, so the same `${MINIO_ENDPOINT}` + bucket from the matrix serves
  both DVC and CVAT; one blob store, two consumers, recorded once.
- It's heavy (several GB of images, real RAM); on a laptop, stop it when not labeling.
- **Export to COCO immediately and version the export** (`data-dvc`) — per `annotation`, the
  tool's internal DB is never the artifact of record. The spec/IAA/gold-set process is
  unchanged; only the tool's address moved.

## Postgres — the local relational store
The `containers` compose pattern (digest-pinned image, `env_file: .env`, named volume) plus two
locals-specific habits:
- **Init scripts:** anything in `/docker-entrypoint-initdb.d/*.sql` runs on first boot — the
  right home for `CREATE DATABASE`, roles, and `CREATE EXTENSION` (below), so a fresh
  `compose up` reproduces the database shape from the repo.
- **Healthcheck** (`pg_isready`) + `depends_on: condition: service_healthy` for anything that
  connects at startup (MLflow's backend store, ingest jobs).
The `sql` skill governs everything you *do* with it — this is a warehouse-lite for that lane
(and DuckDB remains the zero-service alternative for single-user analytical work).

## The extension matrix
One fact drives the whole section: **prebuilt images ship one extension family each.**
| Need | Image | Then (init script) |
|---|---|---|
| vectors / embeddings | `pgvector/pgvector:pg16` | `CREATE EXTENSION vector;` |
| time-series tables | `timescale/timescaledb:latest-pg16` | `CREATE EXTENSION timescaledb;` |
| geospatial | `postgis/postgis:16-*` | `CREATE EXTENSION postgis;` |
| graph queries | `apache/age` | `CREATE EXTENSION age;` + `LOAD 'age';` per session |
- **Pick the image for your primary extension.** Needing two (say vector + timescale) means a
  **custom image**: `FROM` one of them, `apt-get install` the other's PGDG package
  (`postgresql-16-pgvector` etc.) — a real Dockerfile in the repo, digest-pinned, per
  `containers`. Don't chase this before a second extension is actually needed.
- `CREATE EXTENSION` is **per-database** — put it in the init script, not in a memory of having
  run it once.
- Extension versions ride the image tag: a tag bump can bump the extension (TimescaleDB
  upgrades need `ALTER EXTENSION … UPDATE`) — pin, and treat bumps as `/skill-update`-style
  deliberate changes.

## Gotchas
- **Backups are now your job.** The named volume is the database; cloud durability assumptions
  don't apply. `pg_dump` on a schedule (or before risky changes) and `mc mirror` for MinIO —
  to a location that survives the machine.
- Ports 9000/5432/8080 collide across projects — one local stack per box, or offset ports
  deliberately in `.env`.
- Everything here still holds secrets in `.env` and state in named volumes — the
  `compose down -v` confirm-gate exists because of exactly these services.
