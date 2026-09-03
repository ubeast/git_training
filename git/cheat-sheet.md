# Git Cheat Sheet

One page. Print it. See the modules for the full explanations.

## The daily loop

```bash
git status                 # what's changed / staged — run constantly
git add <file>             # stage a file for the next commit
git add -p                 # stage selected chunks interactively
git add .                  # stage everything under the current folder
git commit -m "message"    # save the staged snapshot
git commit -am "message"   # stage all TRACKED changes + commit (skips new files)
```

## Setup (once per machine)

```bash
git config --global user.name  "Your Name"
git config --global user.email "you@example.com"
git config --global init.defaultBranch main
git config --global pull.rebase false
git config --global core.editor "code --wait"      # or "nano"
git config --global alias.lg "log --oneline --graph --decorate --all"
```

## Starting a repo

```bash
git init                          # new repo here
git clone <url>                   # copy a remote repo
git remote add origin <url>       # connect existing local repo to a server
git push -u origin main           # first push, links the branch
```

## Looking around

```bash
git log --oneline --graph --decorate --all   # or: git lg
git log --oneline -5                          # last 5
git log --oneline -- <file>                   # commits touching a file
git show <commit>                             # one commit, full diff
git show <commit>:<file>                      # a file's contents at that commit
git diff                                      # working dir vs staged
git diff --staged                             # staged vs last commit (pre-commit review)
git diff <a> <b>                              # between two commits/branches
git blame <file>                              # who last changed each line
```

Commit references: `HEAD` (now), `HEAD~1` (parent), `HEAD~3` (three back),
`a1b2c3d` (by hash).

## Branching & merging

```bash
git branch                     # list
git switch -c <name>           # create + switch
git switch <name>              # switch
git switch -                   # switch to previous branch
git merge <name>               # merge <name> INTO current branch
git merge --abort              # cancel an in-progress merge
git branch -d <name>           # delete a merged branch
git stash / git stash pop      # shelve / restore uncommitted work
```

## Remotes

```bash
git remote -v                  # list remotes
git fetch                      # download, don't touch my files
git pull                       # fetch + merge into current branch
git push                       # upload commits
git push -u origin <branch>    # push a new branch and link it
git push origin --delete <b>   # delete a remote branch
git fetch --prune              # clear stale origin/* pointers
```

Push rejected ("fetch first")? → `git pull`, resolve, `git push`. **Never**
`git push --force` on a shared branch.

## Merge conflict — the process

```
<<<<<<< HEAD           your current branch's version
=======
>>>>>>> other-branch   the incoming version
```

1. Edit the file to the final desired content.
2. Delete all `<<<<<<<`, `=======`, `>>>>>>>` lines.
3. `git add <file>` for each resolved file.
4. `git commit` (pre-filled message is fine).

Bail out: `git merge --abort`.

## "How do I undo X?"

| I want to... | Command | Loses work? |
| --- | --- | --- |
| Discard unstaged edits to a file | `git restore <file>` | Yes — those edits |
| Discard all unstaged edits | `git restore .` | Yes — those edits |
| Unstage a file (keep the edit) | `git restore --staged <file>` | No |
| Fix the last commit's message | `git commit --amend -m "new msg"` | No (don't if pushed) |
| Add a forgotten file to the last commit | `git add <f>` then `git commit --amend --no-edit` | No (don't if pushed) |
| Undo last commit, keep changes staged | `git reset --soft HEAD~1` | No |
| Undo last commit, keep changes unstaged | `git reset HEAD~1` | No |
| Undo last commit **and** the changes | `git reset --hard HEAD~1` | Yes — working changes |
| Squash last 3 commits into one | `git reset --soft HEAD~3` then `git commit` | No |
| Undo a commit that's already pushed/shared | `git revert <commit>` | No (adds a new commit) |
| Remove untracked files/folders | `git clean -nd` (preview) → `git clean -fd` | Yes — those files |
| Recover after a bad `reset`/`amend` | `git reflog`, then `git reset --hard HEAD@{n}` | Recovers commits |
| Throw away a file's history since a commit | `git checkout <commit> -- <file>` then commit | Replaces current version |
| Go look at an old version, read-only | `git switch --detach <commit>` … `git switch main` | No |

## When git surprises you

1. **Stop.** Don't run more mutating commands.
2. `git status` and `git log --oneline` — understand the current state.
3. Committed work is almost always recoverable: `git reflog`.
4. Ask for help before experimenting further.
