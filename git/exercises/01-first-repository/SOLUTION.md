# Exercise 01 — Solution

Exact commands. Yours may differ slightly (file contents, message wording) —
that's fine.

## Setup

```bash
cd ~
mkdir travel-journal && cd travel-journal
```

## 1. Make it a repository

```bash
git init
git status
```

## 2. First commit

```bash
echo "# Travel Journal" > README.md
git status                       # README.md is untracked
git add README.md
git status                       # "Changes to be committed: new file: README.md"
git commit -m "Add README"
git status                       # clean
git log --oneline                # 1 commit
```

## 3. Add two entries as one commit

```bash
printf "# Day 1\nArrived in Lisbon. Ate too many pastéis de nata.\n" > day-1.md
printf "# Day 2\nTook the tram to Belém.\n" > day-2.md
git add day-1.md day-2.md
git commit -m "Add days 1 and 2"
git log --oneline                # 2 commits
```

## 4. The staging-area checkpoint

```bash
echo "Walked the Alfama at sunset." >> day-1.md
git add day-1.md
echo "Found a tiny fado bar." >> day-1.md
git status
```

`git status` output:

```
Changes to be committed:
        modified:   day-1.md
Changes not staged for commit:
        modified:   day-1.md
```

**Why both sections?** `git add` took a snapshot of `day-1.md` *as it was at
that moment* into the staging area. That snapshot (one new line) is "to be
committed." Then you edited the file again — the working-directory copy now has
a second new line that the staged snapshot doesn't know about, so it also shows
as "not staged." The staging area froze a version; later edits are separate
until you `git add` again.

```bash
git diff                         # shows only "Found a tiny fado bar." (working vs staged)
git diff --staged                # shows only "Walked the Alfama..." (staged vs last commit)
git add day-1.md                 # stage the second line too
git commit -m "Expand day 1"
```

## 5. Ignore some noise

```bash
echo "scratch" > notes.tmp
mkdir .cache && echo x > .cache/x
git status                       # notes.tmp and .cache/ untracked

cat > .gitignore <<'EOF'
*.tmp
.cache/
EOF

git status                       # only .gitignore untracked now
git check-ignore -v .cache/x     # .gitignore:2:.cache/   .cache/x
git add .gitignore
git commit -m "Add .gitignore"
```

## 6. Rename

```bash
git mv day-2.md day-two.md
rm notes.tmp                      # ignored file, plain rm, git doesn't care
git status                       # renamed: day-2.md -> day-two.md
git commit -m "Rename day-2"
```

## Verify

```bash
git log --oneline
```

```
f5c1a20 Rename day-2
9e3b7d4 Add .gitignore
2a8f6c1 Expand day 1
7d4e9b0 Add days 1 and 2
1b2c3d4 Add README
```

```bash
git show HEAD --stat
```

```
 day-2.md => day-two.md | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
```

(0 changes because only the name changed, not the contents — git detected the
rename.)

## Key takeaways

- `git status` is the map. Run it after every step.
- `git add` snapshots a file *now*; later edits need another `git add`.
- `git diff` = working vs staged; `git diff --staged` = staged vs last commit.
- `.gitignore` stops *untracked* files from being seen; it doesn't untrack
  anything already committed.
- `git mv` / `git rm` stage the rename/deletion for you; git also auto-detects
  plain `mv`.
