# Exercise 03 — Solution

## Setup

```bash
cd ~
mkdir conflict-practice && cd conflict-practice
git init
cat > config.md <<'EOF'
# App Config

timeout = 10
retries = 3
log_level = info
EOF
git add config.md
git commit -m "Add initial config"
```

## 1. Two branches, same line

```bash
git switch -c raise-timeout
sed -i '' 's/timeout = 10/timeout = 30/' config.md   # macOS sed; Linux: sed -i 's/.../.../'
git commit -am "Raise timeout to 30"

git switch main
git switch -c lower-timeout
sed -i '' 's/timeout = 10/timeout = 5/' config.md
git commit -am "Lower timeout to 5 for fast failure"
```

(Editing by hand in your editor is completely fine instead of `sed`.)

## 2. Cause the conflict

```bash
git switch main
git merge raise-timeout
```

```
Updating a1b2c3d..b2c3d4e
Fast-forward
 config.md | 2 +-
```

`main` now has `timeout = 30`. Then:

```bash
git merge lower-timeout
```

```
Auto-merging config.md
CONFLICT (content): Merge conflict in config.md
Automatic merge failed; fix conflicts and then commit the result.
```

```bash
git status
```

```
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   config.md
```

## 3. Read the markers

`config.md`:

```
# App Config

<<<<<<< HEAD
timeout = 30
=======
timeout = 5
>>>>>>> lower-timeout
retries = 3
log_level = info
```

- Between `<<<<<<< HEAD` and `=======`: `timeout = 30`. This is **`main`** —
  which already had `raise-timeout` merged in.
- Between `=======` and `>>>>>>> lower-timeout`: `timeout = 5`, from the
  `lower-timeout` branch.
- `# App Config`, `retries = 3`, `log_level = info` merged fine — no markers.

## 4. Attempt 1 — keep ours (30)

```
# App Config

timeout = 30
retries = 3
log_level = info
```

```bash
grep -rn '<<<<<<<\|=======\|>>>>>>>' .    # no output = good
git add config.md
git commit                                # default: "Merge branch 'lower-timeout'"
git log --oneline --graph
```

## 5. Attempt 2 — keep theirs (5)

```bash
git reset --hard HEAD~1
git merge lower-timeout
# edit config.md -> timeout = 5, remove markers
git add config.md
git commit
```

## 6. Attempt 3 — abort, then compromise

```bash
git reset --hard HEAD~1
git merge lower-timeout
git merge --abort
git status                 # clean; no merge in progress

git merge lower-timeout    # for real now
```

Resolve `config.md` to:

```
# App Config

# tuned 2026 — was contested between 5 and 30
timeout = 15
retries = 3
log_level = info
```

```bash
grep -rn '<<<<<<<\|=======\|>>>>>>>' .
git add config.md
git commit
```

## 7. Final state

```bash
git show HEAD
cat config.md
git branch -d raise-timeout lower-timeout
git branch                 # only main
```

`git show HEAD` shows a merge commit (two parents) and the diff resolving to
`timeout = 15`.

## Key takeaways

- A conflict happens only when **the same lines** changed on both sides. The
  other config lines merged silently.
- `<<<<<<< HEAD` is always *your current branch*; below `=======` is *what
  you're merging in*.
- Resolving = editing the file to the final text **and deleting all three
  marker lines**, then `git add` + `git commit`.
- `git merge --abort` is a clean, complete undo of an in-progress merge —
  use it freely.
- `git reset --hard HEAD~1` drops a finished merge commit so you can retry (safe
  here because nothing was pushed).
