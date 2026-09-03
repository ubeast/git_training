# Module 07 — Running jobs from Git

A Databricks **job** (also called a **workflow**) can get the notebooks and
scripts it runs from one of two places:

| Source | What it runs | Good for |
| --- | --- | --- |
| **Workspace** | A notebook at a fixed workspace path (e.g. inside a Git folder, or a plain workspace folder) | Quick/interactive; NOT recommended for production |
| **Git provider** | Notebooks/files pulled from a repo at a **branch, tag, or commit**, fetched fresh at each run | Production and anything that must be reproducible |

## Why "from Git" beats "from the workspace" for production

If a job points at a **workspace path** inside a Git folder:

- Whatever branch that Git folder happens to be on is what runs. Someone
  switches the branch or leaves uncommitted edits → the job runs something
  unreviewed.
- There's no record of *exactly* which commit ran.
- Promoting a change means remembering to Pull the right branch into the right
  folder.

If a job uses a **Git source** pinned to a **tag** (e.g. `v2025.09.1`):

- It runs *exactly* the reviewed, released commit, every time.
- "What's in production?" has a precise answer: that tag.
- Rolling back = point the job at the previous tag.
- Nothing is copied into the prod workspace by hand.

## Configuring a Git source

**Workflows → your job → (job-level) → Git**:

| Field | Value |
| --- | --- |
| **Git repository URL** | `https://github.com/acme/pipelines.git` |
| **Git provider** | GitHub / GitLab / Azure DevOps / … |
| **Git reference type** | **Branch**, **Tag**, or **Commit** |
| **Git reference** | `main` / `v2025.09.1` / `a1b2c3d…` |

Then each **task** in the job sets its notebook/script **path relative to the
repo root** — e.g. `notebooks/ingest`, `src/jobs/run_rollup.py`.

At run time Databricks does a shallow checkout of that ref on the job cluster and
runs the task from it. Nothing persists in the workspace.

### Which ref for which environment

| Environment | Ref type | Example | Set by |
| --- | --- | --- | --- |
| Dev / ad-hoc | Branch | `main` or a feature branch | The developer |
| Staging | Branch | `main` | CI on merge to `main` |
| Production | **Tag** or **Commit** | `v2025.09.1` | CI on tag / a release step |

## Credentials for a Git-sourced job

The job checks out the repo as **an identity**:

- If the job **runs as a user** (the default is often the job owner/creator), it
  uses *that user's* linked git credentials.
- Best practice: the job **runs as a service principal**, and that **service
  principal has its own linked git credentials** (a PAT or OAuth connection with
  read access to the repo). Then the job doesn't break when a person leaves or
  rotates their token.

Set "Run as" on the job (**job → ⋯ → Edit permissions / Run as**), and link git
credentials for the service principal (an admin does this via the account
console or API — the service principal needs a **Git credential** entry just
like a user).

## Parameters and per-environment config

A Git-sourced job still needs to know *which* environment it's running against
(which catalog, which storage path). Don't hardcode that in the notebook. Pass
it in:

- **Job parameters** / **task parameters** — `env = prod`, `catalog =
  main_prod`.
- Read them in the notebook via `dbutils.widgets.get("catalog")` or
  `dbutils.jobs.taskValues`.
- Or let an **Asset Bundle** (Module 08) generate one job definition per target
  with the right values baked in — usually the cleanest.

```python
# top of the notebook
dbutils.widgets.text("catalog", "main_dev")
catalog = dbutils.widgets.get("catalog")
spark.sql(f"USE CATALOG {catalog}")
```

## Delta Live Tables / Lakeflow pipelines from Git

DLT (Lakeflow Declarative) pipelines can also use a Git source for their
notebook definitions — same idea: point the pipeline at a repo + ref instead of
workspace notebooks, so the pipeline definition is versioned and reviewed.

## Check yourself

1. A production job points at a notebook path inside someone's personal Git
   folder. Name two things that can go wrong.
2. What Git reference type should a production job use, and why?
3. A Git-sourced job that used to work now fails to check out the repo after an
   engineer left the team. What's the likely cause and the fix?
4. Your notebook needs a different catalog in dev vs prod. Where should that
   value come from?

<details>
<summary>Answers</summary>

1. The folder can be on the wrong branch or hold uncommitted edits, so the job
   runs unreviewed code; and there's no record of the exact commit that ran.
2. A **tag** (or a specific commit). It pins the job to exactly the reviewed,
   released code, makes "what's in prod" unambiguous, and makes rollback a
   one-line ref change.
3. The job was running as that engineer (or using their linked git credentials),
   which are now gone. Fix: run the job as a **service principal** that has its
   own linked git credentials with repo read access.
4. A job/task **parameter** (read via `dbutils.widgets` or task values), or
   generated per-target by an Asset Bundle — never hardcoded in the notebook.

</details>

Next: [Module 08 — CI/CD with Databricks Asset Bundles](08-asset-bundles.md)
