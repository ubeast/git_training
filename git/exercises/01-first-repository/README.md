# Exercise 01 — Your first repository

**After:** Module 02 · **Time:** ~20 min

## Goal

Build a repo from nothing and run the core loop — `status → add → commit` —
several times. Feel what the staging area does.

## Setup

Work in a scratch folder outside the training repo:

```bash
cd ~            # or anywhere that isn't the training repo
mkdir travel-journal
cd travel-journal
```

## Tasks

### 1. Make it a repository

- Turn this folder into a git repo.
- Run `git status`. You should see "No commits yet" and a clean tree.

### 2. First commit

- Create `README.md` containing one line: `# Travel Journal`.
- Check `git status` — the file should be **untracked**.
- Stage it. Check `git status` again — it should now be "to be committed".
- Commit it with the message: `Add README`.
- Confirm with `git status` (clean) and `git log --oneline` (one commit).

### 3. Add two entries as one commit

- Create `day-1.md` with a couple of lines about an imaginary trip.
- Create `day-2.md` with a couple more.
- Stage **both** and commit together with message `Add days 1 and 2`.
- `git log --oneline` should show two commits.

### 4. The staging-area checkpoint (do this carefully)

- Add a new line to the bottom of `day-1.md`.
- Run `git add day-1.md`.
- Now add **another** new line to `day-1.md` (after staging).
- Run `git status`.

**Question:** why does `day-1.md` appear in *two* sections at once? Write down
your answer before continuing.

- Run `git diff` and `git diff --staged`. Note which change each one shows.
- Stage the file again so both new lines are included, then commit as
  `Expand day 1`.

### 5. Ignore some noise

- Create a file `notes.tmp` with any content, and a folder `.cache/` with a
  file in it (`mkdir .cache && echo x > .cache/x`).
- `git status` shows both as untracked.
- Create a `.gitignore` that excludes `*.tmp` and `.cache/`.
- `git status` should now show only `.gitignore` as untracked (the other two are
  ignored).
- Commit the `.gitignore` as `Add .gitignore`.

### 6. Rename and delete

- Rename `day-2.md` to `day-two.md` using a git command.
- Delete `day-1.md` using a git command... actually **keep day-1**, delete
  `notes.tmp` from disk instead (it's ignored, so this is just `rm notes.tmp` —
  no git involved). Confirm `git status` stays clean-ish.
- Commit the rename as `Rename day-2`.

## Verify

```bash
git log --oneline
```

You should have **5 commits**, newest first roughly:

```
<hash> Rename day-2
<hash> Add .gitignore
<hash> Expand day 1
<hash> Add days 1 and 2
<hash> Add README
```

```bash
git status                 # clean working tree
ls                         # README.md, day-1.md, day-two.md, .gitignore, .cache/
git show HEAD --stat       # shows the rename day-2.md -> day-two.md
```

## Verify checklist

- [ ] `git log --oneline` shows 5 commits with sensible messages
- [ ] Working tree is clean (`git status`)
- [ ] `day-two.md` exists; `day-2.md` does not
- [ ] `git check-ignore -v .cache/x` reports it's ignored by your `.gitignore`
- [ ] You can explain in one sentence why a file showed in two `git status`
      sections in task 4

## If you get stuck

- Wrong commit message? `git commit --amend -m "better message"` (only the most
  recent).
- Committed something you didn't mean to? `git reset --soft HEAD~1` and redo.
- Totally wedged? `cd ~ && rm -rf travel-journal` and start over — no shame.

Compare with [`SOLUTION.md`](SOLUTION.md) when done.
