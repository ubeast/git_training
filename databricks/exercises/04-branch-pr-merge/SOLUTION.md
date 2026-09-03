# Exercise 04 — Solution

This is the Git course Module 08 / GitLab course Module 05–06 loop, with a Git
folder as the editor. The steps *are* the solution; key points below.

## The loop

| Step | Where | Action |
| --- | --- | --- |
| 1 | Databricks Git dialog | `main` → Pull → Create Branch |
| 2–3 | Databricks | Edit notebook → review diff → Commit & Push |
| 4 | Provider | Open PR (what / why / how tested), assign partner as reviewer |
| 5 | Provider | Partner reviews **Files changed**, comments, Approves |
| 6 | Databricks + Provider | Author pushes fixes to the same branch; partner re-approves; **Merge** on the provider |
| 7 | Databricks Git dialog | `main` → Pull |

## What "how tested" should say

Because reviewers usually can't run the notebook (Module 06), the description
carries the evidence:

> Ran `checks` on cluster `training-shared` (DBR 15.4). Called
> `assert_non_empty(spark.range(3), "t")` → printed "t: 3 rows"; called it on
> `spark.range(0)` → raised AssertionError as expected.

## Non-overlapping cells can still conflict

Both A and B added a function to `checks`. On disk that's:

```python
# Databricks notebook source

# COMMAND ----------

<<<<<<< main
def assert_non_empty(df, name):
    ...
=======
def print_schema(df, name):
    ...
>>>>>>> b-add-schema-print
```

Git sees edits to the same region of `checks.py`. The **first** PR merges
cleanly; the **second** one shows "this branch has conflicts" — resolve on the
provider's web editor (keep both functions, separated by a
`# COMMAND ----------`) or locally, then merge.

Lesson: coordinate on who touches which notebook, or keep helpers in separate
module files (`src/checks.py`) so two people adding functions don't collide as
often — and even then, additions near the same line can conflict. Small,
frequent merges keep it manageable.

## End state

`main` has both merges:

```
*   Merge pull request #4 (b-add-schema-print)
|\
| * Add schema print helper
* |   Merge pull request #3 (a-add-row-count-check)
|\ \
| |/
| * Add row-count check
|/
* <earlier main>
```

`checks` notebook on `main` contains both `assert_non_empty` and
`print_schema`. Both feature branches deleted.

## Key takeaways

- Own Git folder, own branch, per person. Collaboration is branches + PRs, not a
  shared working copy.
- Databricks pushes; the **provider** reviews and merges.
- Address review feedback with commits on the same branch.
- "How tested" in the description substitutes for the reviewer running it.
- Two people editing one notebook conflict easily — coordinate, or split into
  modules, and merge often.
