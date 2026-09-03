# Exercise 06 — Solution

## Prerequisites

```bash
databricks version                # v0.205.0+  (Go CLI, not the 0.1x Python one)
databricks auth login --host https://your-workspace.cloud.databricks.com
```

## 1. Reading `databricks.yml`

From [`examples/databricks.yml`](examples/databricks.yml):

| Question | Answer |
| --- | --- |
| Bundle name | `bundle_lab` |
| Targets | `dev` (default) and `prod` |
| `mode: development` | `dev` |
| `mode: production` | `prod` |
| dev deploys to | your `workspace.host`, per-user path `/Workspace/Users/<you>/.bundle/bundle_lab/dev` |
| prod deploys to | the SP path in `root_path` |
| prod runs as | service principal `ci-sp-prod` |

## 2–3. Point at your workspace + validate

Set `targets.dev.workspace.host` to your workspace URL.

```bash
databricks bundle validate -t dev
```

Clean output ends with the resolved config and:

```
Validation OK!
```

Common errors:

| Error | Fix |
| --- | --- |
| `cannot resolve auth` / `host mismatch` | `databricks.yml` host ≠ the host you `auth login`'d with. Make them match. |
| `unknown field` | Typo/indent in the YAML. |
| `node_type_id ... not available` | Use a node type valid for your cloud/region. |

## 4. Deploy to dev

```bash
databricks bundle deploy -t dev
```

In the UI:

- Files under `/Workspace/Users/<you>/.bundle/bundle_lab/dev/files/...`
- **Workflows** → **`[dev <your name>] weekly_rollup`**
- The job's schedule shows **Paused**

## 5. Run

```bash
databricks bundle run weekly_rollup -t dev
```

```
Run URL: https://<workspace>/#job/123/run/456
...
2025-... Run status: RUNNING
2025-... Run status: TERMINATED SUCCESS
```

The `rollup` notebook executes: prints the catalog, calls
`build_weekly_rollup`, `display()`s 7 rows.

## 6. Change + redeploy

Add `print("v2")` to `notebooks/rollup.py`, then:

```bash
databricks bundle deploy -t dev
```

Output shows only the changed file uploading. `bundle run` again → `v2` in the
task output.

## 7. Prod target (validate only)

```bash
databricks bundle validate -t prod
```

Diff vs dev in the resolved output:

| | dev | prod |
| --- | --- | --- |
| Job name | `[dev you] weekly_rollup` | `weekly_rollup` |
| `run_as` | you | `ci-sp-prod` |
| Deploy path | `/Users/you/.bundle/...` | `/Users/ci-sp-prod@.../.bundle/...` |
| Schedule | paused | active |
| `catalog` var | `main_dev` | `main_prod` |

`deploy -t prod` from a laptop would (a) likely fail production-mode validation
(personal auth vs `run_as` SP) and (b) be the wrong thing to do — CI does it, as
the SP, on a tag (Module 09).

## 8. Clean up

```bash
databricks bundle destroy -t dev
```

Removes the `[dev you] weekly_rollup` job and the deployed files.

## Key takeaways

- A bundle = resource definitions (`resources/*.yml`) + per-target config
  (`targets:` in `databricks.yml`) + the CLI.
- `validate` → `deploy` → `run` → `destroy`, with `-t <target>`.
- `mode: development` = safe sandbox: name-prefixed, schedule paused, per-user
  path. `mode: production` = real, run by an SP, strict.
- `deploy` is incremental.
- Prod deploys belong in CI, as a service principal, from a tag — never from a
  laptop.
- The notebook stays thin; `src/rollup_lib.py` holds the tested logic.
