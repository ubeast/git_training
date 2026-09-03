# Module 09 — Automating with CI pipelines

Modules 06–08 give you the pieces: PRs into a protected `main`, jobs from Git,
and a bundle that deploys per environment. A **CI pipeline** wires them
together so deployment happens automatically on the right git events.

Examples use **GitHub Actions**; the **GitLab CI** equivalent is shown for each
step (see the [GitLab course](../../gitlab/) Modules 08–09 for the CI concepts).

## The target automation

| Git event | What CI does | Databricks target |
| --- | --- | --- |
| **Pull request opened/updated** | `pytest` on `src/`; `databricks bundle validate`; (optionally) deploy to a PR/dev target and run a smoke job against a staging catalog | dev / ephemeral |
| **Merge to `main`** | `databricks bundle deploy -t staging`; run integration job | staging |
| **Tag `v*` pushed** (or a release) | `databricks bundle deploy -t prod`; optionally run/verify | prod |

## What CI authenticates as

**A service principal per environment**, using **OAuth M2M**:

1. Create a service principal in the Databricks account console (one for
   staging, one for prod — least privilege).
2. Give it a **client ID** and a **client secret** (OAuth secret).
3. Grant it: `CAN_MANAGE` on the target jobs (or workspace admin in
   staging/prod as your org allows), access to the catalogs it writes, and — if
   jobs use a Git source — its own **linked git credential** with repo read
   access.
4. Put the client ID/secret in the CI system's **secrets** store, scoped so
   only the right branch/tag/environment can read them (prod secrets → protected
   / environment-gated).

Never use a person's PAT for deployment automation.

## GitHub Actions

`.github/workflows/databricks.yml`:

```yaml
name: databricks-cicd

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  test-and-validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/                       # unit tests on src/ modules

      - uses: databricks/setup-cli@main          # installs the databricks CLI
      - name: Validate bundle (staging config)
        env:
          DATABRICKS_HOST: ${{ vars.STAGING_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.STAGING_SP_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.STAGING_SP_SECRET }}
        run: databricks bundle validate -t staging

  deploy-staging:
    needs: test-and-validate
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging                          # GitHub environment = gated secrets
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - env:
          DATABRICKS_HOST: ${{ vars.STAGING_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.STAGING_SP_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.STAGING_SP_SECRET }}
        run: |
          databricks bundle deploy -t staging
          databricks bundle run integration_smoke -t staging

  deploy-prod:
    needs: test-and-validate
    if: startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: prod                             # add required reviewers on this env
    steps:
      - uses: actions/checkout@v4
      - uses: databricks/setup-cli@main
      - env:
          DATABRICKS_HOST: ${{ vars.PROD_HOST }}
          DATABRICKS_CLIENT_ID: ${{ secrets.PROD_SP_CLIENT_ID }}
          DATABRICKS_CLIENT_SECRET: ${{ secrets.PROD_SP_SECRET }}
        run: databricks bundle deploy -t prod
```

Notes:

- `databricks/setup-cli@main` is Databricks' official action to install the CLI.
- `environment: prod` with **required reviewers** (GitHub repo → Settings →
  Environments) gives you a manual approval gate before prod deploys — the
  equivalent of GitLab's `when: manual` + protected environment.
- Prod deploys trigger on **tags**, so production always runs a released,
  reviewed commit (Module 07).

## GitLab CI equivalent

`.gitlab-ci.yml`:

```yaml
stages: [test, validate, deploy]

default:
  image: python:3.11
  before_script:
    - pip install -r requirements-dev.txt
    - pip install databricks-sdk        # or install the CLI:
    - curl -fsSL https://raw.githubusercontent.com/databricks/setup-cli/main/install.sh | sh

test:
  stage: test
  script: [pytest tests/]

validate:
  stage: validate
  script: [databricks bundle validate -t staging]
  variables:
    DATABRICKS_HOST: $STAGING_HOST
    DATABRICKS_CLIENT_ID: $STAGING_SP_CLIENT_ID
    DATABRICKS_CLIENT_SECRET: $STAGING_SP_SECRET
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-staging:
  stage: deploy
  script:
    - databricks bundle deploy -t staging
    - databricks bundle run integration_smoke -t staging
  variables: { DATABRICKS_HOST: $STAGING_HOST, DATABRICKS_CLIENT_ID: $STAGING_SP_CLIENT_ID, DATABRICKS_CLIENT_SECRET: $STAGING_SP_SECRET }
  environment: { name: staging }
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-prod:
  stage: deploy
  script: [databricks bundle deploy -t prod]
  variables: { DATABRICKS_HOST: $PROD_HOST, DATABRICKS_CLIENT_ID: $PROD_SP_CLIENT_ID, DATABRICKS_CLIENT_SECRET: $PROD_SP_SECRET }
  environment: { name: production }
  rules:
    - if: $CI_COMMIT_TAG =~ /^v/
      when: manual
```

Store `*_SP_CLIENT_ID` / `*_SP_SECRET` as **masked, protected** CI/CD variables
(GitLab course Module 08); scope prod ones to protected tags.

## Testing notebooks in CI (the strong signal)

Unit tests on `src/` modules are table stakes. To actually exercise the
pipeline:

- On the PR, `databricks bundle deploy -t dev` (a PR-scoped target) then
  `databricks bundle run <job> -t dev` against a **staging catalog with sample
  data**. If the notebook errors, the check fails.
- Keep a dedicated **`integration_smoke`** job in the bundle: runs the real
  notebooks over a tiny fixture dataset and asserts row counts / schema.
- Clean up ephemeral dev deploys with `databricks bundle destroy -t dev` in a
  post-merge or scheduled job.

## Rollback

- **Prod runs from a tag** → roll back by deploying the previous tag:
  re-run the `deploy-prod` job for `v2025.09.0`, or `git checkout v2025.09.0 &&
  databricks bundle deploy -t prod`.
- Jobs with a **Git source** → change the job's ref back (Module 07); a bundle
  redeploy at the old tag does this for you.

## Check yourself

1. What three git events typically drive a Databricks CI pipeline, and what does
   each deploy?
2. Why does CI authenticate as a service principal instead of using your token?
3. How do you get a manual approval gate before a production deploy in GitHub
   Actions? In GitLab CI?
4. What's a stronger PR check than "unit tests pass" for a notebook change?

<details>
<summary>Answers</summary>

1. PR opened/updated → test + `bundle validate` (+ optional dev deploy & smoke);
   merge to `main` → `bundle deploy -t staging`; tag `v*` → `bundle deploy -t
   prod`.
2. So automation doesn't depend on one person's credentials (which expire, get
   revoked, or leave with them) and can be scoped to least privilege per
   environment.
3. GitHub: a job with `environment: prod` that has **required reviewers**
   configured. GitLab: a job with `when: manual` (plus a protected environment
   restricting who can run it).
4. `databricks bundle deploy` + `bundle run` of the actual notebook/job against
   a staging catalog with fixture data on the PR — it executes the notebook, not
   just the extracted library code.

</details>

Next: [Module 10 — Environments, identities & secrets](10-environments-identities-secrets.md)
