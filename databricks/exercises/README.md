# Exercises

Hands-on labs for the Git-in-Databricks course. Do each after the module noted.

| # | Exercise | After module | You practise |
| --- | --- | --- | --- |
| 01 | [Connect & first Git folder](01-connect-and-first-git-folder/) | 01–04 | Link credentials, create a Git folder, branch, edit a notebook, commit & push |
| 02 | [Notebook diffs & the source format](02-notebook-diffs/) | 02 | Read the committed `.py`, confirm outputs aren't committed, read a diff |
| 03 | [A notebook merge conflict](03-notebook-conflict/) | 05 | Create and resolve a conflict in one notebook cell |
| 04 | [Feature branch → PR → merge](04-branch-pr-merge/) | 06 | The full loop through the git provider (in pairs) |
| 05 | [Run a job from Git](05-run-job-from-git/) | 07 | A workflow with a Git source; repoint from branch to tag |
| 06 | [Deploy an Asset Bundle](06-asset-bundle/) | 08 | `bundle init` → `validate` → `deploy -t dev` → `run` |

## Prerequisites for all of these

- A **Databricks workspace** with Git folders enabled (any current paid tier).
- **Linked git credentials** (Exercise 01 sets this up) — a PAT or OAuth for
  GitHub / GitLab / Azure DevOps.
- **A cluster** (all-purpose or serverless) you can attach notebooks to.
- **A course repo** your instructor created that you can push branches to. If
  you're doing this solo, create your own empty repo on your git provider and
  use that.
- Exercises 05–06 also need: permission to create jobs; and for 06, the
  **Databricks CLI v0.205+** installed locally with auth configured
  (`databricks auth login --host <your-workspace-url>`).

## How to work through one

1. Read the exercise's `README.md`.
2. Do the **Setup** exactly.
3. Work the **Tasks** in order — try each yourself first.
4. Check against **Verify**.
5. Then compare with `SOLUTION.md`.

## Ground rules

- Use a throwaway Git folder / branch. If a Git folder wedges, delete it and
  re-create it from the URL — nothing is lost as long as your branch is pushed.
- Never commit data, secrets, or notebook outputs (Module 11).
- Write to a `training` catalog / your own schema, never a shared prod one.
