# Git in Databricks Cheat Sheet

For git itself, see [`../git/cheat-sheet.md`](../git/cheat-sheet.md). For CI
concepts, [`../gitlab/cheat-sheet.md`](../gitlab/cheat-sheet.md).

## Connecting (once per user)

Provider PAT scopes: GitHub `repo` (classic) or fine-grained **Contents:
read/write** + **Metadata: read** · GitLab `write_repository` · Azure DevOps
**Code: Read & Write**.

Databricks: **username ▸ Settings ▸ Linked accounts** → provider + username +
token (or **Link Git account** for OAuth).

## Git dialog ↔ git CLI

| Git dialog | git CLI |
| --- | --- |
| Create Git folder from URL | `git clone <url>` |
| Pull | `git pull` |
| Create Branch | `git switch -c <name>` |
| branch selector | `git switch <name>` |
| Commit & Push | `git commit -am "…"` && `git push` |
| ⋯ ▸ Merge | `git merge <branch>` |
| ⋯ ▸ Discard changes | `git restore .` / `git reset --hard` |
| Create pull request (link) | open provider's new-PR page |

- **No partial staging** in the dialog — commit in stages, or use a terminal
  (`git add -p`).
- **Merge / review / merge PR** happens in the provider, not Databricks.
- Discard changes is the only button that loses (uncommitted) work.

## Notebook source format

```python
# Databricks notebook source        ← must be line 1 (.py). SQL: --  Scala/JS: //
# MAGIC %md                          ← non-Python cell content
# MAGIC # Title

# COMMAND ----------                 ← cell separator

import pyspark.sql.functions as F    ← a normal Python cell
```

| Lang | File | Line 1 | Separator |
| --- | --- | --- | --- |
| Python / R | `.py` / `.r` | `# Databricks notebook source` | `# COMMAND ----------` |
| SQL | `.sql` | `-- Databricks notebook source` | `-- COMMAND ----------` |
| Scala | `.scala` | `// Databricks notebook source` | `// COMMAND ----------` |

- Source format: **outputs never committed**. `.ipynb`: outputs gated by admin
  setting + per-notebook toggle.
- Format setting: **Settings ▸ Developer ▸ Notebook default format** (Source /
  Jupyter). Prefer **Source** for team repos.
- Import modules: Git folder root is on `sys.path` → `from src.mod import fn`.
  `%run ./other_notebook` runs a notebook inline (avoid for real logic).

## Job from Git

Job ▸ **Git**: repo URL + provider + **reference type** (Branch / Tag / Commit)
+ reference. Task notebook paths are **relative to repo root**.

| Env | Ref | Set by |
| --- | --- | --- |
| dev | branch | developer |
| staging | `main` | CI on merge |
| prod | **tag** / commit | CI on tag |

Run job as a **service principal** with its own linked git credential.

## Databricks Asset Bundles

Needs CLI v0.205+ (`databricks version`).

```bash
databricks bundle init                    # scaffold (pick default-python)
databricks bundle validate -t dev         # check config; show planned resources
databricks bundle deploy   -t dev         # upload files + create/update resources
databricks bundle run <job> -t dev        # run a bundle job/pipeline now
databricks bundle summary  -t dev         # what's deployed, where
databricks bundle destroy  -t dev         # tear down what this bundle deployed
```

`databricks.yml` skeleton:

```yaml
bundle:
  name: my_project
include:
  - resources/*.yml
variables:
  catalog: { default: main_dev }
targets:
  dev:
    mode: development         # name-prefix [dev you], schedules paused, per-user path
    default: true
    workspace: { host: https://dbc-dev.cloud.databricks.com }
  prod:
    mode: production          # strict validation, real names, schedules live
    workspace:
      host: https://dbc-prod.cloud.databricks.com
      root_path: /Workspace/Users/ci-sp@acme.com/.bundle/${bundle.name}/${bundle.target}
    run_as: { service_principal_name: ci-sp-prod }
    variables: { catalog: main_prod }
```

Job resource skeleton (`resources/x.job.yml`):

```yaml
resources:
  jobs:
    weekly_rollup:
      name: weekly_rollup
      tasks:
        - task_key: rollup
          notebook_task:
            notebook_path: ../notebooks/rollup.py
            base_parameters: { catalog: ${var.catalog} }
          job_cluster_key: main
      job_clusters:
        - job_cluster_key: main
          new_cluster:
            spark_version: "15.4.x-scala2.12"
            node_type_id: "i3.xlarge"
            num_workers: 2
```

## CLI auth (bundles & scripts)

| Method | Env / command | Use |
| --- | --- | --- |
| Profile | `databricks configure` / `databricks auth login`; `~/.databrickscfg` | local |
| OAuth U2M | `databricks auth login --host https://…` | local, interactive |
| **OAuth M2M** | `DATABRICKS_HOST`, `DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET` | **CI/CD** (service principal) |
| PAT | `DATABRICKS_HOST`, `DATABRICKS_TOKEN` | works; prefer M2M in CI |

`-t` / `--target` selects the environment; omitted → the `default: true` target.

## Secrets

```bash
databricks secrets create-scope external-apis
databricks secrets put-secret external-apis stripe_token
databricks secrets put-acl external-apis <sp-or-group> READ
```

```python
token = dbutils.secrets.get(scope="external-apis", key="stripe_token")  # redacted if printed
```

Never in: notebook cells, repo files, `databricks.yml`, job param defaults,
outputs. Same key, per-environment scope contents.

## `.gitignore` for a Databricks repo

```
.databricks/
__pycache__/
*.pyc
.venv/
dist/
data/
*.parquet
*.csv          # !ref/lookup.csv to keep specific small files
.env
*.pem
```

## Never commit

secrets/tokens · data files & extracts · model binaries · notebook outputs ·
hardcoded catalog/path/env config · `.databricks/` state.

## "What is this at the git CLI?"

The one question that unblocks most Git-folder confusion. Git dialog = a GUI for
`git`; the provider is where branches, PRs, reviews, and merges live.
