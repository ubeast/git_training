# Instructor Guide — Git in Databricks Training

For whoever runs the session. Assumes participants finished the Git course (or
pass a quick git check — see that course's instructor guide). The GitLab course
helps for Modules 08–09 but isn't required.

## Format and timing

A **one-day workshop (~6 hours + breaks)**, or 3 × 2.5-hour sessions. The course
splits cleanly:

- **Modules 00–06** — using git for notebooks day to day. Everyone needs this.
- **Modules 07–11** — jobs from Git and CI/CD. More relevant to data engineers /
  platform folks than to analysts. If your room is mostly analysts, spend the
  afternoon on 00–06 depth + a demo of 07–09, and make 08–11 self-study.

| Block | Modules | Time | Hands-on |
| --- | --- | --- | --- |
| 1. Orientation | 00 | 25 min | — |
| 2. Connect | 01 | 35 min | **Exercise 01** part 1 (link credentials) |
| 3. Source format | 02 | 35 min | **Exercise 02** (read the committed file) |
| 4. Git folders + the loop | 03, 04 | 55 min | **Exercise 01** parts 2–4 (folder, branch, commit) |
| *break* | | 15 min | |
| 5. Conflicts & recovery | 05 | 40 min | **Exercise 03** (notebook conflict) |
| 6. Collaboration | 06 | 40 min | **Exercise 04** (branch → PR → merge) |
| *lunch* | | 45 min | |
| 7. Jobs from Git | 07 | 40 min | **Exercise 05** (job with Git source) |
| 8. Asset Bundles | 08 | 70 min | **Exercise 06** (`bundle init` → deploy → run) |
| *break* | | 15 min | |
| 9. CI pipelines | 09 | 40 min | Walk the sample workflow file; no live CI |
| 10. Environments & secrets | 10 | 35 min | Discussion + demo a secret scope |
| 11. Habits & wrap | 11 | 30 min | Review checklist; Q&A |

## Critical prerequisites — arrange before day one

This course has more setup than the others. Send a setup email a week ahead and
verify completion.

### Per participant

1. **Databricks workspace access** on a plan with Git folders/Repos (any
   current paid tier; **not** Community Edition). Confirm they can log in and see
   **Workspace ▸ Create ▸ Git folder**.
2. **A git provider account** (GitHub in the examples) and a **PAT** with the
   right scope (Module 01). Have them add it to **Settings ▸ Linked accounts**
   before class if possible.
3. **A cluster they can use** — an all-purpose cluster or serverless, for running
   notebooks in exercises. Pre-create a shared small cluster or a cluster policy
   so this isn't a bottleneck.
4. For Exercise 06 (bundles): the **Databricks CLI v0.205+** installed locally,
   and a **config profile** or auth set up (`databricks auth login --host …`).
   This is the #1 day-of blocker — test it in advance.

### You provide

- **A course repo** on the git provider that everyone can clone. Pre-populate
  it with:
  - `notebooks/` — 2–3 small sample notebooks (source format), one with an
    obvious spot for a conflict (a single-line config cell).
  - `src/` — one tiny module + a `pytest` test.
  - `databricks.yml` + `resources/` — a minimal bundle with one job, `dev` and
    `prod` targets. (Exercise 06 can also `bundle init` from scratch — decide
    which.)
  - A `README` and `.gitignore`.
- **Branch protection on `main`** in the course repo (require PR + 1 approval)
  so Exercise 04 is real.
- Add participants as **collaborators** (write access) so they can push
  branches. For PR review, **pair them** — A reviews B, B reviews A.
- A **shared "answer key" workspace folder** is not needed — the exercise
  READMEs + SOLUTIONs cover it.
- Decide the **catalog story**: a `training` catalog (or `main.training_<user>`
  schemas) participants can write to without stepping on anything.

### If you can, also provide

- **A service principal** with OAuth creds + a linked git credential, so you can
  *demo* a Git-sourced job running as an SP (Module 07) and a bundle deploy as
  M2M (Module 09). Participants don't each need one.

## Teaching notes per module

### 00 — Why version control in Databricks

- Start with the pain: show a workspace notebook's built-in revision history,
  then ask "how do I see a change that spanned 4 notebooks? branch? get someone
  to review before it goes live? promote it to the prod workspace?" — none of it
  works.
- Draw the diagram: provider repo ↔ Git folder (a clone) in the workspace.
- Hammer the mental model: **a Git folder is a normal git clone; the Git dialog
  is a GUI for `git`.** Return to this every time someone's confused.

### 01 — Connecting

- Do it live and projected. Everyone lands on **Settings ▸ Linked accounts**
  with a green/connected state before moving on.
- Fine-grained vs classic PAT: recommend fine-grained scoped to the course repo.
- Distinguish the two layers clearly (admin Git integration vs personal
  credentials) — if someone has *no* Git folder option, it's the admin layer.
- Mention OAuth as the better option where the org has it configured; don't make
  everyone switch mid-class.

### 02 — Notebooks as source

- Open the course repo **in the git provider** and show a notebook's `.py`
  source — the `# Databricks notebook source`, `# COMMAND ----------`,
  `# MAGIC %md` markers. Then open the same notebook in Databricks. "Same file,
  two renderings."
- Show a real PR diff of a notebook change — readable line diff. That's the
  payoff of source format.
- Source vs `.ipynb`: recommend Source for the course and for team repos. Show
  where the setting is.
- **Outputs not committed**: demo it — run a notebook, `display()` a table,
  commit, look at the diff: no output. Explain why that's good (data, size,
  noise).
