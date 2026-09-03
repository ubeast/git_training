# Module 11 — Everyday good habits on GitLab

The Git course's habits (small commits, good messages, don't commit secrets)
still apply. These are the GitLab-layer additions.

## Merge request hygiene

| Do | Why |
| --- | --- |
| **Keep MRs small** — one issue, ideally < ~400 lines of diff | Big MRs sit unreviewed for days and get rubber-stamped |
| **Open early as a Draft** | Reviewers see direction sooner; CI runs sooner |
| **Fill the description**: what, why (`Closes #`), how to test | The MR is the permanent record of the decision |
| **Respond to every thread** | Unresolved threads block merge (if configured) and signal "not done" |
| **Push fixes as new commits during review** | Reviewers can see "what changed since last look"; squash on merge |
| **Re-request review** when ready for another pass | Reviewers aren't notified automatically that you're done |
| **Delete the source branch on merge** | Keeps the branch list meaningful |
| **Don't merge your own un-reviewed MR** even if you can | The point of the gate is a second pair of eyes |

## Issue hygiene

- **One issue = one deliverable.** If it needs three MRs, it's probably three
  issues (or an epic on Premium).
- **Label on creation** — an unlabelled issue is invisible to the board.
- **Close via the MR** (`Closes #`), not by hand — keeps the link.
- **Use quick actions** (`/assign @me`, `/milestone`, `/label`) instead of the
  sidebar — faster and works from your first comment.
- **Confidential** for security issues until fixed and released.

## Pipeline hygiene

| Do | Why |
| --- | --- |
| **Keep pipelines fast** (< ~10 min for the MR pipeline) | Slow CI = people stop waiting for it and merge on faith |
| Use `needs:` to parallelise; `cache` dependencies; `rules: changes:` to skip irrelevant jobs | All cut wall-clock time |
| **Fail fast** — lint and quick unit tests before slow integration/e2e | Don't wait 20 min to learn about a formatting error |
| **No flaky jobs.** Fix or quarantine them | One flaky job trains everyone to hit "Retry" blindly, hiding real failures |
| **Don't `allow_failure: true` to silence a real problem** | It just hides breakage; fix the job or delete it |
| **Pin image tags and `include: ref:`** | `python:3` or an unpinned template silently changes under you |
| **Keep `.gitlab-ci.yml` reviewed** like code — put it in `CODEOWNERS` | CI config is production infrastructure |

## Secrets — the GitLab way

- **Never** in `.gitlab-ci.yml`, never in the repo, never echoed in a job.
- Use **CI/CD Variables** (Settings → CI/CD → Variables): **masked** so they
  don't print in logs, **protected** so only protected-branch jobs see them.
- Production secrets → **protected** variables + **protected environments**, so a
  feature branch's pipeline can never read them.
- Group-level variables for things shared across projects.
- Rotate a variable the same as any secret; update it in one place.
- For real secret management, integrate a vault (HashiCorp Vault / cloud secret
  manager) via OIDC — no long-lived secrets in GitLab at all. (Beyond this
  course; know it's the mature answer.)
- If a secret leaks into a job log or the repo: **rotate it now**, then clean up.

## Permissions & settings

- Manage access through **groups**, not per-project invites (Module 02).
- Give the **lowest role that works** — most people are Developers, not
  Maintainers.
- Set **membership expiry** for contractors and external collaborators.
- Protect `main` (and `release/*`) from day one, not after the first bad push
  (Module 07).
- Turn off project features you don't use (wiki, snippets, container registry) —
  less surface, less confusion.

## Notifications — tune them or drown

Avatar → **Preferences → Notifications**. Set a sane global level (e.g.
"On mention"), then bump specific projects you own to "Watch". Use **To-Do**
(`g` `t`) as your GitLab inbox — it collects assignments, mentions, review
requests, and failed pipelines you care about.

## Keeping your fork/clone current

Same as the Git course:

```bash
git switch main && git pull          # start of day
git switch -c 51-add-export           # branch per issue
# ... work, small commits ...
git push -u origin 51-add-export
glab mr create --fill                 # or the web link
# review, address threads, get approval
# Maintainer merges; then:
git switch main && git pull
git branch -d 51-add-export
```

## A team's "definition of done"

A change is done when:

- [ ] Its issue is linked (`Closes #`)
- [ ] The MR is small and described
- [ ] The pipeline is green
- [ ] Required approvals are in, from someone other than the author
- [ ] All threads resolved
- [ ] Merged to `main` (by a Maintainer, for protected `main`)
- [ ] Deployed (or queued for the next release) and verified
- [ ] Source branch deleted

## Check yourself

1. Why is a 1,500-line MR a problem even if the code is fine?
2. Where does a deployment API token belong, and which two flags matter?
3. Your MR pipeline takes 35 minutes. Name three ways to bring it down.
4. What's the To-Do list for?
5. A CI job is flaky — passes on retry ~half the time. What's the wrong response
   and what's the right one?

<details>
<summary>Answers</summary>

1. It's too big to review properly — it either blocks for days or gets approved
   without real scrutiny. Split it.
2. A **CI/CD variable**, **masked** (hidden in logs) and **protected** (only
   exposed to protected-branch/tag pipelines). Never in the YAML or repo.
3. Any of: parallelise with `needs:`/`parallel:`, cache dependencies, use
   `rules: changes:` to skip unaffected jobs, run fast checks (lint, unit)
   before slow ones, split e2e into a separate non-blocking pipeline, use a
   bigger/self-hosted runner.
4. It's your GitLab inbox — assignments, mentions, review requests, and pipeline
   failures you need to act on, in one list (`g` then `t`).
5. Wrong: add `allow_failure: true` or train everyone to hit Retry. Right: treat
   it as a bug — fix the underlying nondeterminism, or quarantine the specific
   test into a separate non-blocking job with a ticket to fix it.

</details>

---

That's the GitLab course. Keep [the cheat sheet](../cheat-sheet.md) handy for
`.gitlab-ci.yml` keywords and `glab` commands.

Next course (separate folder): **Git in Databricks**.
