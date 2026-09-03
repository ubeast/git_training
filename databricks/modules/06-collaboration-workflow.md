# Module 06 — A collaboration workflow

Putting Modules 01–05 together into the routine a Databricks team actually
follows.

## The shape

It's the feature-branch workflow from the Git course (Module 08) and GitLab
course (Module 08), with Databricks as the editor:

```
issue / ticket
   │
   ▼
personal Git folder, on a new branch     ← you edit notebooks here
   │  Commit & Push (Git dialog)
   ▼
branch on the provider  →  Pull Request  →  review  →  CI checks  →  merge
   │
   ▼
main  ──────────────────────────────────────►   (protected; PR-only)
   │
   ├─►  a shared/prod Git folder or a Git-sourced job runs from main or a tag
   └─►  CI/CD (Asset Bundles) deploys main to staging, tags to prod  (Modules 08–09)
```

## Roles: personal vs shared Git folders

| Git folder | Branch | Who writes | Purpose |
| --- | --- | --- | --- |
| `Users/alice@…/pipelines` | Alice's feature branches | Alice only | Alice's dev work |
| `Users/bob@…/pipelines` | Bob's feature branches | Bob only | Bob's dev work |
| `Shared/pipelines-main` (optional) | `main`, read-only | automation / admin | A stable clone to read or run interactively against "what's on main" |
| (production) | a **tag** | nobody edits | Jobs run from Git at a pinned tag — no folder to edit |

**Never** develop by having several people commit from one shared Git folder.
The shared working copy has one branch and one uncommitted state; you'll
overwrite each other. Isolation comes from **each person's own Git folder + their
own branch**.

## The loop, step by step

### 1. Sync and branch

Git dialog → `main` → **Pull** → **Create Branch** `123-fix-null-handling`.

### 2. Work in small pieces

Edit notebooks / modules. Keep the change focused on the one ticket. Commit &
Push regularly — it's your backup and it makes the eventual diff reviewable.

### 3. Keep current

If `main` moves, merge it into your branch (Module 04 step 5) and resolve
conflicts now, on your branch — not at PR time.

### 4. Open the PR

Use the **Create pull request** link after a push. Write a real description:

- **What** changed and **why** (link the ticket: `Closes #123`).
- **How it was tested** — which cluster, which notebook run, what you checked.
  This matters more for notebooks than for library code because reviewers often
  can't just "run the tests."
- **Screenshots** of key outputs if a result is the point of the change
  (outputs aren't in the diff).

### 5. Review

Reviewers read the **source diff** of the notebooks in the provider. Good
notebook review looks at:

- Is logic creeping into notebooks that should be in a tested module?
- Any hardcoded paths, table names, tokens, or `dbutils.secrets` misuse?
- Cluster/library assumptions — will this run on the job cluster, not just the
  author's all-purpose cluster?
- Idempotency — safe to re-run? Overwrites vs appends?
- Does it touch a notebook a scheduled job runs? (Blast radius.)

CI can run linting and unit tests on the `src/` modules automatically
(Module 09).

### 6. Merge

In the provider, once approved and green. Protect `main` so this is the only
path (GitLab course Module 07; GitHub branch protection is equivalent):

- Require a PR, require ≥1 approval, require status checks (CI) to pass.
- No direct pushes to `main`.

### 7. Propagate

After merge:

- Everyone's next `main` **Pull** in their Git folder gets the change.
- A shared/prod Git folder is updated (by automation or admin) — or better, the
  job runs from Git and just needs its ref bumped (Module 07).
- CI deploys (Modules 08–09).

## Notebooks and code review — the honest bit

Reviewing notebooks is harder than reviewing library code:

- Reviewers often **can't run it** without the right cluster, data, and
  permissions.
- A "passing" notebook depends on cluster state, installed libraries, and
  catalog contents that aren't in the diff.
- Outputs (the actual results) aren't committed.

Mitigations, all covered elsewhere in this course:

- **Thin notebooks, thick modules** (Module 11) — the reviewable logic lives in
  `.py` files with `pytest` tests that CI runs.
- **Asset Bundles** (Module 08) pin the cluster, libraries, and parameters in
  `databricks.yml`, which *is* in the diff.
- **Git-sourced jobs** (Module 07) mean "what runs" is a repo ref, reviewed like
  anything else.
- A **CI job that actually executes** the notebook against a staging catalog on
  the PR (Module 09) — the strongest signal.

## Check yourself

1. Why shouldn't a team develop from one shared Git folder?
2. What belongs in a Databricks PR description that a normal code PR might not
   need?
3. Name two reasons reviewing a notebook diff is weaker than reviewing a library
   PR, and one way this course reduces that.
4. After a PR merges, how does a colleague's Git folder get the change?

<details>
<summary>Answers</summary>

1. It has a single shared branch and a single uncommitted working state — two
   people committing from it overwrite each other's work. Isolation must come
   from separate Git folders and separate branches.
2. How it was tested (cluster, data, notebook run, what was checked) and
   screenshots of key outputs — because outputs aren't in the diff and reviewers
   often can't re-run it.
3. Reviewers usually can't run it (needs the right cluster/data/permissions);
   "passing" depends on un-diffed cluster and catalog state; results aren't
   committed. Mitigation: put real logic in tested `.py` modules, pin
   environment in an Asset Bundle, or have CI execute the notebook against a
   staging catalog.
4. Their next **Pull** of `main` in the Git dialog brings it in.

</details>

Next: [Module 07 — Running jobs from Git](07-jobs-from-git.md)
