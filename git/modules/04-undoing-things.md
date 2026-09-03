# Module 04 — Undoing things

The most reassuring module. Git is a safety net; you just need to know which
rope to grab. [Exercise 05](../exercises/05-undo-lab/) drills all of these.

## First: which situation are you in?

| Situation | Go to |
| --- | --- |
| Edited a file, haven't staged it, want the last committed version back | [A](#a-discard-changes-in-the-working-directory) |
| Staged something with `git add`, want to unstage it (keep the edit) | [B](#b-unstage-a-file) |
| Last commit has a typo in the message, or you forgot a file | [C](#c-fix-the-last-commit-amend) |
| Made a commit (or several) you want to remove from the branch | [D](#d-move-the-branch-back-reset) |
| A commit is already shared with others and you need to undo its effect | [E](#e-undo-a-commit-safely-revert) |
| "I've made a horrible mess and just want to get back to safety" | [F](#f-panic-button) |

---

## A. Discard changes in the working directory

You edited `pancakes.md` and want to throw those edits away:

```bash
git restore pancakes.md        # one file
git restore .                  # everything in the current folder
```

The file goes back to the staged version (or the last commit if nothing's
staged).

> **This one genuinely loses work** — the discarded edits were never committed,
> so git can't get them back. Everything else in this module is recoverable.

## B. Unstage a file

You ran `git add` too eagerly. Take it out of the staging area but **keep your
edits**:

```bash
git restore --staged pancakes.md
```

The file is still modified in your working directory; it's just no longer queued
for the commit. (Older tutorials say `git reset HEAD pancakes.md` — same effect.)

## C. Fix the last commit (`--amend`)

**Wrong message:**

```bash
git commit --amend -m "Add pancake cooking method"
```

**Forgot to include a file:**

```bash
git add forgotten.md
git commit --amend --no-edit      # keep the existing message
```

`--amend` *replaces* the last commit with a new one. Only do this if you
**haven't pushed it** yet (Module 07). Rewriting a commit other people already
have causes headaches.

## D. Move the branch back (`reset`)

`git reset` moves your current branch pointer to an earlier commit. Three
flavours, differing only in what happens to the changes from the commits you're
dropping:

```bash
git reset --soft  HEAD~1     # undo commit, KEEP changes staged
git reset          HEAD~1     # undo commit, keep changes but UNSTAGED  (default: --mixed)
git reset --hard  HEAD~1     # undo commit AND throw the changes away
```

Picture undoing the last commit:

| Flag | Commit gone? | Your changes end up... |
| --- | --- | --- |
| `--soft` | yes | staged, ready to re-commit |
| `--mixed` (default) | yes | in your working directory, unstaged |
| `--hard` | yes | **deleted** |

Typical use: "these last 3 commits should really be one" →
`git reset --soft HEAD~3` then one fresh `git commit`.

> `--hard` is the only reset that loses working changes. The *commits* it
> "removes" still exist for ~30–90 days and are findable via `git reflog` (see
> Panic button) — but uncommitted edits in your working dir are gone.

**Never `reset` a branch you've already pushed and shared** — use `revert`
instead.

## E. Undo a commit safely (`revert`)

`git revert` doesn't remove history. It creates a **new commit** that is the
exact opposite of a previous one, cancelling out its changes:

```bash
git revert HEAD              # undo the latest commit with a new commit
git revert a1b2c3d           # undo a specific older commit
```

Because it only *adds* a commit, it's safe on shared branches — everyone else
just pulls the new "undo" commit normally. This is the right tool when the bad
commit is already on the team's `main`.

## F. Panic button

### "Get my working directory back to exactly the last commit"

```bash
git status                       # look first — know what you're discarding
git restore --staged .           # unstage everything
git restore .                    # discard all working-dir changes
git clean -nd                    # PREVIEW untracked files/dirs that would be removed
git clean -fd                    # actually remove them (irreversible)
```

### "I ran a bad command and lost commits" — `git reflog`

`git reflog` is a private log of everywhere `HEAD` has been — including states
that `reset` or `--amend` "removed." It's your undo history for git operations
themselves.

```bash
git reflog
```

```
7f3a9c1 HEAD@{0}: reset: moving to HEAD~2
9d4e2f8 HEAD@{1}: commit: Add topping ideas
c1a5b3e HEAD@{2}: commit: Add pancake method
```

Spot the state you want (say `HEAD@{1}`) and get back to it:

```bash
git reset --hard HEAD@{1}
```

As long as you haven't run `git gc` or waited weeks, **committed work is almost
always recoverable this way.** This is why Module 00 says: if you're lost, stop
and ask before doing more.

## The rule of thumb

| Bad thing is... | Use |
| --- | --- |
| ...only in your working directory | `git restore` |
| ...only staged | `git restore --staged` |
| ...the most recent commit, not pushed | `git commit --amend` or `git reset` |
| ...one or more commits, not pushed | `git reset` |
| ...already pushed / shared | `git revert` |
| ...a command you regret | `git reflog` + `git reset --hard HEAD@{n}` |

## Check yourself

1. You `git add`ed a file but haven't committed. How do you unstage it without
   losing the edit?
2. Your last commit (not pushed) should have included one more file. Fix it in
   two commands.
3. A teammate reports that a commit already on `main` broke the build. Which
   command do you use, and why not `reset`?
4. You ran `git reset --hard HEAD~3` and realise you needed one of those
   commits. Are you stuck?

<details>
<summary>Answers</summary>

1. `git restore --staged <file>`.
2. `git add <file>` then `git commit --amend --no-edit`.
3. `git revert <hash>`. `reset` would rewrite shared history — everyone else
   still has the old commits and their next push/pull turns into a mess.
   `revert` adds a normal new commit that undoes the change.
4. No. `git reflog`, find the `HEAD@{n}` entry from before the reset, then
   `git reset --hard HEAD@{n}`. (Any changes that were only in your working
   directory, never committed, are gone — but the commits are fine.)

</details>

Next: [Module 05 — Branching & merging](05-branching-merging.md)
