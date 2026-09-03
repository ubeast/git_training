# Module 11 — Everyday good habits

The Git course's habits (small commits, clear messages, no secrets, pull before
push) all still apply. These are the Databricks-specific additions.

## Thin notebooks, thick modules

The single highest-value habit.

| Put in a notebook | Put in a `.py` module (`src/`) |
| --- | --- |
| Orchestration: "read this, call that, write there" | Business logic, transformations, parsing, validation |
| `display()` / exploration during development | Anything with edge cases worth a unit test |
| Widget/parameter wiring | Pure functions that take and return DataFrames |
| The 10–20 lines a reviewer needs to understand the flow | The 200 lines they'd have to trace through cells otherwise |

Why:

- Modules get **`pytest` tests** that CI runs (Module 09). Notebook cells
  effectively don't.
- Module diffs review cleanly. A 40-cell notebook diff is a slog.
- Logic in a module is reusable across notebooks and jobs without `%run`
  spaghetti.
- The Git folder root is on `sys.path`, so `from src.x import y` just works
  (Module 02).

A good notebook is mostly imports and a short `main()`-like flow.

## One notebook, one job

- A notebook should do **one thing** — a mega-notebook that ingests, transforms,
  trains, and reports is impossible to review, test, or partially re-run, and is
  a conflict magnet.
- Split by stage; wire them together as **tasks in a job** (or a DLT pipeline),
  not as one 60-cell file.

## Don't dual-edit

- Don't edit the same notebook in the **Workspace** copy and in a **Git folder**
  copy — they're different files; you'll lose one set of changes.
- Don't have two people committing from one Git folder (Module 03/06).
- Pick the Git folder as the source of truth and stay there.

## Notebook format and outputs

- **Use Source format** for team repos (Module 02) — cleanest diffs, no output
  leakage.
- If using `.ipynb`, **don't commit outputs** unless there's a specific reason
  and an admin has allowed it — outputs can carry data/PII and bloat history.
- Don't paste query results, sample rows, or `df.show()` dumps into markdown
  cells and commit them — that's data in git.

## `.gitignore` for a Databricks repo

```
# Bundle / CLI local state
.databricks/

# Python
__pycache__/
*.pyc
.venv/
*.egg-info/
dist/
build/

# Local data & scratch — never commit data
data/
*.parquet
*.csv          # allow specific small reference files with  !ref/lookup.csv
*.delta/

# Secrets & local config
.env
*.pem
```

## Never commit

| Don't | Why | Instead |
| --- | --- | --- |
| Access tokens, API keys, connection strings | Permanent in git history *and* notebook revision history | Secret scopes (`dbutils.secrets.get`) — Module 10 |
| Data files, extracts, model binaries | Bloat every clone forever; hit Git folder size limits | Unity Catalog volumes / tables / cloud storage |
| Notebook cell outputs (esp. `.ipynb`) | May contain data; noisy diffs | Screenshot in the PR; write a summary table |
| Absolute workspace paths hardcoded | Break in other environments / users | Relative paths, widgets, bundle variables |
| Catalog / schema / bucket names hardcoded | Wrong in dev vs prod | Job parameters / bundle `${var.catalog}` |
| `.databricks/` bundle state | Machine-specific, causes churn | `.gitignore` it |

If a secret does get committed and pushed: **rotate it now** (in the provider /
the external system), then clean up. History keeps it otherwise.

## Idempotency and re-runs

- Assume every notebook will be re-run: use `CREATE OR REPLACE`, `MERGE`, or
  explicit partition overwrites — not blind `INSERT` that double-counts.
- Don't depend on cluster state from a previous cell run that a fresh job
  cluster won't have.
- Parameterise the date/window; don't hardcode "yesterday" as a literal.

## Pin production

- Production jobs run from a **tag or commit**, never a branch (Module 07).
- CI deploys prod on **tag push**, behind a manual approval (Module 09).
- Rollback = redeploy the previous tag.

## Keep the Git folder current

```
Git dialog → main → Pull            # start of day
Git dialog → Create Branch          # per ticket
... edit, Commit & Push regularly ...
Create pull request → review → merge in the provider
Git dialog → main → Pull            # get your merged work + everyone else's
```

## Review checklist for a Databricks PR

- [ ] Logic that deserves a test is in `src/`, not a notebook cell
- [ ] No hardcoded tokens, catalog names, or absolute paths
- [ ] `dbutils.secrets.get` used for anything sensitive
- [ ] No committed outputs / data / large files
- [ ] Notebook is idempotent (safe to re-run)
- [ ] `databricks.yml` / job changes reviewed (cluster size, schedule,
      parameters, permissions)
- [ ] Description says how it was tested (cluster, data, run link) + screenshots
      of key results
- [ ] Won't unexpectedly break a scheduled job that uses the same notebook

## Check yourself

1. What's the main reason to move logic out of notebook cells into `.py`
   modules?
2. Give three things that must never be committed to a Databricks repo.
3. Why must production jobs run from a tag rather than `main`?
4. You need a query result visible in code review. What do you do — and not do?

<details>
<summary>Answers</summary>

1. Modules can be unit-tested by CI and review cleanly; notebook cells
   effectively can't, and big notebook diffs are unreviewable.
2. Any three: secrets/tokens, data files or extracts, model binaries, notebook
   cell outputs, hardcoded environment config (catalogs/paths), `.databricks/`
   local state.
3. `main` moves; a tag is fixed. Prod-from-a-tag runs exactly the reviewed,
   released commit, makes "what's in prod" unambiguous, and makes rollback a
   one-line ref change.
4. Put a screenshot in the PR description, or write a small summary table
   somewhere the reviewer can query. Do **not** commit the notebook with its
   outputs or paste result rows into a markdown cell — that's data in git.

</details>

---

That's the course. Keep [the cheat sheet](../cheat-sheet.md) handy for the Git
dialog mapping, notebook format markers, and `databricks bundle` commands.

You've now done all three courses: **Git** → **GitLab** → **Git in Databricks**.
