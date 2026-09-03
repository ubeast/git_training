# Module 02 — Your first repository

You'll make a repo from nothing, and learn the everyday loop:
**edit → `status` → `add` → `commit`**, repeated forever.

Follow along by typing every command. [Exercise 01](../exercises/01-first-repository/)
walks the same path with checkpoints.

## 1. Create a project folder and turn it into a repo

```bash
mkdir recipes
cd recipes
git init
```

Output:

```
Initialized empty Git repository in /path/to/recipes/.git/
```

`git init` created a hidden `.git/` folder. **That folder *is* the repository** —
all history lives there. Delete it and the folder goes back to being an ordinary
folder. The rest of `recipes/` is your working directory.

```bash
git status
```

```
On branch main

No commits yet

nothing to commit (working tree clean)
```

## 2. Create a file

```bash
echo "# My Recipes" > README.md
git status
```

```
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        README.md

nothing added to commit but untracked files present
```

**Untracked** means git sees the file but isn't managing it yet. Git never
tracks a file until you tell it to.

## 3. Stage the file (`git add`)

```bash
git add README.md
git status
```

```
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
        new file:   README.md
```

`README.md` is now in the **staging area** — it's queued for the next commit.
Nothing is permanent yet.

## 4. Make the commit

```bash
git commit -m "Add README with project title"
```

```
[main (root-commit) a1b2c3d] Add README with project title
 1 file changed, 1 insertion(+)
 create mode 100644 README.md
```

- `-m` supplies the commit message inline. Without it, git opens your editor.
- `a1b2c3d` is the start of the commit's **hash** — its unique ID.
- `root-commit` just means "the first commit in this repo."

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

"Clean" = working directory matches the latest commit. Nothing outstanding.

## 5. The loop again, with more files

```bash
echo "## Pancakes" > pancakes.md
echo "Flour, milk, eggs." >> pancakes.md
echo "## Omelette" > omelette.md
echo "Eggs, butter, salt." >> omelette.md

git status
```

Both files are untracked. Stage and commit them — **together, because they're
one logical addition**:

```bash
git add pancakes.md omelette.md
git commit -m "Add pancakes and omelette recipes"
```

Tip: `git add .` stages *everything* new or changed in the current folder. Handy,
but look at `git status` first so you know what you're sweeping in.

## 6. Change an existing file

```bash
echo "Mix, then fry." >> pancakes.md
git status
```

```
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   pancakes.md
```

Now the file is **tracked** and **modified**. See exactly what changed:

```bash
git diff
```

```diff
diff --git a/pancakes.md b/pancakes.md
index 83db48f..bf3459b 100644
--- a/pancakes.md
+++ b/pancakes.md
@@ -1,2 +1,3 @@
 ## Pancakes
 Flour, milk, eggs.
+Mix, then fry.
```

Lines starting with `+` are added, `-` are removed. Stage and commit:

```bash
git add pancakes.md
git commit -m "Add pancake method"
```

## 7. Staged vs unstaged — an important detail

`git diff` shows **working directory vs staging area** (changes you haven't
staged). To see **staging area vs last commit** (what you're about to commit):

```bash
git diff --staged
```

Common workflow: edit, `git add -p` (stage hunks interactively), `git diff
--staged` to review, then `git commit`.

## 8. `.gitignore` — files git should leave alone

Some files should never be committed: secrets, build output, editor junk,
huge binaries, OS files like `.DS_Store`. List them in a file named
`.gitignore` at the repo root:

```bash
cat > .gitignore <<'EOF'
# OS noise
.DS_Store
Thumbs.db

# Editor
.vscode/
*.swp

# Secrets — never commit these
.env
*.key
EOF

git add .gitignore
git commit -m "Add .gitignore"
```

Now `git status` won't nag about ignored files, and `git add .` won't pick them
up.

> **`.gitignore` only affects *untracked* files.** If a file is already
> committed, adding it to `.gitignore` does nothing. You have to stop tracking
> it: `git rm --cached secret.env` then commit. (And if it was a real secret,
> rotate it — it's still in history.)

## 9. Removing and renaming tracked files

```bash
git rm omelette.md          # deletes the file AND stages the removal
git mv pancakes.md flapjacks.md   # rename, staged
git commit -m "Rename pancakes; drop omelette"
```

(`git mv` is just shorthand — a plain `mv` followed by `git add` does the same
thing; git detects renames automatically.)

## Command recap

| Command | Does |
| --- | --- |
| `git init` | Create a new repo in the current folder |
| `git status` | Show what's changed and what's staged — run it constantly |
| `git add <file>` | Stage a file (or its changes) for the next commit |
| `git add .` | Stage everything new/changed under the current folder |
| `git commit -m "msg"` | Save the staged snapshot with a message |
| `git diff` | Working directory vs staging area |
| `git diff --staged` | Staging area vs last commit |
| `git rm` / `git mv` | Delete / rename a tracked file (and stage it) |

## Check yourself

1. What's the difference between an *untracked* and a *modified* file?
2. You ran `git add notes.txt`, then edited `notes.txt` again. What's in the
   next commit — and what does `git status` show?
3. You committed `config.env` yesterday and now added it to `.gitignore`. Is it
   still tracked?
4. Which command shows what you're *about* to commit?

<details>
<summary>Answers</summary>

1. Untracked: git isn't managing it at all yet. Modified: git tracks it and has
   a committed version, but your working copy differs from what's staged.
2. Only the version you staged goes in. `git status` shows `notes.txt` under
   *both* "Changes to be committed" (the staged version) and "Changes not
   staged for commit" (the newer edits). Run `git add` again to include them.
3. Yes. `.gitignore` doesn't untrack anything. Run `git rm --cached config.env`
   and commit to stop tracking it.
4. `git diff --staged` (also written `git diff --cached`).

</details>

Next: [Module 03 — Looking at history](03-history.md)
