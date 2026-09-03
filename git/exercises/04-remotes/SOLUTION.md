# Exercise 04 — Solution

Throughout: `cd ~/remotes-lab/alice` and `cd ~/remotes-lab/bob` switch between
the two "people." Watch your shell prompt so you know which one you're in.

## Setup

```bash
cd ~
mkdir remotes-lab && cd remotes-lab
git init --bare server.git

git clone server.git alice
cd alice
echo "# Shared Notes" > notes.md
git add notes.md
git commit -m "Add notes file"
git push -u origin main

cd ~/remotes-lab
git clone server.git bob
```

## 4. Clean round-trip

```bash
cd ~/remotes-lab/bob
echo "Meeting: Thursday 10:00" >> notes.md
git commit -am "Add meeting time"
git push

cd ~/remotes-lab/alice
git log --oneline               # only "Add notes file" — bob's commit not here
```

**Why?** Git never contacts the remote on its own. Alice's repo only knows what
it knew at the last sync. `origin/main` in alice's repo still points at the
first commit.

```bash
git fetch
git log --oneline origin/main   # NOW shows "Add meeting time"
git log --oneline main          # still doesn't
git status                      # "Your branch is behind 'origin/main' by 1 commit"
git pull                        # fast-forwards main to catch up
git log --oneline               # both commits now
```

## 5. Rejected push

```bash
cd ~/remotes-lab/alice
echo "Agenda: Q3 planning" >> notes.md
git commit -am "Add agenda"
# do NOT push

cd ~/remotes-lab/bob
git pull                        # get alice's earlier state first (has "Add meeting time")
echo "Location: Room 4" >> notes.md
git commit -am "Add location"
git push                        # succeeds — bob was up to date

cd ~/remotes-lab/alice
git push
```

```
To /Users/you/remotes-lab/server.git
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs to '/Users/you/remotes-lab/server.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref.
```

The server's `main` moved (bob's push) since alice last synced, so alice's push
would lose bob's commit. Git refuses.

## 6. Recover

```bash
git pull
```

Both appended near the end of `notes.md`, so this likely conflicts:

```
Auto-merging notes.md
CONFLICT (content): Merge conflict in notes.md
```

`notes.md`:

```
# Shared Notes
Meeting: Thursday 10:00
<<<<<<< HEAD
Agenda: Q3 planning
=======
Location: Room 4
>>>>>>> <hash>
```

Resolve — keep both:

```
# Shared Notes
Meeting: Thursday 10:00
Agenda: Q3 planning
Location: Room 4
```

```bash
git add notes.md
git commit                      # default merge message
git push                        # succeeds now
```

```bash
cd ~/remotes-lab/bob
git pull
git log --oneline --graph       # bob sees alice's agenda + the merge commit
```

> If your two lines had landed far apart, `git pull` would auto-merge with no
> conflict and just make a merge commit. Same lesson: pull integrates, then you
> can push.

## 7. Branch and its remote

```bash
cd ~/remotes-lab/bob
git switch -c cleanup
printf '# Shared Notes\nMeeting: Thursday 10:00\nAgenda: Q3 planning\nLocation: Room 4\n' > notes.md
git commit -am "Normalise notes formatting"
git push -u origin cleanup

cd ~/remotes-lab/alice
git fetch
git branch -a
#   * main
#     remotes/origin/cleanup
#     remotes/origin/main
git switch cleanup              # "branch 'cleanup' set up to track 'origin/cleanup'"
git switch main
git merge cleanup
git push

cd ~/remotes-lab/bob
git push origin --delete cleanup

# both repos:
git fetch --prune
git branch -a                   # no origin/cleanup anymore
```

## Verify

```bash
cd ~/remotes-lab/alice && git log --oneline --graph --all
```

Shows the linear early history, a fork where alice/bob diverged, a merge commit
joining them, then the `cleanup` work merged in.

## Key takeaways

- A remote is just another repo — even a local folder. `--bare` = no working
  copy, which is what a server uses.
- `origin/main` is alice's *cached* idea of the server's `main`. It only updates
  on `fetch`/`pull`/`push`/`clone`.
- `fetch` = safe download. `pull` = fetch + merge into your branch.
- Rejected push = the remote moved under you. Fix: `git pull`, resolve, `git
  push`. Never `--force` a shared branch.
- `git switch <name>` for a branch that exists only on the remote auto-creates a
  local tracking branch.
- `git push origin --delete <b>` + `git fetch --prune` cleans up a merged
  branch everywhere.
