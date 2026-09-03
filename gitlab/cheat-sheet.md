# GitLab Cheat Sheet

For git commands themselves, see [`../git/cheat-sheet.md`](../git/cheat-sheet.md).
This page is the GitLab layer.

## Connecting

```bash
ssh-keygen -t ed25519 -C "you@example.com"      # make a key
cat ~/.ssh/id_ed25519.pub                        # → paste into GitLab: Profile → SSH Keys
ssh -T git@gitlab.com                            # test → "Welcome to GitLab, @you!"

git remote set-url origin git@gitlab.com:group/project.git   # switch HTTPS → SSH
```

HTTPS instead: create a **Personal Access Token** (Profile → Access Tokens,
scope `write_repository`), use it as the password. Cache it:
`git config --global credential.helper osxkeychain` (mac) / `manager` (win).

## Push an existing repo to a new empty project

```bash
git remote add origin git@gitlab.com:group/project.git
git push -u origin main
```

## Roles (least → most)

`Guest` (view/comment) · `Reporter` (+ read code, issues, pipelines) ·
`Developer` (+ push unprotected branches, MRs) · `Maintainer` (+ merge protected
branches, settings, CI vars) · `Owner` (+ delete/transfer).
Developers **cannot** merge to a protected `main` by default.

## Quick actions (type in any issue/MR comment)

| | |
| --- | --- |
| `/assign @me` | `/unassign` |
| `/label ~"type::bug"` | `/unlabel ~"..."` |
| `/milestone %"Sprint 24"` | `/due 2026-10-01` |
| `/estimate 3h` · `/spend 1h` | `/weight 3` |
| `/close` · `/reopen` | `/relate #42` |
| `/draft` (MR) | `/assign_reviewer @lee` (MR) |
| `/target_branch release/2.0` (MR) | `/rebase` (MR) |

## MR description keywords

| Keyword | Effect |
| --- | --- |
| `Closes #42` / `Fixes #42` / `Resolves #42` | Auto-close the issue on merge to default branch |
| `Closes group/other#42` | Same, cross-project |
| `Related to #42` | Link without auto-closing |
| `Draft:` title prefix | MR can't be merged until "Mark as ready" |

## Merge widget unlocks when

pipeline passed (if required) · approvals met · threads resolved (if required)
· no conflicts · not a Draft · you can merge the target branch.

## `.gitlab-ci.yml` skeleton

```yaml
stages: [build, test, deploy]

default:
  image: python:3.12
  cache:
    key: { files: [requirements.txt] }
    paths: [.pip-cache/]

build:
  stage: build
  script: [pip install -r requirements.txt, python -m build]
  artifacts:
    paths: [dist/]
    expire_in: 1 week

test:
  stage: test
  script: [pytest --junitxml=report.xml]
  artifacts:
    when: always
    reports: { junit: report.xml }

deploy:
  stage: deploy
  script: [./deploy.sh production]
  environment: { name: production, url: https://example.com }
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

## `.gitlab-ci.yml` keywords

| Keyword | Purpose |
| --- | --- |
| `stages` | Ordered list of phases |
| `stage:` | Which phase a job is in (jobs in a stage run in parallel) |
| `image:` / `services:` | Container the job runs in / linked containers (db, etc.) |
| `script:` / `before_script:` / `after_script:` | Commands; non-zero exit fails the job |
| `rules:` (`if`, `changes`, `when`) | Whether the job is added to the pipeline |
| `when:` | `on_success` (default) · `manual` · `always` · `on_failure` · `delayed` · `never` |
| `artifacts:` (`paths`, `reports`, `expire_in`, `when`) | Files to keep / pass downstream |
| `cache:` (`key`, `paths`) | Best-effort reuse of deps between pipelines |
| `needs:` | Start when named jobs finish (DAG); `needs: []` = start now |
| `environment:` (`name`, `url`, `action`, `on_stop`) | Deploy target GitLab tracks |
| `variables:` | Env vars for the job/pipeline |
| `extends:` / `.hidden-job:` | Reuse job templates |
| `include:` (`local`, `project`, `template`, `component`, `remote`) | Pull in other CI config |
| `parallel:` / `parallel: matrix:` | Run N copies / a build matrix |
| `trigger:` | Start a child/downstream pipeline |
| `allow_failure:` | Job can fail without failing the pipeline |
| `tags:` | Require a runner with these tags |

## Useful predefined CI variables

| Variable | Is |
| --- | --- |
| `CI_COMMIT_BRANCH` | Current branch (empty for tags/MRs) |
| `CI_DEFAULT_BRANCH` | The repo's default branch name |
| `CI_COMMIT_SHA` / `CI_COMMIT_SHORT_SHA` | Commit hash |
| `CI_COMMIT_TAG` | Tag name (only on tag pipelines) |
| `CI_PIPELINE_SOURCE` | `push` · `merge_request_event` · `schedule` · `web` · `trigger` … |
| `CI_COMMIT_REF_SLUG` | Branch/tag, sanitised for URLs/env names |
| `CI_PROJECT_DIR` | Checkout path on the runner |
| `CI_REGISTRY` / `CI_REGISTRY_IMAGE` | Container registry host / this project's image path |
| `CI_JOB_TOKEN` | Short-lived token for API calls from a job |

## Common `rules:` conditions

```yaml
- if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH          # on main
- if: $CI_PIPELINE_SOURCE == "merge_request_event"     # MR pipelines
- if: $CI_COMMIT_TAG                                    # tag pipelines
- if: $CI_PIPELINE_SOURCE == "schedule"                # scheduled runs
- if: $CI_COMMIT_BRANCH =~ /^release\//                # release/* branches
- changes: ["**/*.py"]                                  # only if Python files changed
```

## `glab` CLI

```bash
glab auth login
glab repo clone group/project
glab mr create --fill [--draft] [--target-branch main]
glab mr list [--mine]
glab mr view 17 [--web]
glab mr checkout 17
glab mr merge 17 --squash --remove-source-branch
glab mr approve 17
glab issue create --title "..." --label "type::bug"
glab issue list [--assignee @me]
glab ci view              # live pipeline for the current branch
glab ci status
glab ci lint              # validate .gitlab-ci.yml
glab ci trace <job>       # stream a job log
glab variable set KEY value --masked --protected
```

## Protect `main` — Free-tier team baseline

Settings → Repository → Protected branches: **Allowed to push and merge = No
one**, **Allowed to merge = Maintainers**.
Settings → Merge requests: **Pipelines must succeed** ✓, **All threads resolved**
✓, **Approvals required = 1**, **author can't approve** ✓, **remove approvals on
new commits** ✓.
Add `CODEOWNERS` for sensitive paths. Default **delete source branch** ✓.

## "Is this a git problem or a GitLab problem?"

| Symptom | Layer | Look at |
| --- | --- | --- |
| `Permission denied (publickey)` | git/auth | SSH key setup (Module 01) |
| `not allowed to push to protected branches` | GitLab | Protected branch settings (Module 07) |
| Merge button greyed out | GitLab | Merge widget checklist — pipeline/approvals/threads/role |
| Merge conflict on the MR | git | Resolve on your branch: `git merge origin/main` (Module 05) |
| `HTTP Basic: Access denied` | git/auth | Using password not token, or token expired/lacks scope |
| Pipeline job "stuck" / no runner | GitLab | Runners enabled? job `tags:` match? (Module 08) |
| Job can't see a secret | GitLab | Variable not `protected` but branch is unprotected, or wrong env scope |
