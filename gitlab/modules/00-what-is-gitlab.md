# Module 00 — What GitLab is

## Where GitLab sits

Git is a tool that runs on your laptop. It has no idea about servers, teams,
permissions, or running your tests. A **git hosting platform** wraps a git
server with a web application that adds all of that. GitLab is one such
platform. GitHub and Bitbucket are others.

```
        ┌─────────────────────── GitLab ───────────────────────┐
        │                                                       │
        │   a git server        +   a web app on top:           │
        │   (hosts your repos)       - issues & boards           │
        │                            - merge requests & review   │
        │                            - CI/CD pipelines            │
        │                            - roles & access control     │
        │                            - wiki, pages, container reg. │
        └───────────────────────────────────────────────────────┘
                     ▲
                     │  git push / git pull   (ordinary git — unchanged)
                     │  + the web UI and API for everything else
                     ▼
              your laptop
```

Your git workflow doesn't change. `git push` still just uploads commits. GitLab
is about what the *team* does with those commits once they land.

## GitLab vs GitHub

If you know GitHub, GitLab maps almost one-to-one:

| GitHub | GitLab |
| --- | --- |
| Repository | Project |
| Organization | Group (groups can nest; orgs can't) |
| Pull Request (PR) | Merge Request (MR) |
| GitHub Actions | GitLab CI/CD (`.gitlab-ci.yml`) |
| Actions workflow file | `.gitlab-ci.yml` (one file, repo root) |
| `CODEOWNERS` | `CODEOWNERS` (same) |
| Issues, Projects, Wiki, Pages | Issues, Boards, Wiki, Pages (same names) |

The biggest practical difference: GitLab ships CI/CD, the container registry,
security scanning, and package hosting **in the box**, and its groups nest
arbitrarily (`company / department / team / project`).

## SaaS vs self-managed

| | **GitLab.com** (SaaS) | **Self-managed** |
| --- | --- | --- |
| Who runs it | GitLab Inc. | Your company's ops team |
| URL | `gitlab.com/your-group/your-project` | `gitlab.yourcompany.com/...` |
| Runners for CI | Shared runners provided (compute quota on free tier) | Your team provides runners |
| Upgrades | Automatic | Your ops team's schedule |
| This course | Works as written | Works — substitute your hostname; ask your admin what's enabled |

Everything you learn applies to both. This course uses **gitlab.com** so you can
follow along without infrastructure.

## Tiers

GitLab has Free, Premium, and Ultimate tiers (and the self-managed equivalents).
Features like multiple *required* approval rules, code-owner approval
enforcement, merge trains, and advanced security scanning are paid. This course
sticks to **Free-tier** features and flags anything that isn't.

## The core objects you'll work with

| Object | What it is |
| --- | --- |
| **Project** | One repository plus its issues, MRs, pipelines, settings, wiki |
| **Group** | A namespace containing projects and/or subgroups, with shared members and settings |
| **Issue** | A unit of work to do — a bug, a feature, a task. Lives in a project. |
| **Merge Request (MR)** | A proposal to merge one branch into another, with diff, discussion, approvals, and pipeline status |
| **Pipeline** | One run of your CI/CD config, made of **jobs** grouped into **stages** |
| **Runner** | A machine (GitLab's or yours) that executes pipeline jobs |
| **Environment** | A named deploy target (`staging`, `production`) that GitLab tracks deployments to |

## The loop GitLab is built around

1. An **issue** describes what to do.
2. You branch, commit, push (ordinary git).
3. You open a **merge request** from your branch.
4. A **pipeline** runs automatically — tests, linting, build.
5. Teammates **review**; approval rules are satisfied.
6. The MR **merges** into the default branch (often only if the pipeline passed).
7. A pipeline on the default branch **deploys**.
8. The issue closes (automatically, if the MR said `Closes #123`).

Modules 04–10 walk each step. Everything else in GitLab is in service of this
loop.

## Check yourself

1. Does using GitLab change how `git commit` works?
2. What's the GitLab word for a GitHub "pull request"? For an "organization"?
3. You push to a job that needs to run tests. What executes them — GitLab itself?
4. Name three things GitLab adds on top of a bare git server.

<details>
<summary>Answers</summary>

1. No. Local git is identical. GitLab only affects what happens to commits after
   they reach the server.
2. Merge request; group.
3. A **runner** — a separate machine, either one GitLab provides ("shared
   runners") or one your team hosts.
4. Any three of: merge requests / code review, issues & boards, CI/CD pipelines,
   access roles & protected branches, wiki, pages, container registry, security
   scanning.

</details>

Next: [Module 01 — Getting connected](01-getting-connected.md)
