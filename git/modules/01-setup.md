# Module 01 — Setup & configuration

Goal: have a working `git`, and tell it who you are, so your commits are
labelled correctly.

## 1. Check whether git is already installed

```bash
git --version
```

If you see something like `git version 2.39.0`, skip to step 3. Any version
2.20+ is fine for this course.

## 2. Install git

| Platform | How |
| --- | --- |
| **macOS** | Run `git --version` — macOS offers to install the Xcode Command Line Tools, which include git. Or `brew install git` if you use Homebrew. |
| **Windows** | Download [Git for Windows](https://git-scm.com/download/win). This also gives you **Git Bash**, the terminal you'll use for this course. |
| **Linux (Debian/Ubuntu)** | `sudo apt install git` |
| **Linux (Fedora)** | `sudo dnf install git` |

Re-run `git --version` afterwards to confirm.

## 3. Tell git who you are

Every commit is stamped with a name and email. Set them once, globally, for your
user account:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Use the email you'd want associated with your work. (For this course any email
is fine; it never leaves your machine.)

## 4. Set a few sensible defaults

```bash
# Name the first branch "main" in every new repo (modern default)
git config --global init.defaultBranch main

# Make "git pull" refuse to do anything surprising (explained in Module 07)
git config --global pull.rebase false

# Use your preferred editor for commit messages.
# VS Code:
git config --global core.editor "code --wait"
# or nano (simple, terminal-based):
git config --global core.editor "nano"
```

If you skip the editor setting on many systems you'll land in **vim**, which is
hard to exit if you've never used it (`Esc`, then type `:q!`, then `Enter`).
Setting an editor you know avoids that.

## 5. Turn on colour and helpful hints

Most modern git installs do this already, but to be sure:

```bash
git config --global color.ui auto
```

## 6. Check what you set

```bash
git config --global --list
```

You should see your `user.name`, `user.email`, and the other settings. You can
also open the file directly — it's plain text at `~/.gitconfig`.

## Where config lives (three levels)

| Level | Flag | File | Applies to |
| --- | --- | --- | --- |
| System | `--system` | `/etc/gitconfig` | Every user on the machine |
| Global | `--global` | `~/.gitconfig` | You, in every repo |
| Local | `--local` (default) | `.git/config` inside a repo | Just that one repo |

More specific wins. You'll sometimes set a per-repo email with
`git config user.email "work@company.com"` (no `--global`) inside a work project.

## Optional: a nicer `git log`

Add a shortcut ("alias") for a compact, graphical history view — you'll use it a
lot from Module 03 on:

```bash
git config --global alias.lg "log --oneline --graph --decorate --all"
```

Now `git lg` works in any repo.

## Check yourself

1. Which command sets the name attached to your commits, for all your repos?
2. Where is the global config file stored?
3. You're in a work repo and need commits to use your work email without
   changing your personal default. What do you run?

<details>
<summary>Answers</summary>

1. `git config --global user.name "Your Name"`
2. `~/.gitconfig` (your home directory).
3. `git config user.email "work@company.com"` from inside that repo (no
   `--global`), which writes to that repo's `.git/config`.

</details>

Next: [Module 02 — Your first repository](02-first-repository.md)
