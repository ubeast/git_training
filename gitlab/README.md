# GitLab Training

A hands-on introduction to **GitLab** — the platform teams use on top of git for
hosting repositories, tracking work, reviewing code, and running CI/CD.

## Who this is for

People who have finished the [Git course](../git/) (or already know git:
`add`/`commit`/`branch`/`merge`/`push`/`pull`/conflicts) and now need to work in
GitLab day to day. We do **not** re-teach git here — we build on it.

## What GitLab adds to git

| git gives you | GitLab adds |
| --- | --- |
| Local version control | A shared server hosting the repo (the "remote") |
| Branches and merges | **Merge requests**: review, discussion, approval before merge |
| Commit history | **Issues, boards, milestones** to plan and track the work |
| Nothing about running code | **CI/CD**: run tests, build, and deploy automatically on every push |
| No access control | **Roles, protected branches, approval rules** |

It's one integrated place for the whole "code → review → ship" loop.

## What you need before you start

1. **Git installed and configured** (Git course, Module 01).
2. **A GitLab account.** Sign up free at <https://gitlab.com>. Everything in
   this course works on the free tier (you may need to verify the account with a
   credit card or phone to use shared CI runners — GitLab's anti-abuse measure,
   no charge).
3. **A terminal** and a text editor.
4. Optional but recommended: the **`glab`** CLI (<https://gitlab.com/gitlab-org/cli>).

> **Self-managed GitLab?** If your company runs its own GitLab, use that instead
> of gitlab.com — swap the hostname in every URL. The concepts are identical.
> Check with your admin about which runners and features are enabled.

## The modules (read in order)

| # | Module | What you learn |
| --- | --- | --- |
| 00 | [What GitLab is](modules/00-what-is-gitlab.md) | GitLab vs git vs GitHub; SaaS vs self-managed; the mental model |
| 01 | [Getting connected](modules/01-getting-connected.md) | SSH keys, personal access tokens, cloning, `glab` |
| 02 | [Projects, groups & roles](modules/02-projects-groups-roles.md) | Namespaces, visibility, creating/importing projects, permission levels |
| 03 | [The GitLab web UI](modules/03-web-ui.md) | Repo browsing, Web IDE, compare, tags & releases, snippets, wiki, pages |
| 04 | [Issues & planning](modules/04-issues-and-planning.md) | Issues, labels, milestones, boards, quick actions, templates |
| 05 | [Merge requests](modules/05-merge-requests.md) | Creating an MR, description templates, linking issues, the MR anatomy |
| 06 | [Code review & merging](modules/06-code-review-and-merging.md) | Reviewing, suggestions, approvals, squash/merge options, merge trains |
| 07 | [Protecting the default branch](modules/07-protecting-branches.md) | Protected branches, approval rules, CODEOWNERS, push rules |
| 08 | [CI/CD fundamentals](modules/08-cicd-fundamentals.md) | `.gitlab-ci.yml`, stages, jobs, runners, pipelines, artifacts, variables |
| 09 | [CI/CD: deploying & scaling up](modules/09-cicd-deploying.md) | Environments, manual & scheduled jobs, `needs`, `include`, review apps |
| 10 | [GitLab Flow](modules/10-gitlab-flow.md) | A branching strategy that ties branches, MRs, and CI/CD together |
| 11 | [Everyday good habits](modules/11-good-habits.md) | MR/issue/pipeline hygiene, secrets, keeping pipelines fast |

## The exercises

| Exercise | Do it after | Skill |
| --- | --- | --- |
| [01 — Connect & push](exercises/01-connect-and-push/) | Module 01–03 | SSH key, create a project, push an existing repo |
| [02 — Issues & boards](exercises/02-issues-and-boards/) | Module 04 | Issues, labels, a board, quick actions |
| [03 — Your first merge request](exercises/03-first-merge-request/) | Module 05–06 | Branch → MR → review → merge, `Closes #` |
| [04 — Protect main](exercises/04-protect-main/) | Module 07 | Protected branch + approval rule; watch a direct push get rejected |
| [05 — Your first pipeline](exercises/05-first-pipeline/) | Module 08 | Write `.gitlab-ci.yml`, break a job, read logs, fix it |
| [06 — A deploy job](exercises/06-deploy-job/) | Module 09 | An `environment`, a manual gate, job dependencies |

## Also in this folder

- [`cheat-sheet.md`](cheat-sheet.md) — `.gitlab-ci.yml` keywords, `glab` commands, MR/issue quick actions
- [`instructor-guide.md`](instructor-guide.md) — for whoever runs the session
- [`videos/links.md`](videos/links.md) — short videos to watch alongside

## The one thing to remember

GitLab doesn't change git — your local `add`/`commit`/`push` are exactly the
same. GitLab is what happens to your commits **after** they reach the server:
review, approval, and automation. When something is confusing, ask "is this a
git thing or a GitLab thing?" — it clarifies where to look.
