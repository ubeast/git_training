# Exercise 06 — Solution

## 1. Fake deploy script

```bash
cd ~/gitlab-lab
git switch main && git pull
git switch -c add-deploy

cat > deploy.sh <<'EOF'
#!/usr/bin/env sh
set -e
TARGET="${1:?usage: deploy.sh <target>}"
echo "Deploying commit ${CI_COMMIT_SHORT_SHA} to ${TARGET}..."
sleep 2
echo "Deployed to ${TARGET} at $(date -u +%FT%TZ)"
EOF
chmod +x deploy.sh
```

`chmod +x` matters — git records the executable bit, and the runner needs it to
run `./deploy.sh`.

## 2. `.gitlab-ci.yml` additions

Add `deploy` to `stages:` and append the two jobs from
[`examples/deploy-jobs.yml`](examples/deploy-jobs.yml). Final `stages`:

```yaml
stages: [lint, test, build, deploy]
```

## 3. Push + MR

```bash
glab ci lint
git add deploy.sh .gitlab-ci.yml
git commit -m "Add staging + manual production deploy jobs"
git push -u origin add-deploy
```

**MR pipeline**: `lint`, `test`, `build` only. No deploy jobs — the `rules`
need `$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`, and an MR pipeline's branch
context doesn't match (`CI_COMMIT_BRANCH` is empty for MR pipelines, and for the
branch pipeline it's `add-deploy`, not `main`). This is correct: **you never
deploy from a feature branch.**

## 4. Merge → `main` pipeline

Approved + merged. The `main` pipeline:

```
lint ✅ → test ✅ → build ✅ → deploy-staging ✅   deploy-production ⏸ (manual)
```

`deploy-staging` log:

```
Deploying commit a1b2c3d to staging...
Deployed to staging at 2026-09-03T14:22:10Z
Job succeeded
```

## 5. Environments

**Deploy → Environments**:

| Environment | Last deployment |
| --- | --- |
| `staging` | commit `a1b2c3d`, "just now", **View deployment** → https://staging.example.com |

No `production` row yet.

## 6. Run production

Click ▶ on `deploy-production` in the pipeline. It runs `./deploy.sh
production`. Now **Environments** lists `production` too.

## 7. Protect production

**Settings → CI/CD → Protected environments → Protect an environment**:

- Environment: `production`
- Allowed to deploy: **Maintainers** only

A Developer now sees the ▶ but gets:

```
You do not have permission to run this job.
```

Only Maintainers can trigger `deploy-production`. This is the real production
gate — `when: manual` alone lets *anyone* who can run pipelines click it.

## 8. Rollback

```bash
git switch main && git pull
git switch -c tweak-readme
echo "- deploy demo" >> README.md
git commit -am "Tweak README"
git push -u origin tweak-readme
# MR → approve → merge
git switch main && git pull
```

New `main` pipeline deploys the new commit to `staging`. **Environments →
staging → Deployment history** now has 2+ entries. On an older entry click
**Re-deploy** — GitLab re-runs `deploy-staging` with `CI_COMMIT_SHA` pinned to
that commit. That's a rollback: same job, older code.

## 9. `needs:` shape

- **With `needs:`**: `deploy-staging` starts the moment `build` finishes, not
  waiting for the whole `build` stage (here there's only one build job, so no
  visible difference — but on a real pipeline with parallel builds/tests it
  matters). The pipeline graph shows dependency arrows instead of solid stage
  walls.
- **Without `needs:`**: `deploy-staging` waits for every job in `test` *and*
  `build` stages. Remove the lines in the Pipeline editor and watch the
  visualisation change from a DAG to strict columns.

## Key takeaways

- Deploy jobs are gated to `main` with `rules` — deployments only from the
  reviewed, protected branch.
- `environment:` turns "a script that deploys" into "a deployment GitLab
  tracks" — history, current-version, URL, rollback.
- `when: manual` = a button; **protected environments** = *who* may press it.
  You need both for a real production gate.
- `needs:` builds a dependency graph so jobs start as early as their real
  inputs allow, and `deploy-production` correctly won't run if
  `deploy-staging` fails.
- Rollback = re-running the deploy job pinned to an earlier commit, from the
  Environments page.
