# Module 08 — CI/CD with Databricks Asset Bundles

A **Databricks Asset Bundle** (DAB, or just "bundle") is:

- a **YAML description** of your Databricks resources — jobs, pipelines, the
  notebooks and code they use, clusters, permissions — plus
- **per-environment settings** (dev / staging / prod), and
- a **CLI** (`databricks bundle …`) that deploys all of it to a workspace.

It's the supported way to get code from a repo into Databricks as *running
jobs*, reproducibly, per environment. It replaces the older `dbx` tool.

> Needs the **Databricks CLI v0.205+** (the Go-based CLI). Check:
> `databricks version`. Install: `brew install databricks` / see the docs.

## Why bundles instead of clicking

Without a bundle, "deploy this pipeline to prod" means recreating a job in the
prod workspace UI — cluster config, schedule, parameters, permissions,
notebook paths — by hand, and keeping it in sync forever. A bundle makes that
job definition **a file in the repo**, reviewed in the PR, applied by one
command in CI.

## Anatomy

```
my_project/
├── databricks.yml            # the bundle root: name, targets, includes
├── resources/
│   └── weekly_rollup.job.yml  # a job definition
├── notebooks/
│   └── rollup.py              # a notebook (source format)
├── src/
│   └── rollup_lib.py          # tested library code
├── tests/
│   └── test_rollup_lib.py
└── requirements-dev.txt
```

### `databricks.yml`

```yaml
bundle:
  name: my_project

include:
  - resources/*.yml

# Defaults applied to every target unless overridden
variables:
  catalog:
    description: Unity Catalog to write to
    default: main_dev

targets:
  dev:
    mode: development       # see below
    default: true
    workspace:
      host: https://dbc-dev.cloud.databricks.com

  staging:
    mode: production
    workspace:
      host: https://dbc-staging.cloud.databricks.com
      root_path: /Workspace/Users/ci-sp@acme.com/.bundle/${bundle.name}/${bundle.target}
    run_as:
      service_principal_name: ci-sp-staging
    variables:
      catalog: main_staging

  prod:
    mode: production
    workspace:
      host: https://dbc-prod.cloud.databricks.com
      root_path: /Workspace/Users/ci-sp@acme.com/.bundle/${bundle.name}/${bundle.target}
    run_as:
      service_principal_name: ci-sp-prod
    permissions:
      - level: CAN_MANAGE
        group_name: data-platform
    variables:
      catalog: main_prod
```

### `resources/weekly_rollup.job.yml`

```yaml
resources:
  jobs:
    weekly_rollup:
      name: weekly_rollup                     # dev mode prefixes this automatically
      schedule:
        quartz_cron_expression: "0 0 6 ? * MON"
        timezone_id: UTC
      tasks:
        - task_key: rollup
          notebook_task:
            notebook_path: ../notebooks/rollup.py
            base_parameters:
              catalog: ${var.catalog}
          job_cluster_key: main
      job_clusters:
        - job_cluster_key: main
          new_cluster:
            spark_version: "15.4.x-scala2.12"
            node_type_id: "i3.xlarge"          # AWS; use the right type for your cloud
            num_workers: 2
```

## `mode: development` vs `mode: production`

| | `mode: development` | `mode: production` |
| --- | --- | --- |
| Resource names | Prefixed `[dev your_name]` so they don't collide | Used as-is |
| Schedules & triggers | **Paused** on deploy | Active |
| Deploy path | Per-user (`/Users/you/.bundle/...`) | The `root_path` you set (a service principal path) |
| Runs marked | As "development" | Normal |
| Validation | Lenient | Strict — e.g. warns/errors if `run_as` is a personal user, if paths look personal |
| Concurrency | Assumes one developer | — |

Rule of thumb: **`dev` target = `development` mode** (safe personal sandbox),
**`staging`/`prod` targets = `production` mode** (real, run by a service
principal).

## The commands

```bash
# scaffold a new bundle from a template
databricks bundle init                       # pick "default-python" for a good starting point

# check the config is valid and see what would be created (per target)
databricks bundle validate -t dev

# deploy the bundle's resources to the target workspace
databricks bundle deploy -t dev

# run a job/pipeline defined in the bundle, now
databricks bundle run weekly_rollup -t dev

# show what's deployed and where
databricks bundle summary -t dev

# tear down everything this bundle deployed to the target
databricks bundle destroy -t dev
```

`-t` / `--target` picks the environment. Omit it and the `default: true` target
is used.

## How the bundle authenticates

The bundle CLI uses the **standard Databricks CLI auth resolution**, matched to
the target's `workspace.host`:

| Method | How | Use |
| --- | --- | --- |
| **Config profile** | `~/.databrickscfg` `[dev]` section; `databricks configure` or `databricks auth login` | Local dev |
| **OAuth U2M** | `databricks auth login --host https://...` (browser) | Local dev, interactive |
| **OAuth M2M** | env: `DATABRICKS_HOST`, `DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET` (a service principal) | **CI/CD** |
| **PAT** | env: `DATABRICKS_HOST`, `DATABRICKS_TOKEN` | Works, but prefer OAuth M2M in CI |

In CI you set the M2M env vars as pipeline secrets and the bundle commands just
work (Module 09).

## What gets deployed, and where it lands

`databricks bundle deploy -t staging`:

1. Uploads the bundle's files (notebooks, `src/`, wheels) to the target
   workspace under the target's `root_path`.
2. Creates/updates the **jobs, pipelines, and other resources** from
   `resources/*.yml` via the APIs.
3. Sets **permissions** as declared.
4. Records state so the next deploy is a diff, and `destroy` can clean up.

The deployed jobs use a **Git source or the uploaded files** depending on your
config; a common production pattern is deploy-from-CI-at-a-tag so the workspace
copy always corresponds to a released commit.

## `.gitignore` for bundles

Add:

```
.databricks/          # local bundle state / cache
dist/
*.egg-info/
__pycache__/
```

## Check yourself

1. In one sentence, what does an Asset Bundle let you keep in the repo that you'd
   otherwise recreate by hand?
2. What does `mode: development` do to a job's schedule and name?
3. Which auth method should CI use to deploy a bundle, and what does it
   authenticate as?
4. What's the difference between `databricks bundle validate` and `databricks
   bundle deploy`?

<details>
<summary>Answers</summary>

1. The full definition of your Databricks resources — jobs, pipelines, clusters,
   parameters, permissions, per environment — as reviewed YAML instead of
   click-ops in each workspace.
2. It pauses the schedule on deploy and prefixes the job name with
   `[dev <your name>]` so a dev deploy can't collide with the real job or fire
   on its own.
3. **OAuth M2M** via `DATABRICKS_HOST` / `DATABRICKS_CLIENT_ID` /
   `DATABRICKS_CLIENT_SECRET` — authenticating as a **service principal**, not a
   person.
4. `validate` only checks the config and shows what *would* be created for a
   target (no changes). `deploy` actually uploads the files and creates/updates
   the resources in the target workspace.

</details>

Next: [Module 09 — Automating with CI pipelines](09-cicd-pipelines.md)
