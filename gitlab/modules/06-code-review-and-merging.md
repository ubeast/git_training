# Module 06 — Code review & merging

The MR exists (Module 05). This module is what the *reviewer* does, and how the
MR finally lands.

## Reviewing an MR — the mechanics

Open the MR → **Changes** tab.

- **Comment on a line**: hover the line, click the speech bubble. Write the
  comment.
- **Start a thread** (vs a single comment): threads can be **resolved**, so
  they're right for "please change this." Single comments are fine for "nice" or
  FYI.
- **Multi-line comment**: click-drag the line numbers before commenting.
- **Review batches**: click **Start a review** instead of **Add comment** — your
  comments are held as *pending* until you **Submit review**, so the author gets
  one notification with everything, not ten.
- **Viewed** checkbox per file — track your progress through a big diff.
- **Compare versions** dropdown — if the author pushed changes, diff between
  their pushes to see only what's new.

## Suggestions — propose the exact change

In a comment, use a `suggestion` code block:

````markdown
```suggestion
    timeout = 30  # was 10; CI runners are slow
```
````

GitLab renders it as a diff. The **author clicks "Apply suggestion"** and it
becomes a commit — no local round-trip. Batch multiple suggestions into one
commit with **Add suggestion to batch**.

Great for small, unambiguous fixes. For anything requiring judgement, describe
what you want and let the author implement it.

## Approvals

An **approval** is a reviewer clicking the **Approve** button on the MR. What it
*requires* depends on rules:

| Setting (Settings → Merge requests → Approval rules) | Effect |
| --- | --- |
| **Approvals required: N** | The MR needs N approvals before Merge unlocks |
| **Eligible approvers** | A list of users/groups whose approval counts |
| **Code Owners** as approvers | People named in `CODEOWNERS` for the changed paths must approve (Module 07) |
| **Prevent approval by the author** | You can't approve your own MR (on by default) |
| **Prevent approval by users who added commits** | Anyone who pushed to the branch can't approve it |
| **Reset approvals on new commits** | New push wipes approvals; re-review required |

> On **Free**, you get **one** approval rule and can't strictly *enforce*
> "exactly these people." Premium adds multiple named rules, required code-owner
> approval, and more. This course assumes Free: one rule, N approvals.

**Reviewers vs approvers**: the *Reviewers* field (right sidebar) is a request —
"please look at this." Approval is the action that unlocks merge. A reviewer's
review isn't binding unless they also click Approve and approvals are required.

## `CODEOWNERS` (preview — full detail in Module 07)

A file at `CODEOWNERS`, `.gitlab/CODEOWNERS`, or `docs/CODEOWNERS`:

```
# path            owner(s)
*.js              @frontend-team
/db/migrations/   @dba @alice
/infra/           @platform-team
```

When an MR touches `/infra/`, `@platform-team` is auto-added as a reviewer, and
(if configured) their approval becomes required.

## Merging — who and how

- **Who can click Merge**: for a protected `main` (Module 07), Maintainers by
  default. Developers can be allowed per-branch.
- **The button reflects the project's merge method** (merge commit / squash /
  fast-forward — Module 05).
- **Auto-merge / "Merge when pipeline succeeds"**: click once, walk away; GitLab
  merges when the pipeline is green and approvals are satisfied. Cancels itself
  if the pipeline fails or new commits arrive.

### Merge trains (Premium, awareness)

On busy repos, several MRs waiting to merge can each pass CI alone but break
`main` when combined. A **merge train** queues MRs and runs CI on each *as if
already merged on top of the ones ahead*, merging only if that passes. You'll
see the option on Premium; on Free you just merge one at a time and re-run CI if
`main` moved.

## A reviewer's checklist

- Does it do what the linked issue asked? (Read `Closes #…`.)
- Is the diff scoped to one thing? (Unrelated changes → ask to split.)
- Tests: added/updated for the change? Do they actually test it?
- Names, edge cases, error handling, security-sensitive spots.
- Does CI pass? Don't approve red pipelines "to be fixed later."
- Is the MR description enough for someone in a year to understand *why*?

Approve when you'd be comfortable owning the code. Use threads for blocking
concerns, plain comments for suggestions and praise.

## As the author, responding to review

- Address each thread with a commit **on the same branch**; push. The MR
  updates.
- Reply in the thread, then let the **reviewer** resolve it (they raised it,
  they confirm it's addressed) — or resolve it yourself if the project allows
  and it's clearly done.
- Don't force-push to a branch under active review unless you've agreed to —
  it makes "what changed since I last looked" hard. Regular commits are kinder;
  squash on merge if history matters.
- Re-request review (`/assign_reviewer @lee` or the sidebar "re-request" icon)
  when ready for another pass.

## Check yourself

1. What's the difference between adding a *comment* and adding a *comment that
   starts a thread*?
2. A reviewer left ten inline notes but you only got one notification. What did
   they do?
3. You want a reviewer to make an exact one-line change land as a commit without
   you touching your laptop. What do you both do?
4. Why is "Reset approvals on new commits" often turned on?
5. On GitLab Free, how many approval rules can a project have?

<details>
<summary>Answers</summary>

1. A thread can be **resolved** and the MR can require all threads resolved
   before merge — use threads for "must change this." A plain comment is just a
   remark.
2. They used **Start a review** — comments are batched as pending and sent
   together when they **Submit review**.
3. Reviewer posts a ` ```suggestion ` block with the exact new line; author
   clicks **Apply suggestion**, which commits it to the branch.
4. So a reviewer's approval always reflects the code that will actually merge —
   a later push can't sneak in unreviewed changes under an old approval.
5. One.

</details>

Next: [Module 07 — Protecting the default branch](07-protecting-branches.md)
