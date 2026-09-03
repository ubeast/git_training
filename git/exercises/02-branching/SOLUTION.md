# Exercise 02 — Solution

## Setup

```bash
cd ~
mkdir branch-practice && cd branch-practice
git init
printf "# Website\n\n## Pages\n- Home\n" > site.md
git add site.md
git commit -m "Add site outline with Home page"
```

## Part A — fast-forward merge

### 1. Branch and commit

```bash
git switch -c about-page

# add "- About" under "## Pages"
printf "# Website\n\n## Pages\n- Home\n- About\n" > site.md
echo "We build small websites for small businesses." > about.md
git add site.md about.md
git commit -m "Add About page"

echo "- Alex (design)\n- Sam (code)" > team.md
git add team.md
git commit -m "Add team list"
```

### 2. Shape

```bash
git log --oneline --graph --decorate --all
```

```
* c3d4e5f (HEAD -> about-page) Add team list
* b2c3d4e Add About page
* a1b2c3d (main) Add site outline with Home page
```

### 3. Merge back

```bash
git switch main
ls                      # site.md only
git merge about-page
```

```
Updating a1b2c3d..c3d4e5f
Fast-forward
 about.md | 1 +
 site.md  | 1 +
 team.md  | 1 +
 3 files changed, 3 insertions(+)
```

**Why fast-forward?** `main` had *no* commits of its own since `about-page`
branched off. So git doesn't need to combine anything — it just slides the
`main` label forward to `about-page`'s tip. History stays a straight line.

```bash
ls                      # about.md, site.md, team.md
git branch -d about-page
```

## Part B — real merge commit

### 4. Diverge

```bash
git switch -c contact-page
echo "Reach us at hello@example.com" > contact.md
printf "# Website\n\n## Pages\n- Home\n- About\n- Contact\n" > site.md
git add contact.md site.md
git commit -m "Add Contact page"

git switch main
printf "# Website\n\n## Pages\n- Home\n- About\n\n_Last updated 2026._\n" > site.md
git add site.md
git commit -m "Add footer note"
```

```bash
git log --oneline --graph --decorate --all
```

```
* d5e6f7a (HEAD -> main) Add footer note
| * c4d5e6f (contact-page) Add Contact page
|/
* c3d4e5f Add team list
* b2c3d4e Add About page
* a1b2c3d Add site outline with Home page
```

### 5. Merge

```bash
git merge contact-page
```

Both branches changed `site.md`, so expect a **conflict**:

```
CONFLICT (content): Merge conflict in site.md
Automatic merge failed; fix conflicts and then commit the result.
```

Open `site.md`:

```
# Website

## Pages
- Home
- About
<<<<<<< HEAD
- Contact

_Last updated 2026._
=======
- Contact
>>>>>>> contact-page
```

(Exact markers vary.) Resolve to keep both intentions:

```
# Website

## Pages
- Home
- About
- Contact

_Last updated 2026._
```

```bash
git add site.md
git commit               # accept the default merge message
```

> If your line placement happened to avoid a conflict, git just opens the editor
> for the merge message directly — save and close. Same result.

### 6. Inspect

```bash
git show HEAD --stat
git log --oneline -1 --pretty="%h parents: %p"
```

```
d7e8f9a parents: d5e6f7a c4d5e6f
```

Two parent hashes = a merge commit joining the two lines of history.

```bash
git log --oneline --graph --decorate
```

```
*   d7e8f9a (HEAD -> main) Merge branch 'contact-page'
|\
| * c4d5e6f Add Contact page
* | d5e6f7a Add footer note
|/
* c3d4e5f Add team list
...
```

```bash
git branch -d contact-page
git branch              # only: main
```

## Key takeaways

- **Fast-forward**: destination branch didn't move → git just advances the
  label, linear history, no merge commit.
- **Merge commit**: both branches moved → git creates a commit with two parents
  to join them.
- You merge *into* the branch you're currently on — always `git switch` to the
  destination first.
- Divergent edits to the same file → conflict, resolved with the Module 06
  process, which then completes the merge.
