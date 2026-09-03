# Module 03 — Looking at history

Now that you have a few commits, learn to read them. These commands are all
**read-only** — none of them change anything, so explore freely.

## `git log` — the list of commits

```bash
git log
```

```
commit 7f3a9c1d5e... (HEAD -> main)
Author: Your Name <you@example.com>
Date:   Mon Sep 1 10:15:02 2026 +0000

    Add pancake method

commit 2b8e04a...
Author: Your Name <you@example.com>
Date:   Mon Sep 1 10:11:44 2026 +0000

    Add pancakes and omelette recipes

...
```

Newest first. Press `q` to quit the pager, `Space` to page down.

### Make it readable

```bash
git log --oneline
```

```
7f3a9c1 Add pancake method
2b8e04a Add pancakes and omelette recipes
a1b2c3d Add README with project title
```

Add structure for when branches appear (Module 05):

```bash
git log --oneline --graph --decorate --all
```

- `--graph` draws the branch structure on the left
- `--decorate` shows which branches/tags point where
- `--all` shows every branch, not just the current one

If you set the alias in Module 01, this is just `git lg`.

### Useful filters

```bash
git log --oneline -5                   # last 5 commits
git log --oneline --author="Jane"      # commits by Jane
git log --oneline --since="2 weeks ago"
git log --oneline -- pancakes.md       # commits that touched this file
git log --oneline --grep="fix"         # commits whose message mentions "fix"
```

## `HEAD` — "where you are now"

`HEAD` is a pointer. Almost always it points at the branch you're on, which
points at that branch's latest commit. You'll see `HEAD -> main` in log output.

You can refer to commits *relative to* `HEAD`:

| Reference | Means |
| --- | --- |
| `HEAD` | The current commit |
| `HEAD~1` or `HEAD~` | Its parent (one before) |
| `HEAD~2` | Two commits back |
| `HEAD~3` | Three back, and so on |

These work anywhere a command wants a commit.

## `git show` — one commit in full

```bash
git show HEAD            # the latest commit: message + full diff
git show HEAD~2          # three commits back
git show a1b2c3d         # by hash (first ~7 characters is enough)
git show HEAD:pancakes.md   # the contents of that file AT that commit
```

## `git diff` — compare any two points

`git diff` isn't just for uncommitted work. It compares whatever you give it:

```bash
git diff HEAD~2 HEAD              # what changed over the last 2 commits
git diff HEAD~2 HEAD -- pancakes.md   # ...just for one file
git diff a1b2c3d 7f3a9c1         # between two specific commits
git diff main other-branch        # between two branches (Module 05)
```

Reading a diff:

```diff
--- a/pancakes.md        ← the "before" version
+++ b/pancakes.md        ← the "after" version
@@ -1,2 +1,3 @@          ← "hunk header": before starts at line 1 (2 lines),
                            after starts at line 1 (3 lines)
 ## Pancakes             ← context line (unchanged), shown for orientation
 Flour, milk, eggs.
+Mix, then fry.          ← added line
```

## `git blame` — who last touched each line

```bash
git blame pancakes.md
```

```
a1b2c3d (Your Name 2026-09-01 10:11:44 +0000 1) ## Pancakes
2b8e04a (Your Name 2026-09-01 10:11:44 +0000 2) Flour, milk, eggs.
7f3a9c1 (Your Name 2026-09-01 10:15:02 +0000 3) Mix, then fry.
```

Each line is tagged with the commit that last changed it. Great for "why is this
line here?" — find the commit, then `git show <that hash>` for the full context
and message.

## Browsing an old version without changing anything

To *look at* the whole project as it was at an old commit:

```bash
git switch --detach a1b2c3d    # working dir now matches that commit
# ... look around ...
git switch main                # back to the present
```

You'll see a "detached HEAD" warning — that's fine here. It just means `HEAD`
points straight at a commit instead of a branch. Don't commit while detached
(Module 05 explains why); just switch back when done.

## Check yourself

1. What does `git log --oneline -- README.md` show?
2. What's the difference between `git show HEAD~1` and `git diff HEAD~1 HEAD`?
3. `HEAD~2` refers to what?
4. You want to know which commit introduced a specific weird line in a file.
   Which command starts you off?

<details>
<summary>Answers</summary>

1. A compact list of only the commits that changed `README.md`.
2. `git show HEAD~1` shows one commit (its message, author, and the diff *it*
   introduced). `git diff HEAD~1 HEAD` shows the combined difference between
   those two points — here they happen to be the same single commit's worth of
   change, but `git diff HEAD~5 HEAD` would show five commits combined.
3. The commit two steps back from where you are now (current commit's
   grandparent).
4. `git blame <file>` to find the commit for that line, then `git show <hash>`.

</details>

Next: [Module 04 — Undoing things](04-undoing-things.md)
