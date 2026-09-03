# Exercise 05 — Solution

## Setup

`jobs/hello_job.py` on `main`:

```python
# Databricks notebook source
dbutils.widgets.text("run_label", "unset")
label = dbutils.widgets.get("run_label")

# COMMAND ----------

print(f"hello_job running with run_label = {label}")
result = spark.range(10).count()
print(f"counted {result} rows")
```

## 1–3. Job with a Git source

- **Workflows → Create job** → name it.
- **Git** (job level): repo URL, provider, **Branch** = `main`.
- **Add task** `run_hello`: type **Notebook**, source **Git**, path
  `jobs/hello_job` (repo-root relative), cluster, parameter `run_label =
  from-main-branch`.

## 4. Run

Task output:

```
hello_job running with run_label = from-main-branch
counted 10 rows
```

Run details → **Git** section → the commit SHA of `main` at run time.

## 5. Unmerged edit is invisible

Push `print("EDITED LOCALLY — should NOT appear")` on branch `edit-test`, don't
merge. Re-run the job → output unchanged. The job checks out `main`; your edit
isn't there. **The Git folder's current branch and uncommitted state have zero
effect on a Git-sourced job.**

## 6–7. Tag and repoint

```bash
git switch main && git pull
git tag v0.1.0
git push origin v0.1.0
```

Job → Git → **Tag** = `v0.1.0`, parameter `run_label = from-tag-v0.1.0`. Run:

```
hello_job running with run_label = from-tag-v0.1.0
counted 10 rows
```

## 8. Release + rollback

```bash
# change spark.range(10) -> spark.range(20) via a PR to main
git switch main && git pull
git tag v0.2.0 && git push origin v0.2.0
```

- Job → Tag `v0.2.0` → run → "counted 20 rows".
- Job → Tag `v0.1.0` → run → "counted 10 rows".

Rollback = one field.

## Why this is the production pattern

| Workspace-path job | Git-sourced job (tag) |
| --- | --- |
| Runs whatever branch the folder is on | Runs exactly the tagged commit |
| No record of what ran | Records the resolved SHA per run |
| Promote = remember to Pull the right branch | Promote = push a tag / bump the ref |
| Rollback = ??? | Rollback = point at the previous tag |

## Credentials note

This job checked out the repo using **your** linked git credentials (it runs as
you by default). In production the job should **run as a service principal**
that has its own linked git credential with read access — so it doesn't break
when a person's token rotates or they leave (Module 07 / Module 10).

## Key takeaways

- Job-level **Git reference** + task **Source: Git** + **repo-root-relative
  path** = the job runs code from the repo, not the workspace.
- The Git folder / workspace state is irrelevant to a Git-sourced job.
- Dev → branch; staging → `main`; prod → **tag** (reproducible, records the SHA,
  trivial rollback).
- Automated jobs should run as a service principal with its own git credential.
