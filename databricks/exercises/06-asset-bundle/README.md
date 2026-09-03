# Exercise 06 — Deploy an Asset Bundle

**After:** Module 08 · **Time:** ~40 min · Needs the **Databricks CLI v0.205+**
installed locally.

## Goal

Scaffold a bundle, understand `databricks.yml`, deploy it to a **dev** target,
run its job, then read the **prod** target config and see what `mode:
development` vs `mode: production` changes.

## Prerequisites

```bash
databricks version          # must be v0.205.0 or newer (the Go CLI)
databricks auth login --host https://<your-workspace>.cloud.databricks.com
databricks auth profiles     # confirm a working profile
```

If `databricks version` shows `0.1x` you have the legacy Python CLI — install
the new one (`brew install databricks`, or see the docs).

## Option A — scaffold from the template (recommended)

```bash
cd ~
databricks bundle init          # choose "default-python"
#   Project name: bundle_lab
#   Include a stub notebook / DLT / Python wheel: yes to notebook, no to the rest
cd bundle_lab
```

Explore what it made:

```
bundle_lab/
├── databricks.yml
├── resources/
│   └── bundle_lab.job.yml       # (name varies)
├── src/
│   └── notebook.ipynb  or  .py
└── ...
```

## Option B — use the provided minimal bundle

Copy the files from [`examples/`](examples/) into a new folder and work from
there. They're a hand-written minimal version of the same thing:

```
examples/
├── databricks.yml
├── resources/weekly_rollup.job.yml
├── notebooks/rollup.py
└── src/rollup_lib.py
```

## Tasks

### 1. Read `databricks.yml`

Answer, from the file:

- What is the bundle **name**?
- What **targets** are defined? Which is `default`?
- Which target uses `mode: development`? Which uses `mode: production`?
- Where does each target deploy (`workspace.host` / `root_path`)?
- What identity does the prod target run as?

### 2. Point it at your workspace

Edit `databricks.yml` so the `dev` target's `workspace.host` is **your**
workspace URL (and matches the profile you logged in with). Leave `prod`
pointing at a placeholder host — you won't deploy there.

### 3. Validate

```bash
databricks bundle validate -t dev
```

Fix any errors it reports (usually a host mismatch or a missing field). A clean
run prints the resolved config and the resources it would create.

### 4. Deploy to dev

```bash
databricks bundle deploy -t dev
```

Then in the Databricks UI:

- **Workspace** → find the deployed files under
  `/Workspace/Users/<you>/.bundle/bundle_lab/dev/...`
- **Workflows** → find the job. Its name is prefixed **`[dev <your name>]`**.
- Open the job → note its **schedule is Paused** (if the resource defined one).

Both are `mode: development` at work.

### 5. Run the job

```bash
databricks bundle run weekly_rollup -t dev        # use your job's key
```

Watch it start a run; follow the link to the run in the UI. Confirm the notebook
executed.

### 6. Change something and redeploy

- Edit the notebook (`notebooks/rollup.py` or `src/notebook`) — add a
  `print("v2")`.
- `databricks bundle deploy -t dev` again.
- Note it's a **diff** — only the changed file re-uploads.
- Run again; confirm `v2` appears in the output.

### 7. Inspect the prod target (don't deploy)

```bash
databricks bundle validate -t prod
```

Compare the resolved output to `-t dev`:

- The job name has **no `[dev ...]` prefix**.
- `run_as` is a **service principal**.
- The deploy path is the SP's `root_path`, not your user folder.
- If the job has a schedule, it is **not** paused.

This is `mode: production`. You'd never run `deploy -t prod` from your laptop —
CI does it, as the service principal, on a tag (Module 09).

### 8. Clean up

```bash
databricks bundle destroy -t dev
```

Confirm the `[dev ...]` job and the deployed files are gone.

## Verify checklist

- [ ] `databricks version` is v0.205+
- [ ] You can answer the step-1 questions from `databricks.yml`
- [ ] `databricks bundle validate -t dev` passes
- [ ] `deploy -t dev` created a **`[dev <you>]`**-prefixed job with a paused
      schedule
- [ ] `bundle run` executed the job
- [ ] `validate -t prod` shows no prefix, a service-principal `run_as`, and an
      active schedule
- [ ] `destroy -t dev` removed everything

## Questions

1. What does an Asset Bundle put under version control that you'd otherwise
   click together in each workspace?
2. Name two concrete things `mode: development` changes about a deployed job.
3. Why would you never run `databricks bundle deploy -t prod` from your laptop?
4. You changed one notebook and redeployed. Did the whole bundle re-upload?

<details>
<summary>Answers</summary>

1. The full resource definitions — jobs, clusters, schedules, parameters,
   permissions — plus per-environment config, as reviewed YAML.
2. Any two: prefixes the job name with `[dev <you>]`; pauses schedules/triggers;
   deploys to a per-user path; marks runs as development; relaxes validation.
3. Prod should be deployed by CI as a least-privilege **service principal**, from
   a reviewed **tag** — not with a person's credentials from an unreviewed local
   state. Local prod deploys bypass every control.
4. No — `deploy` is incremental; it uploads only changed files and updates only
   changed resources.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
