# Exercise 05 — Solution

## Setup

```bash
cd ~
mkdir undo-lab && cd undo-lab
git init
for n in 1 2 3 4 5; do
  echo "line $n" >> story.md
  git add story.md
  git commit -m "Add line $n"
done
```

## Part 1

### 1. `git restore`

```bash
echo "line 6 (oops)" >> story.md
git diff                       # + line 6 (oops)
git restore story.md
git diff                       # nothing — line is gone for good
```

### 2. `git restore --staged`

```bash
echo "line 6 (real)" >> story.md
git add story.md
git status                     # Changes to be committed: modified: story.md
git restore --staged story.md
git status                     # Changes not staged for commit: modified: story.md
git diff                       # + line 6 (real) — still there
git commit -am "Add line 6"
```

## Part 2

### 3. `--amend` message

```bash
git commit --amend -m "Add line 6 to the story"
git log --oneline              # message changed, hash changed, count unchanged
```

### 4. `--amend --no-edit` to add a file

```bash
echo "# My Story" > title.md
git add title.md
git commit --amend --no-edit
git show HEAD --stat
```

```
 story.md | 1 +
 title.md | 1 +
 2 files changed, 2 insertions(+)
```

### 5. The three resets

```bash
echo "draft a" >> scratch.md && git add scratch.md && git commit -m "wip a"
echo "draft b" >> scratch.md && git commit -am "wip b"
echo "draft c" >> scratch.md && git commit -am "wip c"
```

**5a — soft:**

```bash
git reset --soft HEAD~1
git status        # modified: scratch.md  (Changes to be COMMITTED)
git log --oneline # no "wip c"
git commit -m "wip c again"
```

**5b — mixed:**

```bash
git reset HEAD~1
git status        # modified: scratch.md  (Changes NOT STAGED)
git log --oneline # no "wip c again"
git commit -am "wip c yet again"
```

**5c — hard:**

```bash
git reset --hard HEAD~1
git status        # clean
git log --oneline # no "wip c yet again"
cat scratch.md    # the "draft c" line is GONE from the file too
```

Collapse remaining wip commits (`wip a`, `wip b` — two of them):

```bash
git reset --soft HEAD~2
git commit -m "Add scratch draft"
git log --oneline
```

```
<hash> Add scratch draft
<hash> Add line 6 to the story
<hash> Add line 5
...
```

### 6. `git revert`

```bash
git revert HEAD          # editor opens with "Revert \"Add scratch draft\"" — save
git log --oneline
```

```
<hash> Revert "Add scratch draft"
<hash> Add scratch draft
<hash> Add line 6 to the story
...
```

```bash
cat scratch.md          # empty / file removed — effect undone
```

Both commits are in history. `revert` never removes anything; it adds an
inverse commit. Safe to push.

### 7. `git reflog`

```bash
git reflog
```

```
a1b2c3d HEAD@{0}: revert: Revert "Add scratch draft"
e4f5a6b HEAD@{1}: commit: Add scratch draft
...
9c8d7e6 HEAD@{5}: commit: wip c yet again
7a6b5c4 HEAD@{6}: reset: moving to HEAD~1
1f2e3d4 HEAD@{7}: commit: wip c yet again
...
```

Find `wip c yet again` (say `HEAD@{5}`):

```bash
git branch rescued HEAD@{5}
git log --oneline rescued        # the "lost" commit is right there
git branch -D rescued            # cleanup
```

The point: `reset --hard` moved a *label*; the commit object stayed in the repo,
reachable via reflog for weeks. Uncommitted working-dir changes are the only
thing genuinely lost.

## Part 3

### 8. `git clean`

```bash
echo x > junk.txt
mkdir tmp && echo y > tmp/y.txt
git status                       # junk.txt, tmp/ untracked

git clean -nd
#  Would remove junk.txt
#  Would remove tmp/

git clean -fd
#  Removing junk.txt
#  Removing tmp/
```

`-n` dry run, `-f` force (required to actually delete), `-d` include
directories. Always run `-nd` first.

## Recap table

| Situation | Command | Recoverable after? |
| --- | --- | --- |
| Unstaged edit to discard | `git restore <file>` | No |
| Unstage, keep edit | `git restore --staged <file>` | n/a (nothing lost) |
| Bad last commit message (unpushed) | `git commit --amend -m "..."` | old commit via reflog |
| Forgot a file in last commit | `git add f && git commit --amend --no-edit` | via reflog |
| Undo commit, keep work staged | `git reset --soft HEAD~1` | commit via reflog |
| Undo commit, keep work unstaged | `git reset HEAD~1` | commit via reflog |
| Undo commit and its changes | `git reset --hard HEAD~1` | commit via reflog; working edits NO |
| Undo a pushed commit | `git revert <hash>` | n/a (adds a commit) |
| Find a "lost" commit | `git reflog` → `git branch x HEAD@{n}` | — |
| Delete untracked files | `git clean -nd` then `git clean -fd` | No |
