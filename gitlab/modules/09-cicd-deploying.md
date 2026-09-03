# Module 09 — CI/CD: deploying & scaling up

Module 08 got a pipeline running tests. This module covers deploying with it,
and the keywords that keep a growing `.gitlab-ci.yml` manageable.

## Environments

An **environment** is a named deploy target GitLab tracks — `staging`,
`production`, `review/feature-x`. Declaring one on a job makes GitLab record
every deployment: what commit, by whom, when, and whether it's current.

```yaml
deploy-staging:
  stage: deploy
  script:
    - ./deploy.sh https://staging.example.com
  environment:
    name: staging
    url: https://staging.example.com      # clickable "View deployment" button
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

**Deploy → Environments** then shows `staging` with its deployment history, the
current commit, and a **re-deploy** / **rollback** button (rollback re-runs the
job for an earlier commit).

### Stopping environments

For dynamic environments (per-branch), pair a stop job:

```yaml
deploy-review:
  stage: deploy
  script: ./deploy-review.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    url: https://$CI_COMMIT_REF_SLUG.review.example.com
    on_stop: stop-review
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"

stop-review:
  stage: deploy
  script: ./teardown-review.sh
  environment:
    name: review/$CI_COMMIT_REF_SLUG
    action: stop
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
```

When the MR merges or closes, GitLab runs `stop-review` and tears down the
environment. This pattern is **Review Apps**: every MR gets its own live
preview URL.

## Manual jobs and gates

`when: manual` makes a job wait for a human to click ▶ in the pipeline:

```yaml
deploy-production:
  stage: deploy
  script: ./deploy.sh production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  allow_failure: false      # a skipped manual job won't block the pipeline unless this is false
```

- **Protected environments** (Settings → CI/CD → Protected environments) — limit
  *who* can run the deploy job for `production` to specific users/roles. This is
  the real production gate.
- `when: delayed` + `start_in: 30 minutes` — a timed auto-deploy you can cancel.

## `needs:` — break out of stage ordering (DAG)

Normally a job waits for its whole previous stage. `needs:` lets a job start as
soon as *specific* jobs finish:

```yaml
build-frontend:
  stage: build
  script: ...

build-backend:
  stage: build
  script: ...

test-frontend:
  stage: test
  needs: [build-frontend]      # starts the moment build-frontend is done,
  script: ...                  # doesn't wait for build-backend
```

This turns the pipeline into a dependency graph (DAG) and can cut total time
significantly. `needs:` also pulls that job's artifacts. `needs: []` = start
immediately, no waiting.

## `include:` — split and reuse config

Keep `.gitlab-ci.yml` small by pulling in other files:

```yaml
include:
  - local: .gitlab/ci/tests.yml
  - local: .gitlab/ci/deploy.yml
  - project: 'acme/ci-templates'
    ref: v2.1.0
    file: '/python.yml'
  - template: 'Security/SAST.gitlab-ci.yml'      # GitLab-provided
  - remote: 'https://example.com/ci/shared.yml'
```

- `local` — another file in this repo.
- `project` — a file from another GitLab project (pin `ref`!).
- `template` — one of GitLab's built-in templates (SAST, Dependency Scanning,
  code quality…).
- `component` (newer) — a versioned **CI/CD Component** from the catalog:
  ```yaml
  include:
    - component: gitlab.com/components/ruby/lint@1.0
  ```

## `extends:` and YAML anchors — DRY jobs

```yaml
.test-base:                    # hidden job (leading dot) — a template, never runs
  image: python:3.12
  before_script:
    - pip install -r requirements.txt

unit-tests:
  extends: .test-base
  script: pytest tests/unit

integration-tests:
  extends: .test-base
  script: pytest tests/integration
```

`extends` merges the hidden job into the real one. Cleaner than YAML anchors
(`&`/`*`), which also work but are harder to read.

## `parallel` and matrix jobs

```yaml
test:
  stage: test
  parallel: 4                       # 4 copies; split tests with CI_NODE_INDEX/CI_NODE_TOTAL
  script: ./run-shard.sh

test-versions:
  stage: test
  parallel:
    matrix:
      - PYTHON: ["3.10", "3.11", "3.12"]
  image: python:$PYTHON
  script: pytest
```

## Scheduled pipelines

**Build → Pipeline schedules → New schedule** — run a pipeline on a cron
schedule (nightly builds, dependency-update checks, data refreshes),
optionally with schedule-specific variables. Gate jobs to schedules with:

```yaml
  rules:
    - if: $CI_PIPELINE_SOURCE == "schedule"
```

## Child pipelines

A job can generate and trigger a whole separate pipeline:

```yaml
trigger-deploy-pipeline:
  stage: deploy
  trigger:
    include: .gitlab/ci/deploy-pipeline.yml
    strategy: depend        # parent job's status mirrors the child pipeline's
```

Used for monorepos (one child pipeline per service) and dynamically generated
config.

## Releases from CI

```yaml
create-release:
  stage: deploy
  image: registry.gitlab.com/gitlab-org/release-cli:latest
  rules:
    - if: $CI_COMMIT_TAG
  script:
    - echo "Releasing $CI_COMMIT_TAG"
  release:
    tag_name: $CI_COMMIT_TAG
    description: "Release $CI_COMMIT_TAG"
```

Push a tag → GitLab creates a Release page (Module 03) automatically.

## GitLab Pages

```yaml
pages:
  stage: deploy
  script:
    - mkdocs build -d public       # must output to ./public
  artifacts:
    paths:
      - public
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

The job **must** be named `pages` and produce a `public/` artifact. Site is
served at `https://<group>.gitlab.io/<project>/`.

## The Deploy view and rollbacks

- **Deploy → Environments** → an environment → its deployment list. Each entry
  has **Re-deploy** and (for older ones) **Rollback**, both of which just re-run
  the deploy job pinned to that commit.
- **Operate → Releases** for the tagged release history.

## Check yourself

1. What does declaring `environment: name: production` on a job give you beyond
   just running a script?
2. How do you make a production deploy wait for a person to click a button, and
   restrict *who* can click it?
3. `test-frontend` only depends on `build-frontend`, but it's waiting for
   `build-backend` too. What keyword fixes that?
4. You want the same `before_script` in five jobs without copy-pasting. Two
   options?
5. Where must a GitLab Pages job put its output, and what must the job be
   called?

<details>
<summary>Answers</summary>

1. GitLab tracks deployments: history of which commit is live, who deployed,
   when; a "View deployment" link; and re-deploy / rollback buttons on the
   Environments page.
2. `when: manual` on the job (adds the ▶ button), plus a **protected
   environment** for `production` limiting which users/roles may run it.
3. `needs: [build-frontend]` — it starts as soon as that job finishes,
   ignoring the rest of the build stage.
4. A hidden job (`.base:`) that the five jobs `extends:`, or a YAML anchor.
   `extends` is preferred for readability.
5. Output goes in `public/`, and the job must be named `pages`.

</details>

Next: [Module 10 — GitLab Flow](10-gitlab-flow.md)
