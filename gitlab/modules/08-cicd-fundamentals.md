# Module 08 — CI/CD fundamentals

CI/CD = **Continuous Integration / Continuous Delivery**. In practice: every
time you push, GitLab automatically runs your tests, linters, and build — and
can deploy. It's driven by one file in your repo.

## The one file: `.gitlab-ci.yml`

Put a file called `.gitlab-ci.yml` at the **root** of your repo. GitLab detects
it and runs a **pipeline** on every push (and for every MR).

Minimal example:

```yaml
stages:
  - test

run-tests:
  stage: test
  image: python:3.12
  script:
    - pip install -r requirements.txt
    - pytest
```

Push that, and GitLab: spins up a `python:3.12` container on a runner, checks
out your code, runs the two `script` lines, and reports pass/fail.

## Vocabulary

| Term | Meaning |
| --- | --- |
| **Pipeline** | One whole run of your CI config, triggered by a push, MR, schedule, etc. |
| **Stage** | A named phase (`build`, `test`, `deploy`). Stages run **in order**. |
| **Job** | One unit of work (`run-tests`, `lint`). Jobs in the **same stage run in parallel**. |
| **Runner** | The machine that executes a job. GitLab-hosted ("shared runners") or self-hosted. |
| **Executor** | *How* a runner runs the job — most commonly `docker` (each job in a fresh container). |
| **Artifact** | Files a job produces that you want to keep or pass to later jobs (build output, reports). |
| **Cache** | Files reused between pipelines to speed things up (dependency downloads). Best-effort, not guaranteed. |

### How stages and jobs fit together

```
stage: build        stage: test              stage: deploy
┌───────────┐        ┌──────────┐ ┌────────┐  ┌────────────┐
│ compile   │  ───►  │ unit     │ │ lint   │  │ deploy-stg │
└───────────┘        └──────────┘ └────────┘  └────────────┘
   (runs first)      (both run in parallel     (runs only if
                      after build succeeds)     test stage passed)
```

If any job in a stage fails, later stages don't run (unless you say otherwise).

## A realistic pipeline

```yaml
stages:
  - build
  - test
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"

default:
  image: python:3.12
  cache:
    key:
      files:
        - requirements.txt        # cache invalidates when deps change
    paths:
      - .pip-cache/

build:
  stage: build
  script:
    - pip install -r requirements.txt
    - python -m build
  artifacts:
    paths:
      - dist/
    expire_in: 1 week

unit-tests:
  stage: test
  script:
    - pip install -r requirements.txt
    - pytest --junitxml=report.xml
  artifacts:
    when: always
    reports:
      junit: report.xml           # GitLab shows test results in the MR

lint:
  stage: test
  script:
    - pip install ruff
    - ruff check .

deploy-staging:
  stage: deploy
  script:
    - ./deploy.sh staging
  environment:
    name: staging
  rules:
    - if: $CI_COMMIT_BRANCH == "main"      # only deploy from main
```

## Runners

A job needs a runner to execute on.

