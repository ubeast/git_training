# Module 00 — Why version control in Databricks

## The problem with the bare workspace

Open a Databricks workspace and you get folders of notebooks. Databricks keeps an
automatic **revision history** for each notebook (the sidebar clock icon) — which
is better than nothing, but:

- It's **per notebook**. There's no "this change spanned five notebooks and a
  config file" — no atomic commits across files.
- There's **no branching**. You can't try a risky change in isolation and throw
  it away cleanly.
- There's **no review**. A teammate can't comment on a proposed change before it
  becomes the live version.
- There's **no promotion path**. Getting a tested notebook from a dev workspace
  to a prod workspace means copy-paste or `dbutils` scripting.
- History lives **inside one workspace**. Lose or migrate the workspace and it's
  gone. It's not portable, not diffable in familiar tools, not backed by your
  org's git hosting.

Every one of those is something git already solves — for code. The trick is
making notebooks behave like code.

## What Databricks adds

```
   your git provider                     your Databricks workspace
   (GitHub / GitLab / ADO)                ┌──────────────────────────────┐
   ┌───────────────────┐                  │  Git folder = a clone         │
   │  the repo          │ ◄── push/pull ──┤   /Workspace/Users/you/myrepo │
   │  branches, PRs,    │                  │   ├── notebooks/*.py          │
   │  reviews, releases │ ──── clone  ───► │   ├── src/*.py                │
   └───────────────────┘                  │   └── databricks.yml          │
            ▲                              │                              │
            │                              │  edit notebooks in the UI,   │
            │  jobs can also run           │  commit & push from the      │
            │  code straight from a        │  "Git" dialog                │
            └──── branch / tag / commit ───┘                              │
                                           └──────────────────────────────┘
```

Three capabilities:

1. **Git folders** (formerly called **Repos**) — a real git clone that lives in
   your workspace. You edit its notebooks in the Databricks editor and run
   `commit`, `push`, `pull`, and branch operations from a **Git dialog**. The
   branching, PRs, and merges happen in your provider like any other repo.

2. **Notebooks stored as source text** — a Python notebook is a `.py` file with
   special comment markers (Module 02). Cell outputs are *not* committed by
   default. So `git diff` on a notebook shows readable line changes, and reviews
   in GitHub/GitLab work normally.

3. **Git as a runtime source** — a job (workflow) or Delta Live Tables pipeline
   can be told to run notebooks *directly from a repo* at a specific branch,
   tag, or commit, instead of from a workspace path (Module 07). This is how you
   run tested, pinned code in production without copying anything into the prod
   workspace by hand.

On top of those, **Databricks Asset Bundles** (Module 08) package jobs,
pipelines, and notebooks with per-environment config so CI/CD can deploy them.

## The mental model

> **A Git folder is an ordinary git working copy that happens to be rendered in
> the Databricks UI instead of a file explorer. The Git dialog is a GUI for
> `git`. Nothing about branching, merging, or pull requests changes — only
> *where* you click the buttons.**

Keep asking "what is this at the git CLI?" The answers:

| In Databricks | At the git CLI |
| --- | --- |
| Create Git folder from URL | `git clone <url>` |
| Git dialog → Create branch | `git switch -c <name>` |
| Git dialog → Commit & Push | `git commit -am "..."` + `git push` |
| Git dialog → Pull | `git pull` |
| Git dialog → branch dropdown | `git switch <name>` |
| Git dialog → Discard changes | `git restore .` / `git reset --hard` |
| "Merge" / "Resolve" a PR | done in the provider, not Databricks |

## What this course covers

- **01–06**: getting your notebooks into git and working day to day — connect,
  the source format, Git folders, the commit loop, conflicts, the PR workflow.
- **07**: running jobs from a repo instead of the workspace.
- **08–10**: CI/CD — Asset Bundles, pipelines, and how dev/staging/prod,
  service principals, and secrets fit together.
- **11**: the habits that keep notebook-based repos sane.

## Check yourself

1. Databricks already keeps notebook revision history. Name two things it does
   *not* give you that git does.
2. A "Git folder" in your workspace — what is it, in git terms?
3. Where do pull requests and code review happen for a Databricks Git folder?
4. What does "run a job from Git" mean, and why would production use it?

<details>
<summary>Answers</summary>

1. Any two of: atomic commits spanning multiple files, branching, pre-merge code
   review, a portable history backed by your git host, a promotion path between
   workspaces/environments.
2. A real git clone (working copy) of a repo, stored inside the Databricks
   workspace and edited through the Databricks UI.
3. In your git provider (GitHub, GitLab, Azure DevOps…), not in Databricks.
   Databricks pushes the branch; you open and merge the PR in the provider.
4. The job runs notebooks pulled straight from a repo at a specified branch, tag,
   or commit — nothing is copied into the workspace by hand. Production pins to a
   **tag or commit** so it runs exactly the reviewed, released code.

</details>

Next: [Module 01 — Connecting to your git provider](01-connecting-git-provider.md)
