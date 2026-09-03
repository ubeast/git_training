# Exercise 05 — Undo lab

**After:** Module 04 (do part 2 again after Module 07) · **Time:** ~30 min

## Goal

Run every recovery move from Module 04 on a repo you don't care about, so that
when you need them for real you're not guessing. The theme: **git is a safety
net.**

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
git log --oneline        # 5 commits: "Add line 5" ... "Add line 1"
```

Keep `git log --oneline` and `git status` running after every step.

## Part 1 — working directory & staging

### 1. Discard an unstaged edit — `git restore`

- Append `line 6 (oops)` to `story.md`. Don't stage it.
- `git diff` shows the new line.
- `git restore story.md`.
- `git diff` is empty; the line is gone. **This one is not recoverable** — it
  was never staged or committed.

### 2. Unstage without losing the edit — `git restore --staged`

- Append `line 6 (real)` to `story.md`. This time `git add story.md`.
- `git status` — "Changes to be committed".
- `git restore --staged story.md`.
- `git status` — the edit is back to "not staged", but `git diff` shows it's
  **still there**. Nothing lost.
- Commit it: `git commit -am "Add line 6"`. (6 commits now.)

## Part 2 — commits (not yet pushed)

### 3. Fix the last commit's message — `--amend`

- `git commit --amend -m "Add line 6 to the story"`.
- `git log --oneline` — same number of commits, new message. The hash changed
  (it's a new commit replacing the old).

### 4. Add a forgotten file to the last commit — `--amend --no-edit`

- Create `title.md` with `# My Story`. You *meant* to include it in the last
  commit.
- `git add title.md`
- `git commit --amend --no-edit`
- `git show HEAD --stat` — the last commit now contains both `story.md` and
  `title.md`.

### 5. The three resets

Make three throwaway commits to practise on:

```bash
echo "draft a" >> scratch.md && git add scratch.md && git commit -m "wip a"
echo "draft b" >> scratch.md && git commit -am "wip b"
echo "draft c" >> scratch.md && git commit -am "wip c"
git log --oneline        # wip c, wip b, wip a on top
```

**5a — `--soft`:** `git reset --soft HEAD~1`.
`git status` — "wip c" is undone; its change is **staged**. `git log` — "wip c"
gone. Re-commit: `git commit -m "wip c again"`.

**5b — `--mixed` (default):** `git reset HEAD~1`.
`git status` — change is present but **unstaged**. `git log` — commit gone.
Re-add and commit: `git commit -am "wip c yet again"`.

**5c — `--hard`:** `git reset --hard HEAD~1`.
`git status` — **clean**. `git log` — commit gone. The `scratch.md` edit from
that commit is **gone from your working directory too**. (The commit itself
still exists — see step 7.)

Now collapse the wip commits into one:

```bash
git log --oneline                       # note how many "wip" commits remain
git reset --soft HEAD~2                  # adjust the number to your wip count
git commit -m "Add scratch draft"
git log --oneline
```

### 6. Undo a commit the safe way — `git revert`

- `git revert HEAD` — git makes a **new** commit undoing "Add scratch draft".
  Accept the default message.
- `git log --oneline` — the bad commit is still there, plus a new "Revert..."
  commit above it.
- `ls` / `cat scratch.md` — the effect is undone, history is intact. This is
  what you use once something is pushed.

### 7. Recover "lost" commits — `git reflog`

- `git reflog` — a list of every position `HEAD` has held, including the commits
  your resets "removed."
- Find the entry for `wip c` (or `wip c again`). Note its `HEAD@{n}`.
- `git branch rescued HEAD@{n}` — creates a branch pointing at that "lost"
  commit.
- `git log --oneline rescued` — there it is. Nothing was truly gone.
- Clean up: `git branch -D rescued`.

## Part 3 — untracked files

### 8. `git clean`

- Create junk: `echo x > junk.txt && mkdir tmp && echo y > tmp/y.txt`.
- `git status` — untracked.
- `git clean -nd` — **preview** what would be deleted (the `-n` = dry run).
- `git clean -fd` — actually delete them. Irreversible.

## Verify checklist

- [ ] You saw `git restore` permanently discard an unstaged edit (step 1)
- [ ] You saw `git restore --staged` keep the edit while unstaging (step 2)
- [ ] `git show HEAD --stat` proves `--amend` folded `title.md` into the last
      commit (step 4)
- [ ] You can state what `--soft`, `--mixed`, `--hard` each do to the changes
      (step 5)
- [ ] `git revert` added a new commit rather than removing one (step 6)
- [ ] `git reflog` + a branch recovered a commit that `reset --hard` "deleted"
      (step 7)
- [ ] `git clean -nd` previewed before `git clean -fd` deleted (step 8)

## The summary you should be able to recite

| Bad thing is... | Tool |
| --- | --- |
| unstaged edit | `git restore <file>` (loses it) |
| staged, want to keep edit | `git restore --staged <file>` |
| last commit, not pushed | `git commit --amend` / `git reset` |
| several commits, not pushed | `git reset` (`--soft` keeps staged, `--hard` discards) |
| already pushed | `git revert` |
| a command you regret | `git reflog` + `git reset --hard HEAD@{n}` |
| untracked junk | `git clean -nd` then `-fd` |

Compare with [`SOLUTION.md`](SOLUTION.md).
