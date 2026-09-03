# Exercise 04 — Remotes (fully offline)

**After:** Module 07 · **Time:** ~30 min

## Goal

Practise `clone`, `push`, `pull`, and recovering from a rejected push — using a
"server" that's just another folder on your own machine. **No network, no
accounts.**

## The idea

A remote is just a repository somewhere else. That "somewhere else" can be a
folder on your own disk. We'll make a **bare** repo (one with no working
directory — only the `.git` internals, which is what servers use) and treat it
as the server. Then we'll make two clones — `alice` and `bob` — and have them
step on each other on purpose.

```
~/remotes-lab/
  server.git/      ← the "remote" (bare)
  alice/           ← clone 1
  bob/             ← clone 2  (you'll play both people)
```

## Setup

### 1. Make the "server"

```bash
cd ~
mkdir remotes-lab && cd remotes-lab
git init --bare server.git
```

`ls server.git` — note there's no working copy, just `HEAD`, `config`,
`objects/`, `refs/`. That's a bare repo.

### 2. Seed it via the first clone

```bash
cd ~/remotes-lab
git clone server.git alice
cd alice
git status                       # "No commits yet" — empty repo cloned fine
echo "# Shared Notes" > notes.md
git add notes.md
git commit -m "Add notes file"
git push -u origin main          # push the first commit to the server
```

`git remote -v` — `origin` points at `~/remotes-lab/server.git`.

### 3. Second clone

```bash
cd ~/remotes-lab
git clone server.git bob
cd bob
ls                               # notes.md is here — bob got it from the server
git log --oneline                # shows Alice's commit
```

## Tasks

### 4. A clean round-trip

- As **bob**: add a line to `notes.md`, commit as `Add meeting time`, and
  `git push`.
- Switch to **alice** (`cd ../alice`). Run `git log --oneline` — you do **not**
  see bob's commit yet. Why?
- Run `git fetch`. Now run `git log --oneline origin/main` — bob's commit shows
  on `origin/main` but still not on alice's `main`.
- Run `git status` — it says alice's `main` is "behind 'origin/main' by 1
  commit". Run `git pull` (or `git merge origin/main`) to catch up.

### 5. Cause a rejected push

- As **alice**: add a line to `notes.md` (`Agenda: Q3 planning`), commit as
  `Add agenda`. **Don't push yet.**
- Switch to **bob**: add a *different* line to `notes.md` (`Location: Room 4`),
  commit as `Add location`, and `git push`. This succeeds.
- Switch back to **alice**: `git push`.

You should get:

```
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '.../server.git'
```

### 6. Recover from the rejection

- As **alice**, run `git pull`.
  - If alice's and bob's lines are far enough apart in the file, this
    auto-merges and creates a merge commit — accept the default message.
  - If they're on adjacent lines, you get a **conflict** — resolve it (keep both
    lines), `git add notes.md`, `git commit`.
- Now `git push` — it succeeds.
- Switch to **bob**, `git pull` — bob now has alice's agenda line and the merge
  commit.

### 7. A branch and its remote

- As **bob**: `git switch -c cleanup`, delete a line or tidy the file, commit,
  then `git push -u origin cleanup`.
- As **alice**: `git fetch`, then `git branch -a` (note `remotes/origin/cleanup`
  appears). `git switch cleanup` — git auto-creates a local branch tracking it.
- As **alice**: merge `cleanup` into `main` locally, push `main`.
- As **bob**: delete the remote branch: `git push origin --delete cleanup`.
- Both: `git fetch --prune` and confirm `origin/cleanup` is gone from
  `git branch -a`.

## Verify checklist

- [ ] `~/remotes-lab/server.git` is a bare repo (no working files)
- [ ] Both `alice` and `bob` have `origin` → the `server.git` path
- [ ] You can explain why alice didn't see bob's commit until `git fetch`/`pull`
- [ ] You reproduced the `! [rejected] ... (fetch first)` error
- [ ] You recovered it with `git pull` then `git push` (no `--force`)
- [ ] `git log --oneline --graph` in `alice` shows a merge commit joining
      alice's and bob's work
- [ ] The `cleanup` branch was pushed, merged, deleted, and pruned everywhere

## The one rule

When a push is rejected: **`git pull`, resolve, `git push`.** Never
`git push --force` on a branch other people use.

Compare with [`SOLUTION.md`](SOLUTION.md).
