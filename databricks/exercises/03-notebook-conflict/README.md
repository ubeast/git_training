# Exercise 03 — A notebook merge conflict

**After:** Module 05 · **Time:** ~25 min · Uses the `databricks-lab` Git folder.

## Goal

Deliberately create a merge conflict in a single notebook cell, then resolve it
— trying the Git dialog first, with the CLI/provider fallback if needed.

## Setup

Get onto a clean `main` with a config notebook to fight over.

### 1. Merge your Exercise 01–02 work first (or branch from main)

Simplest: on the provider, merge `add-hello-notebook` into `main` (or just work
from `main` directly for this exercise). Then in Databricks:

- Git dialog → `main` → **Pull**.

### 2. Create the config notebook on main

> For a clean exercise it's fine to commit this one notebook straight to `main`
> in your **personal** lab repo. On a real protected repo you'd do it via a PR.

- In the Git folder, **Create → Notebook** → `config` → Python.
- Cell 1:
  ```python
  # COMMAND ----------  (this is cell 1; the marker line is implicit)
  CATALOG = "training"
  SCHEMA = "sandbox"
  BATCH_SIZE = 1000
  ```
- Git dialog → commit `Add config notebook` → **Commit & Push** (to `main`).

## Tasks

### 3. Branch A changes BATCH_SIZE

- Git dialog → **Create Branch** → `tune-batch-size`.
- Edit `config` cell 1: change `BATCH_SIZE = 1000` → `BATCH_SIZE = 5000`.
- Commit `Raise batch size to 5000` → **Commit & Push**.

### 4. Branch B changes the same line

- Git dialog → branch selector → `main` → **Pull**.
- **Create Branch** → `lower-batch-size`.
- Edit `config` cell 1: change `BATCH_SIZE = 1000` → `BATCH_SIZE = 250`.
- Commit `Lower batch size to 250 for memory safety` → **Commit & Push**.

### 5. Merge A into main (via the provider)

- On the provider, open a PR from `tune-batch-size` → `main` and merge it.
  (Or, in your personal repo, merge locally — the point is `main` now has
  `BATCH_SIZE = 5000`.)

### 6. Now conflict branch B

- Databricks → Git dialog → branch selector → `lower-batch-size`.
- Bring `main` into your branch: Git dialog → `main` → **Pull**, then switch
  back to `lower-batch-size`, then **⋯ → Merge** (merge `main` in). *Or* just
  try **Pull** on `lower-batch-size` if your setup tracks it against main.
- You get a **conflict** on `config.py`: `main` says `5000`, your branch says
  `250`.

### 7. Read the conflict

The Git dialog shows `config.py` conflicted. Open it. You'll see, in the
notebook source:

```
CATALOG = "training"
SCHEMA = "sandbox"
<<<<<<< HEAD
BATCH_SIZE = 5000
=======
BATCH_SIZE = 250
>>>>>>> lower-batch-size
```

(HEAD side = what you merged in from `main`; the other = your branch — exact
labels vary.)

### 8. Resolve

Decide: keep 250 (memory safety wins), and add a comment. Edit the file to:

```
CATALOG = "training"
SCHEMA = "sandbox"
BATCH_SIZE = 250  # contested: raised to 5000 on main, lowered here for memory safety
```

- **No `<<<<<<<`, `=======`, `>>>>>>>` lines left.**
- The cell must still be valid — no stray markers inside it.
- Mark resolved / commit the resolution from the Git dialog.

### 9. Fallback if the dialog fights you

If the in-dialog resolution won't give a clean result, use the CLI. In a **web
terminal** (or a local clone):

```bash
cd /Workspace/Users/<you>/databricks-lab      # or your local clone path
git switch lower-batch-size
git fetch
git merge origin/main
# edit config.py: set BATCH_SIZE = 250 with the comment, remove all markers
git add config.py
git commit
git push
```

Then Databricks Git dialog → **Pull** on `lower-batch-size`.

To bail out entirely at any point: `git merge --abort` (terminal) or discard the
in-progress merge in the dialog.

### 10. Verify the notebook still works

- Open `config` in Databricks on `lower-batch-size`. It should render as **one
  clean cell**, no marker lines.
- Run it — no `SyntaxError`.
- `git log --oneline` (terminal) or the dialog history shows a merge commit.

## Verify checklist

- [ ] You produced a real conflict on `config.py` (both branches changed
      `BATCH_SIZE`)
- [ ] You could identify which side of the markers was `main` and which was your
      branch
- [ ] The resolved `config` notebook has no conflict markers and runs cleanly
- [ ] History shows a merge that combined the two branches
- [ ] You know how to abort a conflicted merge

## Questions

1. Why did only the `BATCH_SIZE` line conflict and not `CATALOG` / `SCHEMA`?
2. What's the risk of leaving a `=======` line inside a notebook cell,
   specifically (vs a plain script)?
3. Name two places you can resolve a Databricks notebook conflict if the Git
   dialog is awkward.
4. Mid-conflict you change your mind. How do you get back to before the merge?

<details>
<summary>Answers</summary>

1. Only `BATCH_SIZE` was changed on both branches. `CATALOG` and `SCHEMA` were
   untouched, so git merged them with no conflict.
2. It can break the notebook's **cell structure** / make the cell fail to parse
   — not just leave one bad line. The `# COMMAND ----------` boundaries must stay
   intact.
3. The provider's web conflict editor on the PR, or a git CLI (web terminal or
   local clone) then Pull in Databricks.
4. `git merge --abort` in a terminal, or discard the in-progress merge in the
   Git dialog — everything returns to pre-merge state.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
