# Module 08 — A collaboration workflow

The commands from Modules 02–07 are the vocabulary. This module is the
**sentence** — the routine teams actually follow so many people can work on one
codebase without stepping on each other.

## The feature branch workflow

The most common approach, and what GitLab and GitHub are built around:

1. **`main` is always deployable.** Nobody commits directly to it.
2. Every piece of work happens on its own short-lived **branch** off `main`.
3. When it's ready, you open a **merge request** (GitLab) / **pull request**
   (GitHub) — a request to merge your branch into `main`.
4. Teammates **review** it, CI runs the tests, and when it's approved it's
   merged.
5. The branch is deleted. Repeat.

```
main   ──●──────●───────────●────────●──►   (only ever moves via merged MRs)
          \            /      \      /
feature-A  ●──●──●────/        \    /
feature-B                  ●──●─────/
```

## The loop, step by step

### 1. Start from an up-to-date `main`

```bash
git switch main
git pull
```

### 2. Branch

```bash
git switch -c add-search
```

Name it for the work: `add-search`, `fix-login-timeout`, `update-docs`. Some
teams prefix with a ticket number: `PROJ-142-add-search`.

### 3. Work in small commits

```bash
# edit...
git add -p
git commit -m "Add search box to header"
# edit...
git commit -am "Wire search box to results query"
```

Push early so your work is backed up and visible:

```bash
git push -u origin add-search
```

Keep pushing as you go (`git push`).

### 4. Keep your branch current

If `main` moves a lot while you work, pull its changes into your branch
periodically so the eventual merge is small:

```bash
git switch main
git pull
git switch add-search
git merge main            # resolve any conflicts now, on your branch
git push
```

Doing this **on your branch** means conflicts are your problem to solve in
private, not something that blocks the merge later.

### 5. Open the merge request

Push, then open the link git prints (or go to the project in GitLab and click
**Create merge request**). A good MR has:

- a title saying what it does,
- a description: *why*, how to test it, anything reviewers should know,
- a link to the ticket/issue,
- a small, reviewable diff (big MRs sit unreviewed).

### 6. Respond to review

Reviewers leave comments. You address them with **more commits on the same
branch** and push again — the MR updates automatically.

```bash
# make requested changes
git commit -am "Debounce search input per review"
git push
```

### 7. Merge and clean up

Once approved and CI is green, click **Merge** in GitLab. Then locally:

```bash
git switch main
git pull                       # get your now-merged work
git branch -d add-search       # delete local branch
git fetch --prune              # drop the stale origin/add-search pointer
```

## Who resolves conflicts, and where

- Conflicts between your branch and `main` are **yours** to resolve, on your
  branch, before the merge (step 4). The MR page will warn you when your branch
  conflicts with `main`.
- Resolve them locally with the Module 06 process, push, and the MR clears.

## Rebase vs merge for "keeping current" (awareness only)

Some teams, instead of `git merge main` in step 4, use `git rebase main`, which
replays your branch's commits on top of the latest `main` for a linear history.

- **Merge**: safe, preserves exactly what happened, adds merge commits.
- **Rebase**: cleaner line of history, but *rewrites your branch's commits* —
  never rebase commits someone else has already pulled.

As a beginner: **use merge.** Learn rebase later, when a team asks for it and
you understand exactly which commits are being rewritten.

## Commit-to-`main`-directly — when it's OK

Solo projects, throwaway repos, and personal notes: committing straight to
`main` and pushing is completely fine. The whole branch/MR/review dance is about
*coordinating multiple people* and *protecting a shared deployable branch*. Use
the ceremony that fits the situation.

## Check yourself

1. Why keep feature branches short-lived?
2. `main` has moved 20 commits ahead since you branched three days ago. What
   should you do on your branch, and why there specifically?
3. A reviewer asks for a change. Do you create a new branch?
4. When is it fine to commit directly to `main`?

<details>
<summary>Answers</summary>

1. Less time for `main` to drift means smaller, easier merges and fewer
   conflicts; smaller diffs get reviewed faster; less risk of the work becoming
   stale or duplicated.
2. `git switch main && git pull`, then `git switch <branch> && git merge main`,
   resolve conflicts, push. Doing it on your branch keeps the conflict
   resolution private and off the critical path — `main` and other people's
   work are never blocked by it.
3. No — commit the change on the *same* branch and push; the merge request
   updates in place.
4. Solo work, personal/throwaway repos, or any repo where you're not
   coordinating with other people on a protected shared branch.

</details>

Next: [Module 09 — Everyday good habits](09-good-habits.md)
