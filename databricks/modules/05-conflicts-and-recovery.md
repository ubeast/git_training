# Module 05 — Conflicts & recovery

Conflicts happen in Databricks for the same reason as anywhere (Git course,
Module 06): two branches changed the same part of the same file. Notebooks make
them slightly more fiddly because the "file" is source with `# COMMAND` markers.

## When you'll hit one

- **Pull** into your branch and someone changed a cell you also changed.
- **Merge `main`** into your feature branch (Module 04 step 5) with overlapping
  edits.
- The **PR** shows "this branch has conflicts" in the provider.

The Git dialog reports it: the operation stops and the conflicted files are
flagged.

## Resolving in the Git dialog

Databricks shows the conflicted file with the two versions and lets you produce
the final content:

1. Open the conflicted notebook / file from the Git dialog's conflict view.
2. You'll see the conflict regions — the same `<<<<<<<` / `=======` /
   `>>>>>>>` markers from the Git course, wrapped around the disputed lines
   **in the source form** of the notebook.
3. Edit to the final desired content. **Delete all three marker lines.** For a
   notebook, make sure each cell still starts/ends cleanly at its
   `# COMMAND ----------` boundaries — a stray marker left inside a cell will
   break the notebook.
4. Mark resolved / **Commit** the resolution from the dialog.

> The in-dialog conflict experience has improved over time and varies by
> workspace version. If it feels clumsy or you can't get a clean result, use one
> of the fallbacks below — that's a normal choice, not a failure.

## Fallback 1 — resolve in the provider

GitHub and GitLab both have a **web conflict editor** on the PR/MR when the
conflict is simple (a few lines). Resolve there, then **Pull** in the Git dialog
to bring the resolution back. (Git course / GitLab course Module 06.)

## Fallback 2 — resolve at a git CLI

The Git folder is a real clone. From a **web terminal** or a **local clone** of
the same repo:

```bash
git switch my-branch
git fetch
git merge origin/main
# ... edit the conflicted .py notebook files, remove markers ...
git add path/to/notebook.py
git commit
git push
```

Then **Pull** in the Databricks Git dialog. This is the most reliable route for
anything non-trivial, and gives you `git merge --abort` if you want to back out.

## Fallback 3 — start the branch over

If your branch is small and the conflict is nasty, it can be faster to:

1. Note what your branch changed.
2. Create a fresh branch from an up-to-date `main`.
3. Re-apply your changes.
4. Push, open a new PR, close the old one.

Not elegant, but for a two-notebook change it's often quickest.

## Recovery — getting back to safety

### Discard uncommitted changes

Git dialog → **⋯ → Discard changes**. Reverts tracked files to the last commit
on the current branch. Loses uncommitted work only.

CLI: `git restore .` / `git reset --hard`

### Undo a bad commit that you pushed

Same rule as the Git course, Module 04: if it's **pushed/shared, use
`git revert`** (a new commit that undoes it), not `reset`. Do this from a
terminal or via the provider (GitHub/GitLab both have a "Revert" button on a
merged PR):

```bash
git revert <sha>
git push
```

Then Pull in Databricks.

### "I reset/rebased and lost commits"

`git reflog` from a terminal on the clone (or a local clone) — same recovery as
the Git course. Committed work is almost always still there.

### The Git folder itself is broken

Push your branch if you can, then **delete the Git folder and re-create it** from
the URL (Module 03). The clone holds nothing irreplaceable.

### Databricks notebook revision history

Independent of git, Databricks keeps a per-notebook revision history (sidebar
clock icon). If you lost an *uncommitted* notebook edit via a bad Discard or
branch switch, check there — you may be able to restore the cell content, then
re-commit it properly.

## Reducing conflicts

- **Small, short-lived branches** — the biggest lever.
- **Pull `main` into your branch often** so you're never far behind.
- **One notebook per concern.** A 40-cell mega-notebook that everyone edits is a
  conflict magnet. Split it; factor logic into modules (Module 11).
- **Agree on notebook format** (Source) so formatting churn doesn't collide.
- **Don't reformat/reorder cells** in the same commit as a logic change.

## Check yourself

1. Why can a leftover conflict marker be worse in a notebook `.py` file than in
   an ordinary script?
2. Your PR shows a simple 3-line conflict. Name two places you could resolve it.
3. A commit that's already merged to `main` broke a job. `reset` or `revert`,
   and where do you run it?
4. You discarded changes by accident and lost an hour of uncommitted notebook
   edits. Any hope?

<details>
<summary>Answers</summary>

1. A stray `=======` or `<<<<<<<` inside a cell can break the notebook's cell
   structure / make it fail to parse, not just leave a bad line — the
   `# COMMAND ----------` boundaries have to stay intact.
2. The provider's web conflict editor on the PR, or a git CLI (web terminal or
   local clone) followed by a Pull in Databricks. (The Git dialog itself is a
   third.)
3. `git revert <sha>` (never `reset` on shared history) — from a terminal on a
   clone, or via the provider's "Revert" button on the merged PR, then Pull in
   Databricks.
4. Maybe — check the notebook's Databricks **revision history** (clock icon),
   which is separate from git and may hold the last auto-saved state. Recover
   the cell content there, then commit it properly.

</details>

Next: [Module 06 — A collaboration workflow](06-collaboration-workflow.md)