- Thin-notebook / import-a-module: preview it here, Module 11 drives it home.

### 03 — Git folders

- Create one live from the course repo URL. Show where it lives in the workspace
  tree.
- **Personal vs shared**: the "don't let two people commit from one Git folder"
  rule — explain the shared-working-state failure mode concretely.
- Limits: don't dwell on exact numbers (they change), but land "code and config,
  not data."
- Recovery: "delete and re-create the folder" is cheap — say it now so people
  aren't precious about the clone later.

### 04 — The everyday loop

- Do the whole loop projected in a Git folder: Pull main → Create Branch → edit
  a notebook cell → open the Git dialog → read the diff → Commit & Push → follow
  the "Create pull request" link.
- Show the CLI equivalent beside each step (the mapping table). Keep reinforcing
  "GUI for `git`."
- **No partial staging** — call it out; show committing in stages as the
  workaround.
- Branch switching reloads open notebooks — demo it so it's not a surprise
  later.

### 05 — Conflicts & recovery

- Manufacture a conflict live (two branches edit the same config cell), then
  Pull → conflict. Walk the markers **in the notebook source**.
- Be honest that the in-dialog resolution UX varies — show it, then show the
  provider web editor and the CLI fallback. "Pick whichever gets you a clean
  result; using the CLI is not a failure."
- Emphasise: stray markers break the **cell structure**, not just a line.
- Recovery: `Discard changes` (loses uncommitted only), `revert` for pushed
  commits, notebook revision history as a last resort for lost uncommitted
  edits.
- Exercise 03.

### 06 — Collaboration workflow

- Draw the loop; it's the Git/GitLab course loop with Databricks as the editor.
- **Pairs**: A and B each make a branch + PR in the course repo, review each
  other, merge. Exercise 04.
- Spend real time on **"reviewing notebooks is hard"** — reviewers can't run it,
  outputs aren't there, cluster state isn't in the diff. Then the mitigations:
  thin notebooks + tested modules, bundles pinning the environment, CI executing
  the notebook. This motivates the whole afternoon.

### 07 — Jobs from Git

- Demo: create a job, set **Source: Git**, point at the course repo + `main`,
  task notebook path relative to root. Run it.
- Then change the ref to a **tag** you pre-created. "This is what prod does."
- The **run-as identity / credentials** point: a job running as a departed
  employee breaks. Service principal with its own git credential is the fix.
- Exercise 05.

### 08 — Asset Bundles

- The centrepiece of the afternoon. Budget time and patience.
- Start with the "without a bundle you recreate the job by hand in each
  workspace" pain.
- `databricks bundle init` → `default-python` template → walk the generated
  `databricks.yml` and `resources/`.
- **`mode: development` vs `production`** — the name prefix and paused schedule
  are the concrete tells; demo a dev deploy and show `[dev you] job_name` in the
  workspace with its schedule paused.
- `validate` → `deploy -t dev` → `run` → `summary` → `destroy`. Do the full
  cycle projected.
- Auth: show `~/.databrickscfg` / `databricks auth login`; explain M2M env vars
  are the CI version (Module 09).
- Exercise 06.

### 09 — CI pipelines

- **No live CI** unless you have a lot of time and a working SP — walk the
  sample GitHub Actions file line by line instead, then the GitLab equivalent.
- The three triggers (PR → validate, merge → staging, tag → prod) and
  per-environment service principals are the takeaways.
- Manual approval gate: GitHub environments with required reviewers / GitLab
  `when: manual` + protected environment.
- If time and infra allow: run `databricks bundle validate` in a real Actions
  run on the course repo as a demo.

