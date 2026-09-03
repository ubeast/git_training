# Module 09 — Everyday good habits

The commands are learned. This module is the judgement that turns "I can use
git" into "git works for me."

## Commit messages

A commit message explains **why** the change was made — the diff already shows
*what*. Future-you, reading `git log` or `git blame` in six months, has no other
source for the reasoning.

### Format

```
Short summary in the imperative, under ~50 chars

Optional body, wrapped at ~72 characters, explaining the motivation:
what problem this solves, what alternatives you rejected, anything
non-obvious. Reference issues like "Closes #142".
```

- **Imperative mood**: "Add search box", not "Added" or "Adds". (It reads as
  "this commit will *add search box*.")
- **Summary line stands alone** — it's what shows in `git log --oneline`.
- Blank line between summary and body (git treats the first line specially).

### Good vs bad

| Bad | Better |
| --- | --- |
| `fix` | `Fix crash when search query is empty` |
| `updates` | `Bump timeout to 30s for slow CI runners` |
| `WIP` | (don't commit WIP to shared branches; if local, squash before the MR) |
| `asdfasdf` | *(no.)* |
| `Fixed the thing we talked about` | `Reject uploads over 10 MB (was silently truncating)` |

## Small, focused commits

Each commit should be **one logical change** that could stand on its own.

- Fixing a bug *and* reformatting a file? Two commits.
- Renaming a function across 12 files? That's one logical change — one commit.
- Rule of thumb: if the summary line needs an "and", consider splitting.

Why it matters: small commits are easier to review, easier to revert precisely
(Module 04), and make `git bisect` (finding which commit broke something)
actually useful.

Use `git add -p` to split messy working changes into clean staged commits.

## What not to commit

| Don't commit | Why | Instead |
| --- | --- | --- |
| Secrets: passwords, API keys, tokens, `.env` | Permanent in history; a repo leak = a credential leak | `.gitignore` them; use a secrets manager or untracked local `.env` |
| Build output: `dist/`, `build/`, `*.pyc`, `node_modules/` | Regenerable; huge; causes constant conflicts | `.gitignore` |
| Large binaries: videos, datasets, installers | Bloats every clone forever, even after deletion | Git LFS, or store elsewhere and link (this repo's `videos/` does the latter) |
| Editor/OS files: `.DS_Store`, `.idea/`, `*.swp` | Noise; personal to your machine | Global gitignore: `git config --global core.excludesfile ~/.gitignore_global` |
| Generated/vendored code you can rebuild | Same as build output | `.gitignore` or a package manager |

> If you commit a secret and push it: **rotate the secret immediately.** Removing
> it in a later commit does *not* remove it from history — anyone with the repo
> can check out the old commit.

## `.gitignore` tips

- One per repo at the root; you can also have per-folder ones.
- `github.com/github/gitignore` has ready-made templates per language.
- Patterns: `*.log` (all `.log` files), `build/` (a directory anywhere),
  `/secret.txt` (only at repo root), `!keep.log` (exception — don't ignore
  this one).
- Check what's ignored and why: `git check-ignore -v somefile`.

## Pull before you push

Already in Module 07, worth repeating as a habit: `git pull` at the start of a
work session and again right before pushing. It keeps your merges tiny and
surfaces conflicts while the context is fresh.

## Branch hygiene

- One branch per unit of work; delete it after merge.
- Don't let branches live for weeks — rebase/merge `main` in or split the work.
- `git branch --merged` lists branches safe to delete;
  `git fetch --prune` clears stale remote pointers.

## Check `git status` and `git diff` before every commit

Ten seconds that prevents:

- committing a debug `print` / `console.log`,
- committing half a change because you forgot a `git add`,
- sweeping in an unrelated file with `git add .`,
- leaving conflict markers in a file.

`git diff --staged` right before `git commit` is the single highest-value habit
in this course.

## Don't panic, don't pile on

When something looks wrong: **stop**. Run `git status` and `git log --oneline`.
Don't run more mutating commands hoping to fix it — that's how a small mess
becomes a big one. Almost everything committed is recoverable via `git reflog`
(Module 04). Ask someone if unsure.

## A minimal daily routine

```bash
git switch main && git pull          # start fresh
git switch -c fix-thing              # branch

# ... work ...
git status                           # what changed?
git add -p                           # stage deliberately
git diff --staged                    # last look
git commit -m "Fix thing clearly"    # good message
git push -u origin fix-thing         # back up / share

# open MR, get review, merge, then:
git switch main && git pull
git branch -d fix-thing
```

## Check yourself

1. Why does a commit message emphasise *why* over *what*?
2. You fixed a bug and also auto-formatted the whole file in one commit. What's
   the downside?
3. You pushed a commit containing an API key. Removing it in the next commit —
   is that enough?
4. What's the single check to run right before `git commit`?

<details>
<summary>Answers</summary>

1. The diff already shows *what* changed. The reasoning — the problem, the
   constraints, the rejected alternatives — exists nowhere else, and that's what
   future readers (including you) actually need.
2. The real fix is buried in a huge diff, so review is harder and a later
   `git revert` of the bug fix also reverts the formatting (or vice versa). Two
   commits keep each change independently reviewable and revertible.
3. No. The key is still in the earlier commit; anyone with the repo can check it
   out. You must rotate (invalidate) the key. Scrubbing history is possible but
   secondary — assume it's already compromised.
4. `git diff --staged` (with a glance at `git status`).

</details>

---

That's the course. Keep [`../cheat-sheet.md`](../cheat-sheet.md) handy, and
revisit [Module 04](04-undoing-things.md) whenever git surprises you.

Next courses (separate folders): **GitLab**, then **Git in Databricks**.