- **GitLab.com shared runners**: provided, Linux Docker containers, metered in
  "compute minutes" (the Free tier gives a monthly quota; you may need to
  verify your account with a card — no charge — before they're enabled).
- **Self-managed / group / project runners**: your own machines, registered to
  the project or group. Unlimited, and can access your private network.
- Jobs pick runners by **tags**: `tags: [docker, linux]` in a job matches a
  runner registered with those tags. No tag → any runner that accepts untagged
  jobs.

Check what's available: **Settings → CI/CD → Runners**.

## `image` and `services`

- `image:` — the Docker image the job's `script` runs inside. Pick one with your
  toolchain (`node:20`, `golang:1.22`, `python:3.12`). Default for all jobs via
  `default: image:`.
- `services:` — extra containers linked to the job, e.g. a database for tests:
  ```yaml
  unit-tests:
    services:
      - postgres:16
    variables:
      POSTGRES_PASSWORD: test
  ```

## `script`, `before_script`, `after_script`

```yaml
job:
  before_script:
    - pip install -r requirements.txt   # runs before script, every time
  script:
    - pytest                            # the actual work; non-zero exit = job fails
  after_script:
    - ./cleanup.sh                      # runs even if script failed
```

Each line is a shell command. First command to exit non-zero fails the job
(except in `after_script`).

## Artifacts vs cache — don't mix them up

| | **Artifacts** | **Cache** |
| --- | --- | --- |
| Purpose | Keep/pass **outputs** (builds, reports) | Speed up by reusing **inputs** (deps) |
| Guaranteed? | Yes — always uploaded/downloaded | No — best effort, may be missing |
| Scope | Downloaded by later stages' jobs automatically | Restored by key, shared across pipelines |
| If missing | Pipeline likely breaks | Job just rebuilds it — slower, still correct |
| Example | `dist/`, `coverage.xml`, `report.xml` | `node_modules/`, `.pip-cache/`, `.m2/` |

Rule: **never** rely on `cache` for something a later job *needs* — use
`artifacts`.

## CI/CD variables

**Settings → CI/CD → Variables** — key/value pairs injected as environment
variables into every job. Use for secrets and config:

| Flag | Effect |
| --- | --- |
| **Protected** | Only exposed to jobs running on **protected** branches/tags — keep production secrets protected |
| **Masked** | Hidden in job logs (value must meet complexity rules) |
| **Expanded / raw** | Whether `$OTHER_VAR` inside the value is expanded |
| **Environment scope** | Limit a variable to jobs targeting a specific environment |

Also: **group-level variables** (shared by all projects in the group), and
**predefined variables** GitLab sets automatically — `CI_COMMIT_BRANCH`,
`CI_COMMIT_SHA`, `CI_PROJECT_DIR`, `CI_PIPELINE_SOURCE`, `CI_DEFAULT_BRANCH`,
`CI_REGISTRY`, and [many more](https://docs.gitlab.com/ee/ci/variables/predefined_variables.html).

> **Never** put a secret literally in `.gitlab-ci.yml` — it's in the repo. Use a
> masked, protected CI/CD variable.

## Controlling when jobs run: `rules`

`rules` decide whether a job is added to the pipeline:

```yaml
deploy-prod:
  stage: deploy
  script: ./deploy.sh production
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH    # only on main
      when: manual                                    # ...and require a button click
    - when: never                                     # otherwise, don't add this job

run-on-mrs-only:
  script: ./integration-test.sh
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

Common `if` conditions:

| Condition | True when |
| --- | --- |
| `$CI_COMMIT_BRANCH == "main"` | Push to `main` |
| `$CI_PIPELINE_SOURCE == "merge_request_event"` | Pipeline is for an MR |
| `$CI_COMMIT_TAG` | The pipeline is for a tag |
| `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH` | On the default branch, whatever it's named |

`when:` values: `on_success` (default), `always`, `on_failure`, `manual`,
`never`, `delayed`.

`changes:` runs a job only when certain files changed:

```yaml
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        - "**/*.py"
```

> Older configs use `only:`/`except:` instead of `rules:`. `rules:` is the
> current approach — more flexible, and you can't mix the two in one job.

## Reading a pipeline

**Build → Pipelines** → click a pipeline → the graph of stages and jobs.

- Click a job → its **log**. Failed jobs show a red ✗; the log ends at the
  command that failed.
- **Retry** a single job or the whole pipeline (transient failure).
- **Pipeline editor** (**Build → Pipeline editor**): edit `.gitlab-ci.yml` in
  the browser with validation, a visualisation, and a lint tab.
- Every MR shows its pipeline status in the merge widget; every commit page
  links its pipeline.

## `CI Lint`

**Build → Pipeline editor → Validate** tab (or the older **CI Lint** page)
checks your YAML *and* expands `include`s and `rules` so you can see the jobs
that would be created. Use it before pushing config changes.

## Check yourself

1. Two jobs are in the same stage. Do they run in parallel or in sequence?
2. Your `test` job needs the compiled output from the `build` job. `artifacts`
   or `cache`?
3. Where do you put a deployment SSH key — in `.gitlab-ci.yml` or somewhere
   else? Which flags?
4. Write the `rules` condition for "only run this job on merge request
   pipelines."
5. A job fails with "no runner". What are two possible causes?

<details>
<summary>Answers</summary>

1. In parallel — jobs in one stage run concurrently; stages run in order.
2. `artifacts` (with `paths: [dist/]` on `build`). Later stages download
   artifacts automatically. `cache` is best-effort and must never be relied on
   for required inputs.
3. A **CI/CD variable** (Settings → CI/CD → Variables), **masked** and
   **protected**. Never in the YAML — the YAML is in the repo.
4. `- if: $CI_PIPELINE_SOURCE == "merge_request_event"`
5. Shared runners not enabled for the project (account not verified / disabled),
   or the job has a `tags:` value no available runner matches, or all runners
   are offline/busy.

</details>

Next: [Module 09 — CI/CD: deploying & scaling up](09-cicd-deploying.md)
