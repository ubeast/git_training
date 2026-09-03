# Exercise 05 — Run a job from Git

**After:** Module 07 · **Time:** ~30 min

## Goal

Create a Databricks job (workflow) that runs a notebook **directly from the
repo** at a branch, run it, then repoint it to a **tag** — the production
pattern.

## Setup

You need a notebook in the course repo (or your `databricks-lab`) that runs
quickly and takes a parameter. On a branch, add `jobs/hello_job.py`:

```python
# Databricks notebook source
dbutils.widgets.text("run_label", "unset")
label = dbutils.widgets.get("run_label")

# COMMAND ----------

print(f"hello_job running with run_label = {label}")
result = spark.range(10).count()
print(f"counted {result} rows")
```

Commit, push, open a PR, merge it to `main` (so `main` has `jobs/hello_job.py`).
Pull `main` in your Git folder.

## Tasks

### 1. Create the job

- Databricks → **Workflows → Create job**.
- Name: `hello-from-git-<yourname>`.

### 2. Point the job at Git (job level)

- In the job settings, find **Git** (job-level, sometimes under "Job details" or
  a "Git" panel).
- **Add Git reference**:
  - Git repository URL: the course repo HTTPS URL.
  - Git provider: GitHub / GitLab.
  - Reference type: **Branch**. Reference: `main`.

### 3. Add a task that runs the repo notebook

- **Add task**:
  - Task name: `run_hello`
  - Type: **Notebook**
  - Source: **Git** (should be pre-selected now that the job has a Git ref)
  - Path: `jobs/hello_job` (relative to repo root — **no leading slash, no
    workspace path**)
  - Cluster: a small job cluster or your all-purpose cluster
  - Parameters: `run_label` = `from-main-branch`

### 4. Run it

- **Run now.**
- Open the run → the `run_hello` task → **Output**. Confirm:
  ```
  hello_job running with run_label = from-main-branch
  counted 10 rows
  ```
- Note in the run details: it records the **commit SHA** it checked out from
  `main`.

### 5. Prove it runs repo code, not workspace code

- In your Git folder on a **new branch**, change the print line in
  `jobs/hello_job.py` to something obviously different (`print("EDITED LOCALLY
  — should NOT appear")`). **Commit & Push that branch, but do NOT merge it.**
- Run the job again. The output is **unchanged** — the job runs `main`, and your
  edit is on an unmerged branch. The workspace/Git-folder state is irrelevant to
  the job.

### 6. Create a release tag

On the provider (or via git CLI):

```bash
git switch main && git pull
git tag v0.1.0
git push origin v0.1.0
```

(Or GitHub: Releases → Draft a new release → tag `v0.1.0`. GitLab: Code → Tags →
New tag.)

### 7. Repoint the job to the tag

- Job → Git settings → Reference type: **Tag**, Reference: `v0.1.0`.
- Change the task parameter `run_label` = `from-tag-v0.1.0`.
- **Run now.** Output shows `run_label = from-tag-v0.1.0` and the run details
  show the SHA that `v0.1.0` points at.

### 8. Simulate a release + rollback

- Merge a small change to `main` (e.g. change the row count to
  `spark.range(20)`), then `git tag v0.2.0 && git push origin v0.2.0`.
- Point the job at `v0.2.0`, run — "counted 20 rows".
- **Rollback**: point the job back at `v0.1.0`, run — "counted 10 rows" again.
  One field changed; that's your rollback.

## Verify checklist

- [ ] The job has a **Git reference** and the task **Source: Git** with a
      repo-root-relative path
- [ ] Running it produced the notebook's output and recorded a commit SHA
- [ ] An unmerged branch edit did **not** change the job's behaviour
- [ ] You created tags `v0.1.0` / `v0.2.0` and pointed the job at a tag
- [ ] Switching the job's tag reference changed which code ran (and rolled back)

## Questions

1. Why does the job's output not change when you push an edit to an unmerged
   branch?
2. The task path is `jobs/hello_job`, not
   `/Workspace/Users/you/databricks-lab/jobs/hello_job`. Why?
3. What's recorded in the run details that makes a Git-sourced run reproducible?
4. How do you roll back a production job that runs from `v0.2.0`?

<details>
<summary>Answers</summary>

1. The job checks out its configured ref (`main`) fresh at each run. Your edit
   is on a different, unmerged branch, so it's not in `main` and the job never
   sees it. The Git folder / workspace copy is unrelated to what the job runs.
2. With a Git source, task paths are **relative to the repo root**. Databricks
   checks the repo out on the job cluster and resolves the path there — there is
   no workspace path involved.
3. The exact **commit SHA** the ref resolved to at run time. Combined with the
   repo URL, that pins precisely what ran.
4. Change the job's Git reference from `v0.2.0` back to `v0.1.0` and run — one
   field. (Or redeploy the old tag via an Asset Bundle.)

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
