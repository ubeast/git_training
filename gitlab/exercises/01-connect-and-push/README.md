# Exercise 01 — Connect & push

**After:** Modules 01–03 · **Time:** ~25 min

## Goal

Get your laptop talking to GitLab over SSH, create a project, push an existing
local repo into it, and find your way around the web UI.

## Part 1 — SSH

### 1. Key

- Check for an existing key: `ls -al ~/.ssh` (look for `id_ed25519.pub`).
- If none, generate one: `ssh-keygen -t ed25519 -C "you@example.com"` (Enter for
  default path; set a passphrase).
- Add it to the agent: `eval "$(ssh-agent -s)" && ssh-add ~/.ssh/id_ed25519`.

### 2. Register it with GitLab

- Copy the **public** key: `cat ~/.ssh/id_ed25519.pub` (or `pbcopy <
  ~/.ssh/id_ed25519.pub` on macOS).
- GitLab → your avatar → **Edit profile** → **SSH Keys** → paste → Title "course
  laptop" → **Add key**.

### 3. Test

```bash
ssh -T git@gitlab.com
```

Expected: `Welcome to GitLab, @your-username!`

**Do not continue until you see that.** If you get `Permission denied
(publickey)`, re-check steps 1–2 and `ssh-add -l`.

## Part 2 — create a project and push to it

### 4. Make a local repo to push

```bash
cd ~
mkdir gitlab-lab && cd gitlab-lab
git init
printf "# GitLab Lab\n\nMy sandbox for the GitLab course.\n" > README.md
mkdir src && printf "def greet(name):\n    return f\"Hello, {name}!\"\n" > src/app.py
git add .
git commit -m "Initial project skeleton"
```

### 5. Create the GitLab project

- GitLab → **+** (top nav) → **New project/repository** → **Create blank
  project**.
- Name: `gitlab-lab` (or `<username>-gitlab-lab` if your instructor asked for a
  prefix).
- Namespace: your course group if you have one, else your personal namespace.
- Visibility: **Private**.
- **Uncheck** "Initialize repository with a README" — you're about to push one.
- **Create project.**

### 6. Connect and push

On the empty-project page, GitLab shows the commands. You want the
"**push an existing folder**" section. From `~/gitlab-lab`:

```bash
git remote add origin git@gitlab.com:<namespace>/gitlab-lab.git
git branch -M main
git push -u origin main
```

Refresh the project page — your files are there.

### 7. Confirm the remote is SSH, not HTTPS

```bash
git remote -v
```

Both lines should start with `git@gitlab.com:` — not `https://`. If they say
`https://`, fix it:

```bash
git remote set-url origin git@gitlab.com:<namespace>/gitlab-lab.git
```

## Part 3 — explore the web UI

In the project, find and note where each of these lives (left sidebar):

- [ ] The file browser and the **Blame** view for `src/app.py`
- [ ] **Code → Commits** — your one commit
- [ ] **Code → Branches** — just `main`
- [ ] The **Web IDE** (open it: press `.` in the repo, or Edit → Web IDE)
- [ ] **Settings → Repository → Protected branches** — note `main` is already
      protected (you'll use this in Exercise 04)
- [ ] **Settings → General** — find the "default branch" setting

### 8. Make one change from the browser

- Open `README.md` in the UI → **Edit** (pencil, single-file editor).
- Add a line: `Created during the GitLab course.`
- Scroll down: commit message `Note course origin in README`, and **select
  "Commit directly to the `main` branch"** (allowed for now — you're the
  owner/maintainer of this project).
- **Commit changes.**

### 9. Pull that change locally

```bash
git pull
git log --oneline
```

You should see the commit you made in the browser.

## Verify checklist

- [ ] `ssh -T git@gitlab.com` greets you by username
- [ ] `git remote -v` shows an `git@gitlab.com:` (SSH) URL
- [ ] The project on GitLab shows `README.md` and `src/app.py`
- [ ] `git log --oneline` locally shows both the initial commit and the
      browser-made commit
- [ ] You can point to where Blame, Commits, Branches, Web IDE, and Protected
      branches live in the UI

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `Permission denied (publickey)` | Key not added to agent (`ssh-add -l`) or not in GitLab. Redo Part 1. |
| `Repository not found` / `access denied` on push | Wrong namespace in the URL, or you're not a member of that group. Check the URL on the project page. |
| Push rejected, "Updates were rejected" | You left "Initialize with a README" checked — the server has a commit you don't. `git pull --rebase origin main` then push, or recreate the project without the README. |
| Push asks for a password | HTTPS remote — `git remote set-url origin git@...`. |

Compare with [`SOLUTION.md`](SOLUTION.md).
