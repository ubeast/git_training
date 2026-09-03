# Exercise 06 — A deploy job

**After:** Module 09 · **Time:** ~30 min · Uses `gitlab-lab` with the pipeline
from Exercise 05.

## Goal

Add a `deploy` stage with a tracked **environment**, a **manual gate** for
production, and use **`needs:`** to speed the pipeline up. No real
infrastructure — the "deploy" is a script that prints and writes a file.

## Tasks

### 1. A fake deploy script

On a branch:

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

### 2. Add deploy jobs to `.gitlab-ci.yml`

Add a `deploy` stage and two jobs. Use
[`examples/deploy-jobs.yml`](examples/deploy-jobs.yml) as the reference and
merge its contents into your `.gitlab-ci.yml`:

```yaml
stages:
  - lint
  - test
  - build
  - deploy          # <-- add

deploy-staging:
  stage: deploy
  needs: [build]
  script:
    - ./deploy.sh staging
  environment:
    name: staging
    url: https://staging.example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy-production:
  stage: deploy
  needs: [deploy-staging]
  script:
    - ./deploy.sh production
  environment:
    name: production
    url: https://example.com
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
  allow_failure: false
```

Key points to notice:

- Both deploy jobs run **only on `main`** (`rules`) — never on feature branches
  or MRs.
- `deploy-production` is `when: manual` — it appears but waits for a click.
- `needs:` makes `deploy-staging` start as soon as `build` is done, and
  `deploy-production` depend specifically on `deploy-staging`.

### 3. Validate, push, open MR

```bash
glab ci lint
git add deploy.sh .gitlab-ci.yml
git commit -m "Add staging + manual production deploy jobs"
git push -u origin add-deploy
```

On the MR pipeline: `lint`, `test`, `build` run — but **no deploy jobs**,
because the `rules` require `main` and this is an MR/branch. Good — you don't
deploy from a feature branch.

### 4. Merge, then watch the `main` pipeline

Get it approved and merged. Then **Build → Pipelines** → the new `main`
pipeline:

- `lint` → `test` → `build` → `deploy-staging` runs automatically.
- `deploy-production` shows as a **manual** job with a ▶ button — **blocked**,
  waiting for you.

### 5. Check the environment

**Deploy → Environments**:

- `staging` appears, with a deployment entry: commit SHA, "deployed just now",
  and a **View deployment** link (to the fake `url`).
- `production` does **not** exist yet — its job hasn't run.

### 6. Run the production deploy

- On the `main` pipeline, click ▶ on `deploy-production`.
- It runs `./deploy.sh production`.
- **Deploy → Environments** now also shows `production`.

### 7. Protect the production environment

**Settings → CI/CD → Protected environments** → **Protect an environment**:

- Environment: `production`
- **Allowed to deploy**: Maintainers (remove Developers)

Now a Developer sees the ▶ on `deploy-production` but clicking it is denied —
only Maintainers can trigger the production deploy. (Demo with a partner if you
have one.)

### 8. See a rollback

- Make a trivial change on a new branch (edit `README.md`), MR, merge.
- New `main` pipeline runs; `deploy-staging` deploys the new commit.
- **Deploy → Environments → staging → Deployment history** now has two entries.
- On the older entry, use the **Re-deploy** (rollback) button — it re-runs
  `deploy-staging` pinned to that older commit. Watch it run.

### 9. (Optional) Speed check with `needs:`

Look at the pipeline graph. Without `needs:`, `deploy-staging` would wait for the
entire `build` stage. With `needs: [build]` it starts the instant the single
`build` job finishes. On this tiny pipeline the saving is small; on a real one
with many parallel build/test jobs it's large. Try temporarily removing the
`needs:` lines and compare the pipeline's shape in the editor's visualisation.

## Verify checklist

- [ ] Deploy jobs run **only** on `main`, never on the MR/branch pipeline
- [ ] `deploy-staging` runs automatically after `build` on `main`
- [ ] `deploy-production` is a **manual** job that waited for your click
- [ ] **Deploy → Environments** shows `staging` and (after step 6) `production`
      with deployment history
- [ ] After protecting `production`, only Maintainers can run its deploy job
- [ ] You performed a re-deploy/rollback of `staging` to an earlier commit
- [ ] You can explain what `needs:` changed about the pipeline

## Questions

1. Why gate the deploy jobs with `rules: if: $CI_COMMIT_BRANCH ==
   $CI_DEFAULT_BRANCH`?
2. What does `environment: name: production` give you that a bare
   `./deploy.sh production` script wouldn't?
3. `when: manual` makes a button appear. What *else* do you need so that not
   everyone can click it?
4. Your `deploy-production` job is `needs: [deploy-staging]`. What happens to
   `deploy-production` if `deploy-staging` fails?

<details>
<summary>Answers</summary>

1. So deployments only ever happen from the reviewed, protected default branch —
   never from an unreviewed feature branch or an MR pipeline.
2. GitLab tracks it: a deployment history per environment (which commit, who,
   when, what's current), a clickable environment URL, and re-deploy / rollback
   buttons on the Environments page.
3. A **protected environment** (Settings → CI/CD → Protected environments)
   restricting "Allowed to deploy" to specific roles/users.
4. It won't run — `needs:` makes it depend on `deploy-staging` succeeding. A
   failed dependency means the dependent job is skipped, and the pipeline is
   marked failed.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
