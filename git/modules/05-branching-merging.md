# Module 05 — Branching & merging

Branches are what make git powerful. They let you work on something without
disturbing the known-good version, then fold it back in when it's ready.

[Exercise 02](../exercises/02-branching/) practises this end to end.

## What a branch actually is

A branch is just a **movable label pointing at a commit**. That's it. Creating a
branch doesn't copy any files — it writes a tiny file containing one commit hash.

```
a1b2c3d ── 2b8e04a ── 7f3a9c1   ← main points here
                          ▲
                         HEAD    (you are on main)
```

When you commit, the current branch label moves forward to the new commit. If
you're on a different branch, *that* label moves and `main` stays put. That's
how two lines of work stay separate.

## Seeing and creating branches

```bash
git branch                 # list branches; * marks the current one
git branch add-desserts    # create a branch (does NOT switch to it)
git switch add-desserts     # switch to it
```

Shortcut — create and switch in one step:

```bash
git switch -c add-desserts
```

> You may see `git checkout` in older material: `git checkout -b add-desserts`
> is the same as `git switch -c add-desserts`. `switch` and `restore` are the
> newer, clearer split of what `checkout` used to do. This course uses `switch`.

## Work on the branch

```bash
git switch -c add-desserts

echo "## Brownies" > brownies.md
echo "Chocolate, butter, sugar, eggs, flour." >> brownies.md
git add brownies.md
git commit -m "Add brownies recipe"

echo "## Ice cream" > icecream.md
git add icecream.md
git commit -m "Add ice cream recipe"
```

Now:

```
a1b2c3d ── 2b8e04a ── 7f3a9c1           ← main
                          \
                           d4f5a6b ── e7c8d9a   ← add-desserts  (HEAD)
```

`main` is untouched. Switch back and look:

```bash
git switch main
ls                    # brownies.md and icecream.md are GONE from the folder
git switch add-desserts
ls                    # ...and back
```

Switching branches rewrites your working directory to match that branch. (Git
won't let you switch if you have uncommitted changes that would be overwritten —
commit or stash them first; see below.)

## Merging: bring the branch's work into `main`

You **merge into the branch you're currently on**. So switch to the destination
first:

```bash
git switch main
git merge add-desserts
```

### Case 1: fast-forward

If `main` hasn't moved since you branched, git can just slide the `main` label
forward to catch up. No new commit needed:

```
Updating 7f3a9c1..e7c8d9a
Fast-forward
 brownies.md | 2 ++
 icecream.md | 1 +
```

```
a1b2c3d ── 2b8e04a ── 7f3a9c1 ── d4f5a6b ── e7c8d9a   ← main, add-desserts
```

### Case 2: a real merge commit

If `main` *did* get its own commits while you were on the branch, the two lines
have genuinely diverged. Git combines them and records a **merge commit** with
*two* parents:

```
a1b2c3d ── 7f3a9c1 ──── m3n4o5p ──────── M   ← main
                 \                       /
                  d4f5a6b ── e7c8d9a ────    (add-desserts)
```

Git opens your editor for the merge commit message — the default text is fine;
save and close. If the same lines were edited on both sides, you get a
**conflict** — that's all of [Module 06](06-merge-conflicts.md).

## Clean up

Once merged, the branch label has done its job:

```bash
git branch -d add-desserts     # -d = delete, refuses if not merged
```

The commits stay in history (now reachable from `main`); only the label goes.

## `git stash` — a shelf for unfinished work

You're mid-edit on `main` and need to switch branches, but you're not ready to
commit:

```bash
git stash              # shelves all uncommitted changes; working dir goes clean
git switch other-branch
# ... do the urgent thing ...
git switch main
git stash pop          # bring the changes back, remove them from the stash
```

`git stash list` shows what's shelved. Treat the stash as short-term only — it's
easy to forget things there.

## Fast-forward vs merge commit — which do you want?

- **Fast-forward** keeps history linear and tidy, but loses the visible record
  that a set of commits belonged to one feature.
- **Merge commit** (`git merge --no-ff`) always records the join, so history
  shows "this clump of work came in together." Many teams require this on
  `main`.

For this course, accept whichever git gives you. Just know the difference
exists — it comes up in team settings and in [Module 08](08-collaboration-workflow.md).

## Check yourself

1. Does `git branch new-thing` change which branch you're on?
2. You're on `main`. You run `git merge feature`. Which branch's label moves?
3. Why did your merge complete without creating a merge commit?
4. You have uncommitted changes and need to switch branches for five minutes
   without committing. What do you do?

<details>
<summary>Answers</summary>

1. No — it only creates the label. Use `git switch new-thing` (or
   `git switch -c new-thing` to do both).
2. `main` moves (it's the branch you're on and merging *into*). `feature` stays
   where it is.
3. It was a fast-forward: `main` had no commits of its own since the branch
   point, so git just advanced the `main` label to the feature's tip.
4. `git stash`, switch and do the work, switch back, `git stash pop`.

</details>

Next: [Module 06 — Merge conflicts](06-merge-conflicts.md)
