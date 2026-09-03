# Module 05 — Merge requests

A **merge request (MR)** is a proposal: "merge this source branch into that
target branch." It bundles the diff, the discussion, the pipeline result, and
the approvals into one page that stays live until the branch merges or the MR
closes.

It is GitLab's equivalent of a GitHub pull request. The mechanics are the same
as the Git course, Module 08 — this module is the GitLab-specific detail.

## Creating an MR

Any of:

- **Push a branch**, then open the link git prints:
  `remote: To create a merge request for my-branch, visit: https://...`
- Project → **Code → Merge requests → New merge request** → pick source and
  target branches.
- From an **issue** → **Create merge request** (makes the branch + MR, linked).
- Web IDE → commit to a new branch → **Create MR**.
- `glab mr create --fill` (uses your commits to fill title/description).

Choose:

- **Source branch**: your feature branch.
- **Target branch**: usually `main` (the project's default). Can be any branch —
  e.g. a release branch.

## Anatomy of the MR page

| Tab / area | What it holds |
| --- | --- |
| **Overview** | Description, discussion threads, activity, the merge widget |
| **Commits** | The commits on the source branch not yet on the target |
| **Pipelines** | Every pipeline run for this MR |
| **Changes** | The diff — comment on any line, start threads, make suggestions |
| Right sidebar | Assignee, **Reviewers**, Labels, Milestone, approval status, linked issues |
| Merge widget (bottom of Overview) | Pipeline status, approvals, merge conflicts, the **Merge** button and its options |

## Writing a good MR

### Description templates

`.gitlab/merge_request_templates/Default.md` in the repo auto-fills the
description box. A useful skeleton:

```markdown
## What
<!-- one or two sentences -->

## Why
Closes #

## How to test
1.

## Screenshots / notes for reviewers
```

Pick a non-default template from the dropdown when creating the MR.

### Linking the issue

Put `Closes #42` (or `Closes group/project#42` across projects) in the
description. Effects:

- The issue is auto-closed when the MR merges into the default branch.
- The issue and MR cross-link and show each other's status.

Other keywords: `Closes`, `Fixes`, `Resolves` (+ plurals). `Related to #42`
links without auto-closing.

### Draft MRs

Prefix the title with `Draft:` (or use `/draft`, or the toggle). A draft **can't
be merged** — it signals "work in progress, look but don't merge yet." Remove
the prefix (**Mark as ready**) when it's done.

## Keeping the MR mergeable

- **Push more commits** to the source branch — the MR updates automatically, the
  pipeline re-runs, existing approvals may reset (a project setting).
- **Target branch moved and now conflicts**: the widget says so. Fix it on your
  branch:
  ```bash
  git switch my-branch
  git fetch
  git merge origin/main      # resolve conflicts (Git course Module 06)
  git push
  ```
  or use the MR's **Resolve conflicts** button for simple cases (edits the files
  in the browser).
- **Rebasing**: the widget may offer a **Rebase** button (if the merge method is
  fast-forward / semi-linear). It runs `git rebase origin/main` on your branch
  server-side. Only use it when you understand your branch's commits aren't
  depended on elsewhere.

## Merge options (set per-project, shown on the button)

| Method (Settings → Merge requests) | Result |
| --- | --- |
| **Merge commit** | Always creates a merge commit. Full history, non-linear. |
| **Merge commit with semi-linear history** | Merge commit, but requires the source to be rebased first (no criss-cross). |
| **Fast-forward merge** | No merge commit; source must be rebased onto target first. Linear history. |

Plus toggles:

- **Squash commits**: combine all source-branch commits into one on merge. The
  MR offers a squash commit message. Great for messy WIP branches; the MR
  description often becomes the squash message.
- **Delete source branch**: tick it (usually default) to auto-clean the branch
  on merge.
- **Merge when pipeline succeeds** / **Auto-merge**: click once; GitLab merges
  automatically the moment the pipeline goes green and approvals are met.

## The merge widget checklist

Before **Merge** activates, GitLab typically requires:

1. ✅ Pipeline passed (if "Pipelines must succeed" is on — Module 07)
2. ✅ All required approvals given (Module 06/07)
3. ✅ All discussion threads resolved (if "All threads must be resolved" is on)
4. ✅ No merge conflicts
5. ✅ Not a Draft
6. ✅ You have permission to merge into the target (Maintainer for protected
   `main`)

## After merging

- The source branch is deleted (if you ticked it).
- Linked issues with `Closes #` close.
- A pipeline runs on the **target** branch (the post-merge state) — this is
  often what deploys.
- Locally: `git switch main && git pull && git branch -d my-branch`.

## `glab` quick reference

```bash
glab mr create --fill --draft          # create from current branch
glab mr list                           # open MRs
glab mr view 17 --web                   # open MR 17 in the browser
glab mr checkout 17                     # check out someone's MR branch locally
glab mr merge 17 --squash --remove-source-branch
```

## Check yourself

1. What are the source and target branches of a typical MR?
2. You prefixed the title with `Draft:`. What can't happen now?
3. Your MR's diff shows a conflict with `main`. Where do you resolve it and how?
4. The project uses "Fast-forward merge." Your branch is 3 commits behind
   `main`. What does GitLab make you do before merging?
5. What does `Closes #88` in the description do?

<details>
<summary>Answers</summary>

1. Source = your feature branch; target = the branch you want it merged into,
   usually `main` (the default branch).
2. It can't be merged. Draft MRs are review-only until marked ready.
3. On your source branch, locally: `git fetch` then `git merge origin/main`,
   resolve the conflict, `git push`. (Or the MR's **Resolve conflicts** button
   for simple ones.)
4. Rebase your branch onto the latest `main` (the **Rebase** button, or
   `git rebase origin/main` locally) so it can fast-forward with no merge
   commit.
5. Links issue 88 to the MR and auto-closes issue 88 when the MR merges into the
   default branch.

</details>

Next: [Module 06 — Code review & merging](06-code-review-and-merging.md)
