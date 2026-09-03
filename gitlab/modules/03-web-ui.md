# Module 03 — The GitLab web UI

A tour of the project interface, and the browser-based tools that save you a
`git clone` for small things.

## The project's left sidebar

Everything for a project hangs off the left nav:

| Item | What's there |
| --- | --- |
| **Project overview** | README, description, activity, quick stats |
| **Manage → Activity / Members / Labels** | Event feed, who's in, label definitions |
| **Plan → Issues / Boards / Milestones / Wiki** | Planning and docs (Module 04) |
| **Code → Merge requests / Branches / Commits / Tags / Repository** | The repo and its history |
| **Build → Pipelines / Jobs / Artifacts / Schedules** | CI/CD (Modules 08–09) |
| **Deploy → Environments / Releases** | Where things are deployed, tagged releases |
| **Settings** | Everything configurable (Module 02) |

The exact labels shift between GitLab versions; the groupings are stable.

## Browsing the repository (Code → Repository)

- **File tree** with breadcrumb navigation; press `y` to freeze the URL to the
  current commit (a permalink that won't move when the branch does).
- **Branch/tag selector** top-left of the file list — switch what you're
  viewing.
- On a file: **Blame** (per-line last-change, like `git blame`), **History**
  (commits touching this file), **Permalink**, and **Open in Web IDE**.
- **Find file** button (or press `t`) — fuzzy file search.
- Press `.` anywhere in a repo to open the **Web IDE** (see below).

## Compare and history

- **Code → Commits** — the commit list for a branch, filterable.
- **Code → Compare** — pick any two refs (branches, tags, SHAs) and see the
  diff and commit list between them. This is `git diff a b` in the browser.
- Each commit page shows its full diff, the pipeline that ran for it, and
  comments.

## The Web IDE

A full editor in the browser (press `.` in a repo, or **Edit → Web IDE** on a
file). Use it for:

- Quick doc/config fixes without cloning.
- Editing several files in one go — it stages them and lets you **commit to a
  new branch and start an MR** in one action.
- It runs the same VS Code editor engine, including search across files.

There's also **single-file editing**: open a file → **Edit** (pencil) → change →
scroll down → write a commit message → choose "commit to a new branch" (keep
this checked for protected branches) → **Commit changes**. GitLab offers to open
an MR next.

> For anything more than a few lines, still clone and work locally — you get
> your tools, your linters, and the ability to run the code.

## The Web Terminal / GitLab Duo (awareness)

Some setups offer a browser terminal (via a runner) and AI assistance (GitLab
Duo, paid). Not covered here; mentioned so you know what those buttons are.

## Tags and releases (Deploy → Releases, Code → Tags)

- A **tag** is a git tag — a fixed label on a commit, usually a version
  (`v1.4.0`). Create from **Code → Tags → New tag**, or `git tag v1.4.0 &&
  git push origin v1.4.0`.
- A **release** is GitLab's wrapper around a tag: release notes, linked
  milestones, downloadable assets, and a permanent page. Create from **Deploy →
  Releases → New release**. CI can create releases automatically (Module 09).

## Snippets

Standalone code/text fragments, not part of any repo — for sharing a script, a
log, a config sample. **Personal snippets** (your namespace) or **project
snippets** (`Code → Snippets`, if enabled). Each snippet is itself a tiny git
repo. Good for throwaway sharing; bad as a home for anything that should be
version-controlled with real code.

## Wiki

Each project (and group) can have a **wiki** — a separate git repo of Markdown
pages for documentation that isn't code: architecture notes, runbooks,
onboarding. **Plan → Wiki**. You can clone it (`...project.wiki.git`) and edit
offline. Keep *developer* docs (READMEs, ADRs) in the main repo next to the
code; use the wiki for living operational docs.

## GitLab Pages

Static site hosting straight from a project. A CI job publishes a folder
(usually `public/`) and GitLab serves it at
`https://your-group.gitlab.io/your-project/`. Used for docs sites, coverage
reports, project landing pages. Setup is a `pages` job in `.gitlab-ci.yml`
(Module 09 touches this).

## Keyboard shortcuts

Press `?` anywhere for the list. The useful ones:

| Key | Action |
| --- | --- |
| `t` | Find file in repo |
| `.` | Open Web IDE |
| `y` | Permalink to current file at this commit |
| `g` then `i` | Go to Issues |
| `g` then `m` | Go to Merge requests |
| `g` then `p` | Go to Pipelines |
| `r` | Reply / quote in a discussion (on MR/issue pages) |

## Check yourself

1. You need to fix one typo in `README.md` and you're on someone else's laptop.
   What's the fastest safe route?
2. What's the difference between a tag and a release in GitLab?
3. Where does developer-facing documentation belong — the wiki or the repo? Why?
4. What does pressing `y` on a file page give you?

<details>
<summary>Answers</summary>

1. Open the file in the GitLab web UI → **Edit** → make the change → commit **to
   a new branch** → let GitLab open a merge request. No clone, no credentials on
   the borrowed machine beyond the web login.
2. A tag is a plain git tag (a label on a commit). A release is GitLab's layer
   on top: notes, assets, linked milestones, and a dedicated page — always tied
   to a tag.
3. In the repo, next to the code, so it versions and reviews together with the
   code it describes. The wiki is better for operational/living docs
   (runbooks, onboarding) that aren't tied to a specific code version.
4. A permalink to that file *at the current commit SHA*, so the link keeps
   pointing at the same content even after the branch moves on.

</details>

Next: [Module 04 — Issues & planning](04-issues-and-planning.md)
