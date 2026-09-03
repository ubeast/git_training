# Module 01 — Getting connected

Goal: your laptop can push to and pull from GitLab without retyping a password
every time.

There are two ways to authenticate git with GitLab: **SSH keys** and **HTTPS +
personal access token**. Set up one. SSH is the smoother long-term choice; this
module covers both.

## Option A — SSH keys (recommended)

An SSH key is a pair of files: a **private key** (stays on your laptop, secret)
and a **public key** (you give to GitLab). GitLab recognises your laptop by the
pair. No passwords after setup.

### 1. Check for an existing key

```bash
ls -al ~/.ssh
```

Look for `id_ed25519` and `id_ed25519.pub` (or `id_rsa` / `id_rsa.pub`). If they
exist, skip to step 3.

### 2. Generate a key

```bash
ssh-keygen -t ed25519 -C "you@example.com"
```

- Press Enter to accept the default location (`~/.ssh/id_ed25519`).
- Set a passphrase (recommended) or press Enter for none.

`ed25519` is the modern algorithm. Use `-t rsa -b 4096` only if a system is too
old to support it.

### 3. Add the key to the ssh-agent

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

(On macOS, `ssh-add --apple-use-keychain ~/.ssh/id_ed25519` remembers the
passphrase across reboots.)

### 4. Give the public key to GitLab

```bash
# macOS:
pbcopy < ~/.ssh/id_ed25519.pub
# Linux:
cat ~/.ssh/id_ed25519.pub      # then copy the output
```

In GitLab: click your avatar (top right) → **Edit profile** → **SSH Keys** (left
sidebar) → paste into the **Key** box → give it a **Title** (e.g. "work laptop")
→ optionally set an expiry → **Add key**.

### 5. Test it

```bash
ssh -T git@gitlab.com
```

```
Welcome to GitLab, @your-username!
```

(Say `yes` if asked to trust the host on first connect.)

### 6. Use SSH URLs

When you clone, pick the **SSH** URL from the project's **Code** button:

```
git@gitlab.com:your-group/your-project.git
```

not the `https://` one.

## Option B — HTTPS + personal access token (PAT)

If SSH is blocked on your network, or you prefer HTTPS:

### 1. Create a token

GitLab → avatar → **Edit profile** → **Access Tokens** → **Add new token**:

- **Name**: `laptop git`
- **Expiration**: pick a date (tokens should expire; you'll renew)
- **Scopes**: check **`write_repository`** (enough for clone/push/pull). Add
  **`api`** only if you'll use `glab` or scripts against the API.
- **Create** — then **copy the token now**. GitLab shows it once.

### 2. Use it

Clone with the HTTPS URL. When git prompts:

```
Username for 'https://gitlab.com': your-username
Password for 'https://...':        <paste the token, NOT your GitLab password>
```

### 3. Stop retyping it — a credential helper

```bash
# macOS (uses the Keychain):
git config --global credential.helper osxkeychain

# Windows (Git for Windows ships this):
git config --global credential.helper manager

# Linux (cache in memory for 1 hour):
git config --global credential.helper 'cache --timeout=3600'
# ...or store on disk (plain text — only on a machine you trust):
git config --global credential.helper store
```

Next push, enter the token once; the helper remembers it.

> Your GitLab account password never works for git operations — it's always a
> token. This is deliberate.

## The `glab` CLI (optional, recommended)

`glab` lets you create MRs, view pipelines, and check issues from the terminal.

```bash
# macOS:
brew install glab
# others: https://gitlab.com/gitlab-org/cli/-/releases

glab auth login
```

Follow the prompts (choose gitlab.com, authenticate in the browser or paste a
token with `api` + `write_repository` scope). Test:

```bash
glab auth status
```

You'll use `glab mr create`, `glab ci view`, `glab issue list` later.

## Two-factor authentication

Turn on 2FA for your account: avatar → **Edit profile** → **Account** →
**Enable two-factor authentication**. With 2FA on, HTTPS git operations *must*
use a PAT (never your password + code), and the API requires a token — SSH is
unaffected. Save the recovery codes somewhere safe.

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `git@gitlab.com: Permission denied (publickey)` | Key not added to agent (`ssh-add -l` to check) or not added to GitLab. Re-do steps 3–4. |
| SSH test works but push asks for a password | You cloned the HTTPS URL. Change it: `git remote set-url origin git@gitlab.com:group/project.git` |
| `remote: HTTP Basic: Access denied` | You typed your password instead of a token, or the token lacks `write_repository`, or it expired. |
| `Support for password authentication was removed` | Same — create and use a PAT. |
| Token works but `glab` fails | `glab` needs the `api` scope; `write_repository` alone isn't enough for it. |

## Check yourself

1. Which file do you give to GitLab — the private or the public key?
2. You cloned a repo and every push asks for a password. What probably went
   wrong, and how do you check?
3. Can you use your GitLab account password to `git push`?
4. What scope does a personal access token need just to clone and push?

<details>
<summary>Answers</summary>

1. The **public** key (`id_ed25519.pub`). The private key never leaves your
   machine.
2. You used the HTTPS URL instead of SSH. Check with `git remote -v`; fix with
   `git remote set-url origin git@gitlab.com:...`. (Or set up a credential
   helper + PAT if you want HTTPS.)
3. No — git operations always use a personal access token (or SSH). The account
   password is only for the web login.
4. `write_repository`. (`api` is only needed for `glab` and API scripts.)

</details>

Next: [Module 02 — Projects, groups & roles](02-projects-groups-roles.md)
