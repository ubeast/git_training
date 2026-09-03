# Git Training

A hands-on introduction to Git for people who have **never used version control
before**. By the end you will be able to track your own work, undo mistakes
safely, use branches, resolve merge conflicts, and collaborate with others
through a shared remote.

## Who this is for

Complete beginners. We assume you can use a terminal enough to change
directories and run a command, and nothing else. Every git concept is built up
from scratch.

## What you need before you start

1. **Git installed.** Check with `git --version`. If that errors, see
   [Module 01](modules/01-setup.md).
2. **A terminal.** macOS Terminal, Linux shell, or Git Bash on Windows.
3. **A text editor** you are comfortable with (VS Code is fine).
4. No GitHub or GitLab account is required — the remote exercises use a local
   "server" folder so nothing leaves your machine.

## The modules (read in order)

| # | Module | What you learn |
| --- | --- | --- |
| 00 | [Why version control](modules/00-why-version-control.md) | The problem git solves; the mental model (snapshots, the three areas) |
| 01 | [Setup & configuration](modules/01-setup.md) | Installing git, setting your identity, first-time config |
| 02 | [Your first repository](modules/02-first-repository.md) | `init`, `status`, `add`, `commit`, the staging area, `.gitignore` |
| 03 | [Looking at history](modules/03-history.md) | `log`, `show`, `diff`, what `HEAD` means |
| 04 | [Undoing things](modules/04-undoing-things.md) | `restore`, `reset`, `commit --amend`, `revert` — and which to use when |
| 05 | [Branching & merging](modules/05-branching-merging.md) | `branch`, `switch`, `merge`, fast-forward vs merge commits |
| 06 | [Merge conflicts](modules/06-merge-conflicts.md) | Why they happen, how to read the markers, how to finish a resolution |
| 07 | [Working with remotes](modules/07-remotes.md) | `clone`, `remote`, `fetch`, `pull`, `push`, tracking branches |
| 08 | [A collaboration workflow](modules/08-collaboration-workflow.md) | Feature branches, pull/merge requests, keeping your branch current |
| 09 | [Everyday good habits](modules/09-good-habits.md) | Commit messages, small commits, what not to commit, staying out of trouble |

## The exercises

Do each exercise after the module with the same number range. Solutions are in
each exercise's `SOLUTION.md`.

| Exercise | Do it after | Skill |
| --- | --- | --- |
| [01 — First repository](exercises/01-first-repository/) | Module 02 | init → stage → commit → inspect |
| [02 — Branching](exercises/02-branching/) | Module 05 | branch, switch, merge |
| [03 — Merge conflict](exercises/03-merge-conflict/) | Module 06 | create and resolve a real conflict |
| [04 — Remotes](exercises/04-remotes/) | Module 07 | clone, commit, push, pull against a local remote |
| [05 — Undo lab](exercises/05-undo-lab/) | Module 04 (revisit after 07) | practise every recovery move |

## Also in this folder

- [`cheat-sheet.md`](cheat-sheet.md) — one page: the commands, and a "how do I undo X?" table
- [`instructor-guide.md`](instructor-guide.md) — for whoever is running the session
- [`videos/links.md`](videos/links.md) — short videos to watch alongside the modules

## The one thing to remember

Git almost never truly deletes committed work. If you feel lost, **stop typing
commands** and ask for help — the recovery is usually easy as long as you
haven't piled on more changes. [Module 04](modules/04-undoing-things.md) and the
cheat sheet cover getting back to safety.
