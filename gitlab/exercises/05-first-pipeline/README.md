# Exercise 05 — Your first pipeline

**After:** Module 08 · **Time:** ~40 min · Uses `gitlab-lab`.

## Goal

Write a real `.gitlab-ci.yml` with three stages, watch it run, **deliberately
break a job**, read the red log, and fix it. The break-and-fix is the point.

## Prerequisites

- Shared runners enabled (verified account), **or** the course project runner
  (ask the instructor; if so, add `tags: [course]` to every job below).
- The `greet()` code and `tests/test_app.py` from Exercise 03 on `main`.
- `main` is protected (Exercise 04), so all work here goes through an MR.

## Tasks

### 1. Add project scaffolding

On a branch:

```bash
cd ~/gitlab-lab
git switch main && git pull
git switch -c add-ci

# make src a package and add a requirements file
touch src/__init__.py tests/__init__.py
cat > requirements.txt <<'EOF'
pytest==8.3.3
ruff==0.6.9
build==1.2.2
EOF
```

### 2. Write `.gitlab-ci.yml`

Create it at the repo root. Start from
[`examples/gitlab-ci.starter.yml`](examples/gitlab-ci.starter.yml) — copy it in:

```bash
cp exercises/05-first-pipeline/examples/gitlab-ci.starter.yml .gitlab-ci.yml
```

(Adjust the path if you're not running from the training repo — the file's
contents are also printed in `SOLUTION.md`.)

Read every line. Make sure you can say what each `stage`, `script`, `artifacts`,
and `rules` block does.

### 3. Validate before pushing

**Build → Pipeline editor** (you can paste there), or:

```bash
glab ci lint          # if you have glab
```

Fix any YAML errors it reports.

### 4. Push and open the MR

```bash
git add src/__init__.py tests/__init__.py requirements.txt .gitlab-ci.yml
git commit -m "Add CI pipeline: lint, test, build"
git push -u origin add-ci
```

Open the MR. In the merge widget you'll see a **pipeline running**. Click
through to **Build → Pipelines** or the MR's **Pipelines** tab.

### 5. Watch it run

You should see three stages: `lint` → `test` → `build`. Jobs in `lint` and
`test` — click each, read the log. All green? Good.

If `lint` (ruff) fails on the starter code, that's real — fix the style issues
it names, commit, push, watch it re-run. (Common: unused import, missing final
newline.)

### 6. Break the test job on purpose

```bash
# introduce a bug in the code the tests check
```

Edit `src/app.py` — change the greeting so the test fails:

```python
    return f"Hi, {name}!"      # was "Hello, {name}!"
```

```bash
git commit -am "Change greeting wording"
git push
```

### 7. Read the failure

- The MR pipeline re-runs. The `test` job goes **red**.
- Open the `test` job log. Scroll to the failure:
  ```
  FAILED tests/test_app.py::test_greet_normal - AssertionError: assert 'Hi, Sam!' == 'Hello, Sam!'
  ```
- Note: the `build` stage **did not run** — a failed stage stops the ones after
  it.
- Note: the MR's **Merge** button is disabled ("Pipelines must succeed").

### 8. Fix it

Two valid fixes — pick one and justify it:

- Revert the wording change (the test encodes the intended behaviour), **or**
- If "Hi," is genuinely the new intended greeting, update the test to match.

Do the revert:

```bash
git revert HEAD --no-edit     # or just edit "Hello," back
git push
```

Pipeline goes green. `build` runs this time and produces a `dist/` artifact —
find it under the `build` job → **Browse** / **Download** artifacts, or the MR's
artifacts.

### 9. Add a job that only runs on MRs

Add this to `.gitlab-ci.yml`:

```yaml
mr-only-check:
  stage: lint
  script:
    - echo "This runs only for merge request pipelines."
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

Commit, push. Confirm the job appears in the **MR pipeline** but not in a
**branch pipeline** (compare the pipeline on the MR vs the one listed for the
branch push, if both exist — or check after merge that it's absent from the
`main` pipeline).

### 10. Merge

Get the MR approved (partner / instructor) and merged. Watch a **pipeline run on
`main`** after the merge.

```bash
git switch main && git pull
```

## Verify checklist

- [ ] A 3-stage pipeline (`lint`, `test`, `build`) ran and went green
- [ ] You broke the `test` job and read the actual assertion failure in the log
- [ ] You confirmed `build` did **not** run while `test` was failing
- [ ] You confirmed the MR **could not be merged** while the pipeline was red
- [ ] The `build` job produced a downloadable `dist/` artifact
- [ ] `mr-only-check` ran on the MR pipeline but not on the `main` pipeline
- [ ] A pipeline ran on `main` after the merge

## Questions

1. Why didn't the `build` stage run when `test` failed?
2. `test` produces `report.xml` as an artifact with `when: always`. Why
   `always` and not the default?
3. You need `pytest` in the `test` job. It's installed by `pip install -r
   requirements.txt`. Should that go in `script` or `before_script`, and why
   might you cache something?
4. What's the difference between the pipeline on the MR and a pipeline on a
   plain branch push?

<details>
<summary>Answers</summary>

1. Stages run in order and a stage only starts if the previous one fully
   succeeded. `test` failed → `build` was skipped.
2. `when: always` uploads the artifact even when the job fails, so GitLab can
   still parse and display the JUnit test report for a red run — which is
   exactly when you want to see which tests failed.
3. Either works; `before_script` is conventional for setup so `script` reads as
   "the actual work". You'd cache the pip download directory (`.pip-cache/` or
   the wheel cache) keyed on `requirements.txt` so unchanged deps don't
   re-download every pipeline — a speed optimisation, never something a later
   job *depends* on.
4. An MR pipeline has `CI_PIPELINE_SOURCE == "merge_request_event"` and can run
   jobs gated to MRs (and, with merged-results pipelines, tests the merged
   state). A branch-push pipeline has `CI_PIPELINE_SOURCE == "push"` and only
   sees the branch as-is.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
