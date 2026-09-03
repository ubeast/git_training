# Module 03 — Git folders: your first clone

A **Git folder** (the feature was called **Repos** until 2024; you'll see both
names) is a git clone that lives in your Databricks workspace.

## Creating one

In the workspace sidebar: **Workspace → your home folder → (or any folder) →
Create → Git folder** (or the **Add** / **+** menu → **Git folder**).

| Field | Notes |
| --- | --- |
| **Git repository URL** | The HTTPS clone URL, e.g. `https://github.com/acme/pipelines.git` |
| **Git provider** | Auto-detected from the URL; must match your linked credentials (Module 01) |
| **Git folder name** | Defaults to the repo name; this is the folder name in your workspace |
| **Sparse checkout** (optional) | Clone only certain subdirectories — for big monorepos |

Click **Create Git folder**. Databricks clones the repo (default branch) into
that workspace path.

## Where it lives

- Historically Git folders were confined to `/Repos/<your-email>/`.
- Current workspaces allow Git folders **anywhere in the workspace tree** —
  commonly your user folder `/Workspace/Users/you@example.com/<repo>` for
  personal work, or a shared folder for a team clone.
- The path matters for `%run` relative paths and for jobs that reference a
  workspace notebook path (though jobs should use a **Git source** instead —
  Module 07).

## What you can do in it

Open the Git folder. It looks like any workspace folder, but:

- The folder header shows the **current branch** and a **Git icon/button**
  (the "Git dialog").
- Notebooks open in the normal editor. Other files open in the file editor.
- Edits are tracked against the clone — the Git dialog shows what changed.

## Personal vs shared Git folders

| Pattern | How | Good for |
| --- | --- | --- |
| **Personal Git folder** | Each person creates their own clone under their user folder | Day-to-day development — everyone on their own branch, own uncommitted state |
| **Shared/production Git folder** | One clone in a shared location, usually pinned to `main` or a release tag, updated by automation or an admin | A stable copy others read from; running notebooks interactively against "what's in prod" |

**The important rule:** a personal dev Git folder is *yours*. Two people should
not be committing from the same Git folder — the uncommitted working state is
shared and you'll clobber each other. Collaboration happens through **branches
and PRs in the provider**, not through a shared working copy.

## Limits and what doesn't belong

Git folders are for **code and config**, not data. Current guidance (check the
docs for exact numbers — they change):

| Limit | Rough value | Why it matters |
| --- | --- | --- |
| Repo size | Keep well under ~200 MB; hard cap higher | Large repos clone slowly and hit workspace storage limits |
| Single file size (editable in UI) | ~10 MB | Bigger files can be in the repo but not opened/edited in Databricks |
| Number of files | Thousands is fine; tens of thousands degrades the UI | The workspace file tree has to render it |
| File types | Any, now — but... | ...binaries and data files bloat history forever |

**Do not commit**: datasets, parquet/CSV data dumps, model binaries, `.env`
files, credentials, large notebook outputs. Use a `.gitignore` (it works in Git
folders) and store data in cloud storage / Unity Catalog volumes / tables.

## Refreshing a Git folder

- **Git dialog → Pull** brings the current branch up to date.
- If a Git folder gets into a weird state, it's cheap to **delete it and
  re-create it** from the URL — there's nothing precious in the clone itself
  that isn't in the provider (as long as you've pushed your branch).

## The Databricks CLI and Git folders

You can script Git folder operations:

```bash
databricks repos create --url https://github.com/acme/pipelines.git --provider gitHub \
  --path /Workspace/Users/you@example.com/pipelines
databricks repos update <repo-id> --branch feature-x
databricks repos list
```

Useful for CI that needs "a workspace clone at branch X" — though **Asset
Bundles** (Module 08) are the better path for most automation.

## Check yourself

1. In git terms, what happens when you click "Create Git folder"?
2. Can two teammates share one Git folder and both commit from it? Why / why
   not?
3. Where should a 500 MB training dataset live — in the Git folder or
   elsewhere?
4. Your Git folder is in a broken state after a bad operation. What's the
   low-risk recovery?

<details>
<summary>Answers</summary>

1. `git clone <url>` into a path inside your Databricks workspace, checked out
   on the repo's default branch.
2. No. A Git folder has one shared working state (current branch, uncommitted
   changes). Two people committing from it overwrite each other. Each person
   should have their own Git folder and collaborate via branches + PRs in the
   provider.
3. Elsewhere — a Unity Catalog volume, cloud object storage, or a table. Git
   folders are for code and config; data bloats the repo and hits size limits.
4. Make sure your branch is pushed, then delete the Git folder and re-create it
   from the URL. The clone holds nothing that isn't recoverable from the
   provider.

</details>

Next: [Module 04 — The everyday Git loop in Databricks](04-everyday-loop.md)
