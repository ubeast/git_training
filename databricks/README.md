# Git in Databricks Training

A hands-on introduction to using **git and version control inside Databricks** —
tracking notebooks, collaborating through a git provider, running jobs from a
repo, and shipping to production with CI/CD.

## Who this is for

Data engineers, analysts, and scientists who work in Databricks notebooks and
need their work under version control. You should have finished the
[Git course](../git/) (or know git: `branch`, `commit`, `push`, `pull`, merge
conflicts, pull requests). The [GitLab course](../gitlab/) is helpful for the
CI/CD modules but not required — this course uses GitHub in its examples and
notes the GitLab equivalents.

## What "git in Databricks" actually means

Databricks doesn't replace git or your git provider. It adds:

| Piece | What it is |
| --- | --- |
| **Linked git credentials** | You tell Databricks how to authenticate to GitHub / GitLab / Azure DevOps on your behalf |
| **Git folders** (formerly "Repos") | A clone of a repo, living in your Databricks workspace, that you edit and commit from the Databricks UI |
| **Notebook source format** | Notebooks are stored as readable `.py` / `.sql` / `.ipynb` text files so git diffs make sense |
| **Git as a job source** | A job/workflow can run notebooks straight from a repo branch, tag, or commit — not from the workspace |
| **Databricks Asset Bundles** | A config format (`databricks.yml`) + CLI to deploy jobs, pipelines, and notebooks from a repo, per environment |

The actual branching, merging, and pull requests still happen in git and in your
provider. Databricks is the editor and the runtime.

## What you need before you start

1. **A Databricks workspace** you can log into, on a plan that includes **Git
   folders** and **Repos** (all current AWS/Azure/GCP paid tiers; not Community
   Edition).
2. **An account with a git provider** — GitHub is used in the examples
   (gitlab.com works too; Azure DevOps and Bitbucket are supported).
3. **A personal access token** from that provider (or OAuth — Module 01).
4. For the CI/CD modules (08–09): the **Databricks CLI** (v0.205+) installed
   locally, and permission to create jobs and (ideally) a service principal.
5. Git installed locally is useful for the "drop to a terminal" cases but not
   required for most of the course.

> **Which cloud?** The concepts are identical on Databricks-on-AWS, Azure
> Databricks, and Databricks-on-GCP. Where a menu path or auth detail differs
> (mainly Azure DevOps integration and Azure Key Vault secret scopes), it's
> called out.

## The modules (read in order)

| # | Module | What you learn |
| --- | --- | --- |
| 00 | [Why version control in Databricks](modules/00-why-version-control-in-databricks.md) | The problem with notebooks in the bare workspace; how Git folders fix it |
| 01 | [Connecting to your git provider](modules/01-connecting-git-provider.md) | Linked git credentials, PAT vs OAuth, supported providers, admin settings |
| 02 | [Notebooks as source files](modules/02-notebooks-as-source.md) | The `# Databricks notebook source` format, `.py` vs `.ipynb`, why outputs aren't committed |
| 03 | [Git folders: your first clone](modules/03-git-folders.md) | Creating a Git folder, what it is, personal vs shared, browsing it |
| 04 | [The everyday Git loop in Databricks](modules/04-everyday-loop.md) | Branch, edit, commit & push, pull — the Git dialog, mapped to git CLI |
| 05 | [Conflicts & recovery](modules/05-conflicts-and-recovery.md) | Resolving conflicts in the Git dialog, discarding changes, when to use a terminal |
| 06 | [A collaboration workflow](modules/06-collaboration-workflow.md) | Feature branch → push → PR in the provider → review → merge; keeping folders synced |
| 07 | [Running jobs from Git](modules/07-jobs-from-git.md) | Jobs/workflows with a Git source; why prod runs from a tag or commit |
| 08 | [CI/CD with Databricks Asset Bundles](modules/08-asset-bundles.md) | `databricks.yml`, resources, targets, `bundle validate / deploy / run` |
| 09 | [Automating with CI pipelines](modules/09-cicd-pipelines.md) | GitHub Actions / GitLab CI running the CLI; validate on PR, deploy on merge/tag |
| 10 | [Environments, identities & secrets](modules/10-environments-identities-secrets.md) | dev/staging/prod, service principals, secret scopes, never hardcoding |
| 11 | [Everyday good habits](modules/11-good-habits.md) | Small notebooks, logic in modules, no dual-editing, `.gitignore`, no data in git |

## The exercises

| Exercise | Do it after | Skill |
| --- | --- | --- |
| [01 — Connect & first Git folder](exercises/01-connect-and-first-git-folder/) | Module 01–04 | Link credentials, create a Git folder, branch, commit & push |
| [02 — Notebook diffs & the source format](exercises/02-notebook-diffs/) | Module 02 | Read the committed file, confirm outputs aren't committed, read a diff |
| [03 — A notebook merge conflict](exercises/03-notebook-conflict/) | Module 05 | Create and resolve a conflict in one notebook cell |
| [04 — Feature branch → PR → merge](exercises/04-branch-pr-merge/) | Module 06 | The full loop through the provider |
| [05 — Run a job from Git](exercises/05-run-job-from-git/) | Module 07 | A workflow with a Git source; repoint from branch to tag |
| [06 — Deploy an Asset Bundle](exercises/06-asset-bundle/) | Module 08 | `bundle init` → `validate` → `deploy -t dev` → `run` |

## Also in this folder

- [`cheat-sheet.md`](cheat-sheet.md) — the Git dialog, notebook format markers, `databricks bundle` commands, auth env vars
- [`instructor-guide.md`](instructor-guide.md) — for whoever runs the session
- [`videos/links.md`](videos/links.md) — short videos and the canonical Databricks docs

## The one thing to remember

**A Git folder is a real git clone that happens to live in your workspace.**
Every confusing moment resolves faster if you ask "what would this be at the git
CLI?" — the Git dialog's Commit & Push, Pull, and Create Branch are exactly
`git commit`/`git push`, `git pull`, and `git switch -c`. The branching strategy,
reviews, and merges are ordinary git, done in your provider.