### 10 — Environments, identities & secrets

- Discussion + one demo: create a secret scope, put a secret, read it in a
  notebook, show it prints `[REDACTED]`.
- "Code identical, config differs" — tie back to bundle targets.
- Service principals: why automation ≠ a person. Least privilege per
  environment.
- The end-to-end diagram: one repo, config per target, identity per env,
  secrets in scopes per env.

### 11 — Habits

- Lead with **thin notebooks, thick modules** — it's the habit that makes
  everything else (testing, review, CI) possible. Show a before/after.
- `.gitignore`, never-commit table, idempotency, pin-prod-to-tags.
- End on the **PR review checklist** — have the room adapt it to their team.

## Common participant problems and fixes

| Symptom | Cause / fix |
| --- | --- |
| No "Git folder" option in the workspace | Admin hasn't enabled Git integration, or Community Edition. Nothing the participant can do — needs an admin. |
| `Authentication failed` creating a Git folder | PAT wrong/expired/mis-scoped, or wrong provider username in Linked accounts. Re-do Module 01. |
| Clone works, Commit & Push fails | Token has read but not write (fine-grained missing "Contents: write"). |
| `Repository URL not allowed` | Admin URL allow-list doesn't include the host. |
| Can't switch branches in the Git dialog | Uncommitted changes. Commit or discard first. |
| Committed a notebook, diff in the PR is huge/unreadable | It's an `.ipynb` (JSON). Switch the repo/notebooks to Source format. |
| Notebook shows outputs in the PR | `.ipynb` with output committing enabled. Strip outputs / switch to Source. |
| Two people edited from one shared Git folder, work lost | Module 03 rule. Each person needs their own Git folder + branch. |
| `databricks: command not found` / old CLI | They have the legacy Python CLI. Install v0.205+ (Go CLI). `databricks version`. |
| `databricks bundle` auth error | No profile / env vars for that target's host. `databricks auth login --host …` or set the M2M env vars. |
| Bundle deploy creates `[dev name]` jobs they didn't expect | That's `mode: development` working as designed. |
| Git-sourced job fails to check out | Job runs as a user without linked git creds (or a departed user). Use a service principal with its own git credential. |
| Job from Git runs stale code | The job points at a workspace path in a Git folder on the wrong branch. Use a Git source pinned to a ref. |

## Facilitation tips

- **One projected course repo + one workspace, all day.** Build the loop in
  front of them before each exercise.
- **"What is this at the git CLI?"** — make the room answer it for every Git
  dialog action. It's the single best debugging habit here.
- **Show the provider side.** Every time you push from Databricks, flip to
  GitHub/GitLab and show the branch, the diff, the PR. Reinforces that
  Databricks is just the editor.
- **Pre-bake the conflict and the tag.** Have the conflicting branch and the
  release tag ready in the course repo so Exercises 03 and 05 are predictable.
- **Screenshots age fast.** Databricks UI shifts (Repos → Git folders, menu
  reshuffles). Teach the navigation logic, not pixels.
- **Analysts vs engineers**: read the room after lunch. If Modules 08–09 are
  over most heads, demo them well and pivot to deeper 00–06 practice + a
  bundle walkthrough rather than forcing everyone through Exercise 06.

## Assessment / "did it land?"

Each participant (or pair), unassisted:

1. Link git credentials; create a Git folder from the course repo.
2. Branch, edit a notebook, Commit & Push; find the branch in the provider.
3. Open the committed `.py` file in the provider; identify the source markers;
   confirm no outputs were committed.
4. Create and resolve a one-cell conflict.
5. Open a PR, get it reviewed by their partner, merge it, Pull `main`.
6. (Engineers) `databricks bundle validate` and `deploy -t dev` the course
   bundle; run its job.
7. Explain: why prod jobs run from a tag; why CI runs as a service principal;
   where a secret belongs.

1–5 + question 7 = the core landed. Add 6 for the engineering track.

## Where to send people next

- Databricks docs — Git folders:
  <https://docs.databricks.com/en/repos/index.html>
- Databricks docs — Asset Bundles:
  <https://docs.databricks.com/en/dev-tools/bundles/index.html>
- Databricks docs — CI/CD with bundles & GitHub Actions:
  <https://docs.databricks.com/en/dev-tools/bundles/ci-cd.html>
- `databricks/setup-cli` GitHub Action:
  <https://github.com/databricks/setup-cli>
- Databricks CLI reference:
  <https://docs.databricks.com/en/dev-tools/cli/index.html>
- This repo's **Git** and **GitLab** courses for the underlying git / CI
  concepts.
