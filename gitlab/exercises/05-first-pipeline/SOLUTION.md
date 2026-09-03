# Exercise 05 — Solution

## 1–2. Scaffolding + CI file

```bash
cd ~/gitlab-lab
git switch main && git pull
git switch -c add-ci

touch src/__init__.py tests/__init__.py
cat > requirements.txt <<'EOF'
pytest==8.3.3
ruff==0.6.9
build==1.2.2
EOF
```

`.gitlab-ci.yml` (same as
[`examples/gitlab-ci.starter.yml`](examples/gitlab-ci.starter.yml)):

```yaml
stages: [lint, test, build]

default:
  image: python:3.12
  cache:
    key:
      files: [requirements.txt]
    paths: [.cache/pip]
  before_script:
    - python -m pip install --upgrade pip
    - pip install -r requirements.txt
  variables:
    PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

lint:
  stage: lint
  script: [ruff check .]

test:
  stage: test
  script: [pytest --junitxml=report.xml]
  artifacts:
    when: always
    reports: { junit: report.xml }
    paths: [report.xml]
    expire_in: 1 week

build:
  stage: build
  script: [python -m build]
  artifacts:
    paths: [dist/]
    expire_in: 1 week
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
```

> `build` also needs a minimal `pyproject.toml` for `python -m build` to work.
> Add one:
> ```toml
> [project]
> name = "gitlab-lab"
> version = "0.1.0"
>
> [build-system]
> requires = ["setuptools"]
> build-backend = "setuptools.build_meta"
> ```
> (If you skip this, `build` fails with "no pyproject.toml" — a fine extra
> break-and-fix.)

## 3–4. Validate and push

```bash
glab ci lint                     # or paste into Build → Pipeline editor → Validate
git add -A
git commit -m "Add CI pipeline: lint, test, build"
git push -u origin add-ci
```

## 5. First run

MR pipeline shows `lint` → `test` → `build`.

If `ruff` flags the starter code (e.g. `tests/test_app.py` imports `pytest` but
the earlier version didn't use it, or a missing newline): fix exactly what it
names, commit, push. Typical:

```
tests/test_app.py:1:8: F401 [*] `pytest` imported but unused
```

— but our test *does* use `pytest.raises`, so more likely it's clean. A missing
trailing newline is the usual first offender; `ruff check --fix .` locally sorts
most of it.

## 6–7. Break it

`src/app.py`:

```python
    return f"Hi, {name}!"
```

```bash
git commit -am "Change greeting wording"
git push
```

`test` job log:

```
=================================== FAILURES ===================================
______________________________ test_greet_normal _______________________________

    def test_greet_normal():
>       assert greet("Sam") == "Hello, Sam!"
E       AssertionError: assert 'Hi, Sam!' == 'Hello, Sam!'
E         - Hello, Sam!
E         + Hi, Sam!

tests/test_app.py:5: AssertionError
=========================== short test summary info ============================
FAILED tests/test_app.py::test_greet_normal - AssertionError: assert 'Hi, Sam...
```

Pipeline overview: `lint` ✅ · `test` ✗ · `build` ⊘ (skipped). MR **Merge**
button disabled.

## 8. Fix

```bash
git revert HEAD --no-edit
git push
```

Green. `build` now runs and uploads `dist/gitlab_lab-0.1.0-*.whl` +
`.tar.gz`. Find it: `build` job → right panel → **Browse** / **Download**.

## 9. MR-only job

```yaml
mr-only-check:
  stage: lint
  script:
    - echo "This runs only for merge request pipelines."
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

```bash
git commit -am "Add MR-only check job"
git push
```

- On the **MR pipeline**: `mr-only-check` is present.
- After merge, on the **`main` pipeline**: it's absent (source is `push`, not
  `merge_request_event`).

## 10. Merge

Approved + green → merge. A pipeline runs on `main`
(`CI_PIPELINE_SOURCE == "push"`, `CI_COMMIT_BRANCH == "main"`), running `lint`,
`test`, and `build` (build's second rule matches the default branch), but not
`mr-only-check`.

## Key takeaways

- One file, `.gitlab-ci.yml`, at the repo root drives everything.
- Stages are sequential gates: a red stage stops all later stages.
- "Pipelines must succeed" (Exercise 04) + a red pipeline = un-mergeable MR.
  That's the safety net working.
- `artifacts:` keep outputs (`dist/`, `report.xml`); `when: always` keeps the
  test report even on failure so you can see *which* tests broke.
- `rules: if: $CI_PIPELINE_SOURCE == ...` controls which jobs exist in which
  kind of pipeline.
- Validate YAML (`glab ci lint` / Pipeline editor) before pushing — it's much
  faster than push-wait-read-fix loops.
