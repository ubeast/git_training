# Training Materials

Hands-on training courses. Each course is self-contained in its own folder.

| Course | Folder | Status |
| --- | --- | --- |
| **Git** — version control fundamentals for complete beginners | [`git/`](git/) | Ready |
| **GitLab** — using GitLab on top of git (projects, merge requests, CI/CD) | [`gitlab/`](gitlab/) | Ready |
| **Git in Databricks** — version control for notebooks, Git folders, jobs from Git, Asset Bundles | [`databricks/`](databricks/) | Ready |

Start with **Git** — the GitLab and Databricks courses assume you already know
the git fundamentals taught there. The Databricks course also refers to the
GitLab course for CI/CD concepts, but doesn't require it.

## How each course is organized

- `modules/` — numbered lesson modules to read through, in order
- `exercises/` — hands-on labs with a starting point, tasks, and solutions
- `instructor-guide.md` — facilitation guide: timing, demo scripts, talking points
- `cheat-sheet.md` — one-page command reference
- `videos/` — short videos used during the session (media not committed; see `videos/links.md`)

## For participants

Clone this repo and work through the course folder for your session:

```bash
git clone <repo-url>
cd git_training/git      # or gitlab/ , databricks/
```

Open `git/README.md` and follow it from the top.
