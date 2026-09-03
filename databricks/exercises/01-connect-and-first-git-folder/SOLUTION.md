# Exercise 01 — Solution

Mostly UI; the value is the reasoning and the git-CLI mapping.

## Part 1 — link credentials

The token proves *you* to the provider. Fine-grained + scoped to one repo +
90-day expiry = least privilege. It goes in **Settings → Linked accounts**,
stored encrypted, used for every Git folder operation you do.

Two layers (Module 01): if there's **no Git folder option at all**, that's the
workspace admin's *Git integration* setting, not your credentials.

## Part 2 — create the Git folder

**Create Git folder** from the HTTPS URL ≡ `git clone <url>` into
`/Workspace/Users/<you>/databricks-lab`, checked out on `main`.

## Part 3 — the loop

| Step | Git dialog action | git CLI |
| --- | --- | --- |
| 5 | Pull | `git pull` |
| 5 | Create Branch `add-hello-notebook` | `git switch -c add-hello-notebook` |
| 7 | Commit & Push (`Add hello notebook`) | `git commit -am "Add hello notebook"` + `git push -u origin add-hello-notebook` |
| 9 | branch selector → `main` / back | `git switch main` / `git switch add-hello-notebook` |

### The committed file

`hello.py` on the provider:

```python
# Databricks notebook source
greeting = "Hello from a Git folder"
print(greeting)

# COMMAND ----------

spark.range(5).show()
```

- First line `# Databricks notebook source` — marks it a notebook.
- `# COMMAND ----------` — cell boundary.
- **No `spark.range(5).show()` output** — Source format never commits outputs,
  even though you ran the notebook. (Exercise 02 verifies this.)

### Switching branches

`hello.py` exists only on `add-hello-notebook`. Switching the Git folder to
`main` rewrites the working tree to `main`'s content — no `hello.py`. This is
exactly `git switch` behaviour; the Git folder is one working copy.

## Key takeaways

- Linked credentials authenticate you; a Git folder is a `git clone` in the
  workspace.
- The Git dialog buttons map 1:1 to `git` commands.
- Source-format notebooks commit code only — running the notebook first doesn't
  put outputs in the commit.
- Switching branches in the dialog swaps the whole Git folder's contents.
- Everything so far is local git + a push; the PR (Exercise 04) happens on the
  provider.
