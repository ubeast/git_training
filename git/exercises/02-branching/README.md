# Exercise 02 — Branching

**After:** Module 05 · **Time:** ~25 min

## Goal

Create branches, switch between them, and merge — producing **one fast-forward
merge** and **one real merge commit** so you see both.

## Setup

```bash
cd ~
mkdir branch-practice && cd branch-practice
git init
printf "# Website\n\n## Pages\n- Home\n" > site.md
git add site.md
git commit -m "Add site outline with Home page"
```

Confirm: `git log --oneline` shows one commit, on `main`.

## Part A — a fast-forward merge

### 1. Branch and commit

- Create a branch called `about-page` and switch to it (one command).
- Confirm you're on it: `git branch` (the `*` should be on `about-page`).
- Add a line `- About` under `## Pages` in `site.md`.
- Also create `about.md` with a sentence about the imaginary company.
- Stage and commit both: `Add About page`.
- Add one more commit: create `team.md`, commit as `Add team list`.

### 2. Look at the shape

```bash
git log --oneline --graph --decorate --all
```

`main` should be one commit back; `about-page` two commits ahead of it, in a
straight line.

### 3. Merge back

- Switch to `main`.
- Note that `about.md` and `team.md` are **not** in the folder right now
  (`ls`).
- Merge `about-page` into `main`.
- Read the output — it should say **`Fast-forward`**. Why? (Write down your
  answer.)
- `ls` again — the files are back.
- Delete the `about-page` branch.

## Part B — a real merge commit

### 4. Two branches that diverge

- From `main`, create and switch to `contact-page`.
- Add `contact.md` (`Reach us at hello@example.com`), and add `- Contact` under
  `## Pages` in `site.md`. Commit as `Add Contact page`.

- Switch back to `main`.
- **On `main` directly**, add a line `_Last updated 2026._` to the bottom of
  `site.md`. Commit as `Add footer note`.

Now `main` and `contact-page` have each moved forward from a common point — they
have diverged.

```bash
git log --oneline --graph --decorate --all
```

You should see the history fork.

### 5. Merge

- On `main`, merge `contact-page`.
- Git opens an editor for a **merge commit message** (because this can't
  fast-forward). The default message is fine — save and close.
  - VS Code: close the tab. nano: `Ctrl-O`, `Enter`, `Ctrl-X`.
- If you get a **conflict** in `site.md`: that's possible depending on where the
  lines landed. Resolve it (Module 06): keep both the `- Contact` line and the
  footer note, remove the markers, `git add site.md`, `git commit`.

### 6. Inspect the merge commit

```bash
git log --oneline --graph --decorate
git show HEAD            # note: this commit has TWO parents
git log --oneline -1 --pretty="%h parents: %p"
```

- Delete the `contact-page` branch.

## Verify checklist

- [ ] `git log --oneline --graph` shows a linear stretch (Part A) then a
      fork-and-join (Part B)
- [ ] The Part A merge said `Fast-forward`; you can explain why
- [ ] The Part B merge created a commit with two parent hashes
      (`git show HEAD` / the `%p` line shows two)
- [ ] `about-page` and `contact-page` branches are deleted (`git branch` shows
      only `main`)
- [ ] `site.md` contains Home, About, Contact, and the footer note; `about.md`,
      `team.md`, `contact.md` all present

## Stretch (optional)

- Redo Part A but force a merge commit: `git merge --no-ff about-page`. Compare
  the history shape.
- Use `git switch -` to hop between the last two branches you were on.

Compare with [`SOLUTION.md`](SOLUTION.md).
