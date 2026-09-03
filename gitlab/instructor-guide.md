# Instructor Guide — GitLab Training

For whoever runs the session. Assumes participants have done the Git course (or
pass a quick git check — see that course's instructor guide).

## Format and timing

A **one-day workshop (~6–7 hours + breaks)**, or 3 × 2.5-hour sessions. GitLab
has more surface than git; resist the urge to demo every feature — stay on the
**issue → MR → pipeline → merge → deploy** spine.

| Block | Modules | Time | Hands-on |
| --- | --- | --- | --- |
| 1. Orientation | 00 | 25 min | — (discussion: what do they use today?) |
| 2. Getting connected | 01 | 45 min | **Exercise 01** part 1 (SSH key) |
| 3. Projects & the UI | 02, 03 | 45 min | **Exercise 01** parts 2–3 (project + push) |
| *break* | | 15 min | |
| 4. Planning | 04 | 45 min | **Exercise 02** (issues & board) |
| 5. Merge requests | 05 | 45 min | **Exercise 03** part 1 (open the MR) |
| *lunch* | | 45 min | |
| 6. Review & merging | 06 | 40 min | **Exercise 03** parts 2–3 (review, merge) |
| 7. Protecting main | 07 | 35 min | **Exercise 04** (protect + watch it block) |
| *break* | | 15 min | |
| 8. CI/CD fundamentals | 08 | 70 min | **Exercise 05** (first pipeline) |
| 9. Deploying | 09 | 45 min | **Exercise 06** (deploy job + manual gate) |
| 10. Strategy & habits | 10, 11 | 40 min | Discussion + definition-of-done |
| 11. Wrap | — | 15 min | Q&A, cheat sheet, next steps |

If short on time, cut: Module 03's snippets/wiki/pages detail, Module 09's child
pipelines and matrix, Module 10 variations B. **Never cut** Exercise 05 — the
first green pipeline is the moment CI/CD clicks.

## Critical prerequisites — do these before day one

Send participants a setup email a week ahead:

1. **Create a gitlab.com account** and **verify it** (credit card or phone —
   GitLab's anti-crypto-mining check). Unverified accounts **cannot use shared
   runners**, which breaks Exercises 05–06. This is the #1 day-of blocker —
   chase it in advance.
2. Confirm git is installed and configured (`git config --global --list` shows
   name + email).
3. Install a text editor; optional: install `glab`.
4. Have them accept an invite to a **course group** you create (see below).

### Set up a course group

- Create a group, e.g. `gitlab-training-2026-09`.
- Add every participant as **Developer** (so protected-branch behaviour in
  Exercise 04 is real — they hit the wall, then you or a co-instructor with
  Maintainer merges).
- Optionally pre-create group labels (`type::bug`, `type::feature`,
  `workflow::ready/in-dev/review`) so Exercise 02 has something to work with,
  or let them create labels as part of the exercise.
- Decide: **one project per participant** (`<username>-sandbox`), or **pairs
  sharing a project** (better for MR review — they review each other). Pairs is
  recommended if the room is even-numbered and comfortable.

### Runner / compute-minutes budget

Shared-runner minutes on Free are limited per namespace per month. For a class:

- The exercises' pipelines are tiny (seconds each), so the quota is usually
  fine.
- **Safer**: register **one project runner** (a `docker` executor on a laptop or
  a cheap VM) to the course group and tag jobs `tags: [course]` — unlimited, no
  quota, no per-account verification needed. Set this up the day before and
  test it.
- Have the runner's `config.toml` set `privileged = false` unless an exercise
  needs Docker-in-Docker (none here do).

## Teaching notes per module

### 00 — What GitLab is

- Start by asking what they use now (email + shared drive? GitHub? Jenkins?
  nothing?). Map their world onto GitLab's objects.
- The GitHub↔GitLab table lands well if anyone knows GitHub.
- Draw the **issue → MR → pipeline → merge → deploy** loop on the board. Leave
  it up all day; point at where each module fits.
- Don't demo anything yet.

### 01 — Getting connected

- Do SSH **live and projected**, walking the room. Everyone must get
  `ssh -T git@gitlab.com` → "Welcome". This gates every later exercise.
- Windows users: Git Bash, and `pbcopy`/`cat` differ — have the commands ready.
- Explain PAT as the fallback; don't have everyone do both.
- 2FA: recommend it, but note it can complicate the class if someone locks
  themselves out — maybe suggest enabling it *after* the course.

### 02 — Projects, groups & roles

- The **Developer-can't-merge-to-protected-main** point is the one to hammer.
  It's surprising and it's the whole reason Exercise 04 works.
- Show your course group's structure. Show inherited membership.
- Keep visibility/tiers brief.

### 03 — The web UI

- Give a **live projected tour** of a real project — sidebar, repo browser,
  blame, compare, Web IDE (press `.`).
- Demo a single-file edit → commit to new branch → "GitLab suggests an MR".
  This previews Module 05 nicely.
- Snippets/wiki/pages: one sentence each. Don't rabbit-hole.

### 04 — Issues & planning

- Build a board **live** with the class calling out columns.
- Demo scoped labels: add `workflow::in-dev`, watch `workflow::ready` vanish.
- Demo quick actions in a comment — `/assign @me`, `/label`, `/milestone`.
- Show `.gitlab/issue_templates/` if you pre-made one.
- Then Exercise 02.

### 05 — Merge requests

- Demo all the creation paths quickly; have them use "push branch → click the
  link."
- Walk the MR page tab by tab on a real MR.
- `Closes #` — demo the auto-close by merging a throwaway MR.
- Draft prefix — show the greyed merge button.
- Merge methods: explain merge-commit vs squash vs fast-forward with the board
  diagram from the Git course. Set the class projects to **squash** +
  **fast-forward** or just merge-commit — pick one and be consistent.

### 06 — Code review & merging

- **Pair review is the exercise.** A reviews B's MR, B reviews A's.
- Demo `Start a review` → batched comments → `Submit review`.
- Demo a ` ```suggestion ` block and "Apply suggestion" — always gets a
  reaction.
- Approvals: set the course projects to "1 approval, author can't approve" so
  the pair genuinely has to review each other.
- CODEOWNERS: preview only; Module 07 does it properly.
- Merge trains: one sentence, "Premium, you'll see the button, ignore for now."

### 07 — Protecting the default branch

- This is a **settings-clicking** module. Project → Settings → Repository →
  Protected branches, and Settings → Merge requests.
- Exercise 04: each participant sets "Allowed to push and merge = No one", then
  tries `git push origin main` and **watches it get rejected**. The rejection
  message is the lesson.
- Then they see their MR from Exercise 03 now *requires* the approval and green
  pipeline before the (Maintainer) merge.
- CODEOWNERS: have them add one line and see the auto-assigned reviewer on a new
  MR.
- Be clear about Free vs Premium: one approval rule, no enforced code-owner
  approval on Free.

### 08 — CI/CD fundamentals

- **The centrepiece.** Budget the most time and the most patience.
- Start from the 6-line example. Push it. Watch it run projected. Then grow it.
- Vocabulary first (pipeline/stage/job/runner/artifact/cache) — draw the
  stages-and-jobs diagram.
- **Artifacts vs cache** confuses everyone. Do the table, then a concrete
  demo: a `build` job produces `dist/`, a `deploy` job consumes it via
  artifacts; delete the artifact line and watch `deploy` break.
- CI/CD variables: add a masked variable, echo it in a job, show it's masked in
  the log.
- `rules:` — do `if: $CI_COMMIT_BRANCH == "main"` and show the job appearing
  only on `main` pipelines.
- Exercise 05: they write a 3-stage pipeline, **deliberately break the test
  job**, read the red log, fix it, watch it go green. The break-and-fix is the
  point.
- Use the **Pipeline editor** (Build → Pipeline editor) — validation + viz
  saves a lot of "why is my YAML wrong."

### 09 — Deploying

- `environment:` — deploy job writes to a fake "environment" (just an
  `echo`/script). Show **Deploy → Environments** populating with history.
- `when: manual` — the ▶ button. Everyone clicks their own deploy.
- Protected environments — restrict who can click; demo with a co-instructor.
- `needs:` — show a pipeline before/after; point at the time saved.
- `include:`/`extends:` — show shrinking a repetitive file. Keep it short.
- Review apps, child pipelines, matrix, releases, Pages: **mention, don't
  drill.** Point at the module for self-study.
- Exercise 06.

### 10 — GitLab Flow

- Discussion-led. Draw the core-rule diagram. Ask the room which variation fits
  *their* actual product.
- The anti-patterns section usually sparks "oh, we do that" — good.
- Emphasise: start with just `main` + feature branches; add branches only for a
  concrete need.

### 11 — Good habits

- Discussion. Show a real (sanitised) messy MR vs a clean one.
- Secrets: reinforce "never in the YAML," masked + protected variables.
- End on the **definition of done** checklist — have the class adapt it to their
  team out loud.

## Common participant problems and fixes

| Symptom | Cause / fix |
| --- | --- |
| `git@gitlab.com: Permission denied (publickey)` | Key not in agent or not added to GitLab. `ssh-add -l`; re-add. |
| Push asks for username/password after SSH setup | They cloned the HTTPS URL. `git remote set-url origin git@gitlab.com:...` |
| `HTTP Basic: Access denied` | Typed password not token, or token expired / missing `write_repository`. |
| Pipeline jobs stay "pending" forever | Shared runners not enabled (account unverified), or job `tags:` match no runner. Use the course project runner. |
| "You are not allowed to push code to protected branches" | Working as intended (Module 07). Branch + MR. |
| Merge button greyed out | Walk the widget checklist: pipeline, approvals, threads, Draft, role. |
| MR shows a conflict | Resolve on the source branch: `git fetch && git merge origin/main`, push. |
| `.gitlab-ci.yml` "invalid" | Use the Pipeline editor's Validate tab. Usually indentation or a `rules`/`only` mix. |
| Job can't read a CI variable | Variable is **protected** but the branch isn't (feature branches are unprotected). Uncheck protected for the exercise, or test on `main`. |
| Scoped label didn't replace the old one | They're not actually in the same `scope::` — check exact spelling before `::`. |
| `glab` commands fail auth | Token needs `api` scope, not just `write_repository`. |
| Compute minutes exhausted mid-class | Switch the class to the project runner (`tags: [course]`); or have participants use a fresh namespace. |

## Facilitation tips

- **One shared demo project, projected, all day.** Build the loop on it in front
  of them before turning them loose on their own.
- **"Git problem or GitLab problem?"** — make the class say which layer every
  error is in. It's the single most useful diagnostic habit (cheat-sheet has the
  table).
- **Pairs for MR review.** Reviewing a peer's real code beats reviewing a
  contrived diff.
- **Pre-bake the failure.** For Exercise 05, have a known-bad test ready so the
  red pipeline is predictable and you can talk through the log calmly.
- **Screenshots age.** GitLab's UI moves labels around every few releases. Teach
  the *navigation logic* (everything hangs off the project left nav, grouped by
  Manage/Plan/Code/Build/Deploy/Settings), not pixel positions.

## Assessment / "did it land?"

Each participant (or pair), unassisted:

1. Create a project, push a local repo to it.
2. Open an issue, put it on a board, move it a column (label changes).
3. Branch, commit, open an MR that says `Closes #<n>`.
4. Get it reviewed and approved by their partner; a Maintainer merges; the issue
   auto-closes.
5. Add a `.gitlab-ci.yml` with a test job; push a change that breaks it; read
   the log; fix it; watch it pass.
6. Explain out loud the difference between artifacts and cache, and why
   `main` is protected.

If they can do 1–5 and answer 6, the course worked.

## Where to send people next

- GitLab Docs: <https://docs.gitlab.com> — the CI/CD reference and the
  `.gitlab-ci.yml` keyword reference especially.
- `.gitlab-ci.yml` keyword reference:
  <https://docs.gitlab.com/ee/ci/yaml/>
- Predefined variables:
  <https://docs.gitlab.com/ee/ci/variables/predefined_variables.html>
- CI/CD examples & templates: the **Build → Pipeline editor** "Browse
  templates", and `gitlab.com/gitlab-org/gitlab/-/tree/master/lib/gitlab/ci/templates`
- The **Git in Databricks** course in this repo, for anyone working in
  notebooks.
