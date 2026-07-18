# Resource matrix — where everything is accessed

> The single inventory of this project's infrastructure: every service, store, and endpoint the
> stack touches — so setup is a read, not archaeology. **The rule:** any change that provisions
> or wires a resource updates this matrix **and `.env.example`** in the same commit — the two
> must agree (every env key here exists there, and vice versa), and a resource missing here is
> a resource the next session can't find. Credentials are recorded **by reference only** — the
> `.env` key name, the AWS profile name, `.dvc/config.local` — never values (security canon:
> `governance` → `security.md`). Written by the infra lanes (`infra-aws`, `local-stack`,
> `containers`, `serving`) and `/intake`/`/bootstrap`; read by everything.

| Resource | Kind | Endpoint / locator | Env keys | Credential (by reference) | Owner skill | Versioned / backup | Added |
|---|---|---|---|---|---|---|---|

_Illustrative rows — replace with real ones as resources appear:_

| Resource | Kind | Endpoint / locator | Env keys | Credential (by reference) | Owner skill | Versioned / backup | Added |
|---|---|---|---|---|---|---|---|
| `myproj-artifacts` | MinIO bucket (DVC remote) | `s3://myproj-artifacts` via `${MINIO_ENDPOINT}` | `MINIO_ENDPOINT` | `.dvc/config.local` (access/secret key) | `local-stack` | bucket versioning ✓ · `mc mirror` nightly | YYYY-MM-DD |
| tracker | MLflow server | `${MLFLOW_TRACKING_URI}` | `MLFLOW_TRACKING_URI`, `MLFLOW_S3_ENDPOINT_URL` | none (local) | `tracking-mlflow` | pg volume + `pg_dump` weekly | YYYY-MM-DD |
| cvat | annotation service | `http://localhost:8080` | `CVAT_HOST` | superuser (human-held) | `local-stack` | label exports DVC-versioned | YYYY-MM-DD |
| `myproj-data` | S3 bucket (raw + processed) | `s3://myproj-data` (`AWS_PROFILE=claude-ds`) | `AWS_REGION`, `AWS_PROFILE` | `~/.aws/` profile `claude-ds` | `infra-aws` | S3 versioning ✓ · lifecycle → IA | YYYY-MM-DD |
