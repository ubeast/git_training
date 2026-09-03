# Module 04 — The everyday Git loop in Databricks

The Git dialog is a GUI for `git`. This module is the loop you'll run dozens of
times a day, with the CLI equivalent beside each step.

## Opening the Git dialog

In a Git folder (or a notebook inside one), click the **branch name / Git
button** in the header. The dialog shows:

- the **current branch** and a branch selector,
- **Changes** — a list of added / modified / deleted files with per-file diffs,
- a **commit message** box,
- **Commit & Push**, **Pull**, **Create Branch**, and (`⋯`) more actions.

## The loop

### 1. Start on an up-to-date main

```
Git dialog → branch selector → main
Git dialog → Pull
```

CLI: `git switch main && git pull`

### 2. Create a branch

```
Git dialog → Create Branch → name it "42-add-weekly-rollup" → Create
```

CLI: `git switch -c 42-add-weekly-rollup`

The new branch is created **from the branch you're currently on** — so pull
`main` first (step 1). You're automatically switched to the new branch.

> **Branch naming**: match your team's convention. `<issue>-<slug>` is common.
> The "Create branch" action on a GitHub issue / GitLab issue also works — then
> just switch to that branch in the Git dialog.

### 3. Edit notebooks and files

Work normally — edit notebook cells, add notebooks, edit `.py` modules. As you
save, the Git dialog's **Changes** list grows.

Each changed notebook shows a **diff** in the dialog: added/removed lines in the
source form (Module 02). Review it before committing — same discipline as
`git diff --staged`.

### 4. Commit & Push

```
Git dialog → write a commit message → Commit & Push
```

CLI: `git commit -am "Add weekly rollup notebook" && git push`

Notes:

- Databricks stages **all** changes in the Git folder and commits them together.
  There's **no partial staging** in the dialog — if you need to split changes
  into separate commits, either commit in stages (commit, change more, commit
  again) or use a terminal (`git add -p`).
- The first push of a new branch sets the upstream automatically (`git push -u`).
- The commit is attributed to your **linked git identity** (Module 01).
- After a successful push, Databricks often shows a **"Create pull request"**
  link straight to your provider.

### 5. Keep the branch current

If `main` moves while you work, pull it into your branch:

```
Git dialog → branch selector → main → Pull
Git dialog → branch selector → 42-add-weekly-rollup
Git dialog → ⋯ → Merge  (merges main into your branch)
```

or, more simply, some UIs offer **⋯ → Pull** with a "merge main" style option,
or you rebase/merge from a terminal. The goal is the same as the Git course,
Module 08: resolve any conflict on **your** branch, before the PR.

CLI: `git switch 42-add-weekly-rollup && git merge origin/main`

### 6. Open the PR

Click the **Create pull request** link (or go to the provider). From here it's
ordinary git provider workflow — the [GitLab course](../../gitlab/) Modules 05–06
or the equivalent on GitHub. Review, approve, merge **in the provider**.

### 7. After the merge

```
Git dialog → branch selector → main → Pull
```

Your merged work is now on `main` in the Git folder. Delete the local branch if
the dialog offers it, or leave it — it's just a label.

## Switching branches

The branch selector in the Git dialog switches the **whole Git folder** to that
branch — every notebook and file updates to that branch's version, just like
`git switch`.

- **Uncommitted changes block a switch** that would overwrite them. Commit them,
  or discard them (below), first. Databricks warns you.
- A notebook you have open will **reload** to the new branch's version. If
  you're mid-edit, save or commit first.

## Discarding changes

Git dialog → **⋯ → Discard changes** (or the per-file revert):

- Reverts the Git folder's tracked files to the last commit on the current
  branch.
- CLI equivalent: `git restore .` (and for a full reset, `git reset --hard`).
- **This loses uncommitted work** — the one genuinely destructive button in the
  dialog. Everything committed is still recoverable.

## When to drop to a terminal

The Git dialog covers ~90% of daily work. Use a **web terminal** (if your
workspace enables it — cluster **Apps/Web terminal**, then `cd` into the Git
folder path under `/Workspace/...`) or your **local git CLI** on a separate
clone for:

- Partial staging / crafting several commits from one messy working state
  (`git add -p`)
- Interactive rebase, cherry-pick, `git reflog` recovery
- Complex conflict resolution
- `git bisect`

The Git folder is a normal clone — any git command works on it from a terminal.

## Mapping table

| Git dialog | git CLI |
| --- | --- |
| Pull | `git pull` |
| Create Branch | `git switch -c <name>` |
| branch selector | `git switch <name>` |
| Commit & Push | `git commit -am "..."` && `git push` |
| ⋯ → Merge | `git merge <branch>` |
| ⋯ → Discard changes | `git restore .` / `git reset --hard` |
| (open a file's diff) | `git diff` |
| Create pull request link | open the provider's "new PR" page |

## Check yourself

1. You want your next two commits to be separate logical changes. The Git dialog
   commits everything at once — how do you get two commits?
2. You try to switch branches and Databricks won't let you. Why, and what are
   your two options?
3. Where do you actually merge a pull request?
4. Which button in the Git dialog can lose work, and what work?

<details>
<summary>Answers</summary>

1. Commit the first set of changes, then make the rest of your edits and commit
   again — or use a terminal with `git add -p` for true partial staging. The
   dialog has no partial staging.
2. You have uncommitted changes that switching would overwrite. Either commit
   them (to the current branch) or discard them, then switch.
3. In your git provider (GitHub / GitLab / Azure DevOps), not in Databricks.
4. **Discard changes** (⋯ menu) — it reverts tracked files to the last commit,
   losing any uncommitted edits. Committed work is safe.

</details>

Next: [Module 05 — Conflicts & recovery](05-conflicts-and-recovery.md)
