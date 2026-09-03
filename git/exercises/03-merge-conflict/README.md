# Exercise 03 — Merge conflict

**After:** Module 06 · **Time:** ~20 min

## Goal

Deliberately cause a merge conflict, read the markers, resolve it three
different ways in three attempts, and practise `git merge --abort`.

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

## Tasks

### 1. Two branches change the same line

```bash
git switch -c raise-timeout
# change the timeout line to: timeout = 30
# (edit config.md however you like)
git commit -am "Raise timeout to 30"

git switch main
git switch -c lower-timeout
# change the SAME line to: timeout = 5
git commit -am "Lower timeout to 5 for fast failure"
```

### 2. Cause the conflict

```bash
git switch main
git merge raise-timeout       # this one fast-forwards or merges cleanly
git merge lower-timeout       # CONFLICT here
```

- Read the conflict output. Run `git status` — note what it tells you to do.

### 3. Read the markers

Open `config.md`. Identify:

- Which value is between `<<<<<<< HEAD` and `=======`? Which branch is that?
- Which value is between `=======` and `>>>>>>> lower-timeout`?
- Which lines merged fine (no markers around them)?

Write the answers down.

### 4. Resolve — attempt 1: keep "ours"

- Edit `config.md` so `timeout = 30` (the `HEAD` side), delete all three marker
  lines.
- Verify no markers remain anywhere: `grep -rn '<<<<<<<\|=======\|>>>>>>>' .`
- `git add config.md`
- `git commit` (accept the default message)
- `git log --oneline --graph` — see the merge commit.

### 5. Redo it — attempt 2: keep "theirs"

Undo the merge commit and try again, this time keeping `timeout = 5`:

```bash
git reset --hard HEAD~1        # drop the merge commit you just made
git merge lower-timeout        # conflict again
```

- Resolve to `timeout = 5`, remove markers, `git add`, `git commit`.

### 6. Redo it — attempt 3: something new + practise abort

```bash
git reset --hard HEAD~1
git merge lower-timeout        # conflict again
git merge --abort             # back out completely
git status                     # clean, as if you never merged
```

Now do it for real:

```bash
git merge lower-timeout
```

- Resolve to a **compromise**: `timeout = 15`, and add a comment line above it:
  `# tuned 2026 — was contested between 5 and 30`.
- Remove markers, `git add`, `git commit`.

### 7. Confirm the final state

```bash
git show HEAD
cat config.md
git branch -d raise-timeout lower-timeout
```

## Verify checklist

- [ ] You hit a real `CONFLICT (content)` on `config.md`
- [ ] You can name which side `<<<<<<< HEAD` represents (it's `main`, which
      already had `raise-timeout` merged, so `timeout = 30`)
- [ ] `git merge --abort` returned you to a clean state
- [ ] Final `config.md` has `timeout = 15` with your comment, no conflict
      markers
- [ ] `grep -rn '<<<<<<<' .` finds nothing
- [ ] Both feature branches deleted

## Common mistakes to notice

- Committing with a marker still in the file → `grep` for markers *every time*
  before `git add`.
- Forgetting `git add` after editing → `git status` still says "both modified",
  and `git commit` refuses.
- Editing the wrong file → only files listed as "both modified" have conflicts.

Compare with [`SOLUTION.md`](SOLUTION.md).
