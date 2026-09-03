# Module 07 — Protecting the default branch

By default, any Developer can `git push` straight to `main`. On a team that's a
recipe for broken builds and un-reviewed code. **Protected branches** and
**approval rules** close that gap — they're what make the Module 05/06 workflow
actually mandatory instead of merely encouraged.

## Protected branches

Project → **Settings → Repository → Protected branches**.

`main` is protected automatically when a project is created, with these
defaults:

| Setting | Default | Means |
| --- | --- | --- |
| **Allowed to merge** | Maintainers | Only Maintainers can merge an MR into `main` |
| **Allowed to push and merge** | No one / Maintainers | Direct `git push main` is blocked (or Maintainers only) |
| **Allowed to force push** | Off | `git push --force` to `main` is rejected for everyone |

Tighten it for a team:

- **Allowed to push and merge → No one.** Now *nobody* can `git push` to `main`
  directly — every change must come through an MR. (Maintainers can still merge
  MRs via **Allowed to merge**.)
- **Allowed to merge → Developers + Maintainers** if you want devs to merge
  their own reviewed MRs; leave at Maintainers if you want a gate.

You can protect other branches too, or use a wildcard: protect `release/*` so
release branches get the same treatment.

### What a blocked push looks like

```
$ git push origin main
remote: GitLab: You are not allowed to push code to protected branches on this project.
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs
```

The fix is always: branch, push the branch, open an MR.

## "Pipelines must succeed"

Project → **Settings → Merge requests** → **Pipelines must succeed**.

With this on, the **Merge** button is disabled until the MR's latest pipeline
passes. Combined with a protected `main`, this guarantees nothing merges to
`main` with a red build.

Related toggle: **Skip pipeline validation when there is no pipeline** — decide
whether an MR with *no* `.gitlab-ci.yml` at all can merge (usually yes).

## Approval rules

Project → **Settings → Merge requests → Approval rules**.

| Control | Effect |
| --- | --- |
| **Approvals required** | N approvals needed before merge (set to 1+ for a team) |
| **Eligible approvers** | Which users/groups can give a counting approval |
| **Prevent approval by author** | On by default — no self-approval |
| **Prevent approvals by users who add commits** | Anyone who pushed can't approve |
| **Prevent editing approval rules in MRs** | Stops authors loosening the rule on their own MR |
| **Remove all approvals when commits are added** | Force re-review after changes |

On **Free**: one rule, a required count, and the author/committer restrictions.
Premium adds multiple named rules ("2 from backend, 1 from security"), optional
vs required rules, and enforced Code Owner approval.

## CODEOWNERS

A `CODEOWNERS` file maps paths to the people responsible for them. Location:
repo root, `.gitlab/`, or `docs/`.

```
# Syntax: <path pattern>   <owner> [<owner> ...]
# Owners are @users, @groups, or emails of members.

*                       @team-leads
*.md                    @docs-team
/frontend/              @frontend-team
/frontend/checkout/     @frontend-team @payments-team
/db/migrations/         @dba
/.gitlab-ci.yml         @platform-team
/infra/                 @platform-team

[Documentation]         # optional named section
docs/                   @docs-team
```

- Last matching pattern wins (like `.gitignore`).
- When an MR changes matching files, the owners are **added as reviewers
  automatically**.
- To make their approval **required**, turn on **Require approval from code
  owners** on the protected branch (this specific enforcement is **Premium**;
  on Free, CODEOWNERS still auto-assigns reviewers, just doesn't hard-block).

Sections in `[brackets]` group rules; `[Name][2]` requires 2 approvals from that
section (Premium).

## Push rules (Premium, awareness)

Project → **Settings → Repository → Push rules**. Regex-enforce commit message
format, block committed secrets/large files, require commits be signed, require
the committer match the GitLab user. Handy but Premium — mentioned so you know
the feature exists.

## A recommended Free-tier team baseline

For `main`:

1. **Protected branch**: Allowed to push and merge = **No one**; Allowed to
   merge = **Maintainers** (or Developers + Maintainers).
2. **Pipelines must succeed** = on.
3. **All threads must be resolved** = on.
4. **Approvals required** = **1** (or 2), author can't approve, committers
   can't approve.
5. **Remove approvals when commits added** = on.
6. A `CODEOWNERS` file for the sensitive paths (auto-assigns the right
   reviewers).
7. **Delete source branch** default = on.

Now the only path to `main` is: branch → MR → green pipeline → review + approval
→ Maintainer merges. Exactly the Module 00 loop, enforced.

## Check yourself

1. With `main` protected and "Allowed to push and merge = No one", what happens
   when a Maintainer runs `git push origin main`?
2. What does "Pipelines must succeed" actually block?
3. On GitLab Free, does adding someone to `CODEOWNERS` force them to approve
   before merge?
4. Why turn on "Prevent approval by author"?
5. A Developer's MR is approved and green but Merge is greyed out. Most likely
   cause?

<details>
<summary>Answers</summary>

1. It's rejected — "not allowed to push code to protected branches." Even
   Maintainers must go through an MR when push is set to "No one". (They *can*
   still click Merge on an MR.)
2. The **Merge** button on an MR — it stays disabled until that MR's latest
   pipeline passes.
3. No. On Free it auto-assigns them as reviewers but doesn't hard-require their
   approval. Enforced code-owner approval is Premium.
4. So no one can rubber-stamp their own work; at least one other person must
   review.
5. `main`'s protected-branch rule only lets **Maintainers** merge; the Developer
   needs a Maintainer to merge, or the rule changed to allow Developers.

</details>

Next: [Module 08 — CI/CD fundamentals](08-cicd-fundamentals.md)
