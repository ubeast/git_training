# Exercise 01 — Solution

## Part 1 — SSH

```bash
ls -al ~/.ssh
ssh-keygen -t ed25519 -C "you@example.com"      # Enter, Enter (or passphrase)
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
# macOS to persist across reboots:
#   ssh-add --apple-use-keychain ~/.ssh/id_ed25519

cat ~/.ssh/id_ed25519.pub          # copy this whole line
# → GitLab: avatar → Edit profile → SSH Keys → paste → Add key

ssh -T git@gitlab.com
# The authenticity of host 'gitlab.com' ... yes
# Welcome to GitLab, @your-username!
```

## Part 2

```bash
cd ~
mkdir gitlab-lab && cd gitlab-lab
git init
printf "# GitLab Lab\n\nMy sandbox for the GitLab course.\n" > README.md
mkdir src && printf "def greet(name):\n    return f\"Hello, {name}!\"\n" > src/app.py
git add .
git commit -m "Initial project skeleton"
```

Create the project in the UI (blank, private, **no** README).

```bash
git remote add origin git@gitlab.com:your-namespace/gitlab-lab.git
git branch -M main
git push -u origin main
```

```
Enumerating objects: 5, done.
...
To gitlab.com:your-namespace/gitlab-lab.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

```bash
git remote -v
# origin  git@gitlab.com:your-namespace/gitlab-lab.git (fetch)
# origin  git@gitlab.com:your-namespace/gitlab-lab.git (push)
```

If it showed `https://`, that's the classic mistake:

```bash
git remote set-url origin git@gitlab.com:your-namespace/gitlab-lab.git
```

## Part 3 — where things are (GitLab UI, project left sidebar)

| Thing | Path |
| --- | --- |
| File browser | **Code → Repository** (or the project overview) |
| Blame for a file | Open the file → **Blame** button (top right of the file view) |
| Commits | **Code → Commits** |
| Branches | **Code → Branches** |
| Web IDE | Press `.` in the repo, or a file's **Edit → Web IDE** |
| Protected branches | **Settings → Repository → Protected branches** (expand section) |
| Default branch | **Settings → Repository → Default branch**, also shown in **Settings → General** |

### 8–9. Browser edit + pull

Edit `README.md` in the UI, commit directly to `main` with message
"Note course origin in README".

```bash
git pull
```

```
Updating a1b2c3d..d4e5f6a
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
```

```bash
git log --oneline
# d4e5f6a Note course origin in README
# a1b2c3d Initial project skeleton
```

## Key takeaways

- The **public** key goes to GitLab; the private key never leaves your laptop.
- `ssh -T git@gitlab.com` is the one-line "is SSH working?" test.
- Clone/remote URLs: `git@gitlab.com:...` (SSH) vs `https://gitlab.com/...`
  (needs a token). `git remote -v` tells you which you have;
  `git remote set-url` switches.
- Create the GitLab project **without** a README when you're pushing an existing
  repo, or your first push is a non-fast-forward.
- A change made in the GitLab web UI is a normal commit — `git pull` brings it
  down like any other.
