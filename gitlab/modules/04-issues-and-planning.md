# Module 04 — Issues & planning

Issues are how a team decides and tracks *what to build*. Everything else (MRs,
pipelines) is about *building it*.

## Issues

An **issue** is one unit of work: a bug, a feature, a task, a question. It lives
in a project and has:

| Field | Purpose |
| --- | --- |
| **Title + description** | What and why. Markdown; supports task lists `- [ ]`, images, code |
| **Assignee(s)** | Who owns it |
| **Labels** | Categorisation and workflow state (see below) |
| **Milestone** | Which release / sprint / time-box it belongs to |
| **Due date** | When it's needed |
| **Weight** | Rough size estimate (a number) |
| **Confidential** flag | Hides it from Guests / non-members |
| **Linked items** | "blocks", "is blocked by", "relates to" other issues/MRs |

Create: **Plan → Issues → New issue**, or press `g i` then `n`, or from an email,
or via `glab issue create`.

### Description templates

Put Markdown files in `.gitlab/issue_templates/` in the repo:

```
.gitlab/issue_templates/Bug.md
.gitlab/issue_templates/Feature.md
```

They appear in a dropdown when creating an issue. A `Bug.md` might prompt for
steps to reproduce, expected vs actual, environment. Keeps reports consistent.

### Comments, threads, and mentions

- Comment to discuss. Start a **thread** on a comment to keep a sub-discussion
  resolvable.
- `@username` notifies a person; `@group/team` notifies a group.
- Reference other items by number: `#42` (issue), `!17` (MR), `` `abc123` ``
  (commit). GitLab auto-links and cross-posts a mention.
- Reference across projects: `group/other-project#42`.

## Labels

Labels are the workhorse of GitLab planning. A label is just a coloured tag, but
teams use them for:

- **Type**: `type::bug`, `type::feature`, `type::chore`
- **Workflow state**: `workflow::triage`, `workflow::ready`, `workflow::in-dev`,
  `workflow::review`
- **Priority**: `priority::high`
- **Team/area**: `area::frontend`, `team::payments`

### Scoped labels (`key::value`)

A label with `::` is **scoped**: an issue can have only one label per scope.
Adding `workflow::in-dev` automatically removes `workflow::ready`. This makes
labels behave like state machines and powers board columns. (Scoped labels are a
Premium feature for *enforcement*, but the `::` naming convention and single-
value board behaviour work on Free.)

### Where labels live

- **Project labels**: `Manage → Labels` in a project.
- **Group labels**: `Manage → Labels` on a group — available to every project in
  it. Prefer group labels so `type::bug` means the same thing everywhere.

## Milestones

A **milestone** groups issues and MRs into a time-box or release: "Sprint 24",
"v2.0". It gives you a burndown chart, a completion percentage, and a single
page listing everything in scope. Project milestones or group milestones (the
latter span all projects in the group).

## Boards (Plan → Issue boards)

A board is a **kanban view of issues**, with columns. Each column is backed by a
label (or by assignee, or milestone). Dragging a card between columns
**changes its labels**.

Typical board:

```
| Open | workflow::ready | workflow::in-dev | workflow::review | Closed |
```

Drag a card from `ready` to `in-dev` → GitLab swaps the scoped label. The board
*is* the label state, visualised. Multiple boards per project/group are allowed
(one per team, one per release).

## Quick actions

Type these as slash-commands in any issue/MR description or comment. They
execute and disappear:

| Action | Effect |
| --- | --- |
| `/assign @me` | Assign to yourself |
| `/label ~"type::bug" ~"area::frontend"` | Add labels |
| `/milestone %"Sprint 24"` | Set milestone |
| `/due 2026-10-01` | Set due date |
| `/estimate 3h` / `/spend 1h` | Time tracking |
| `/close` `/reopen` | Change state |
| `/relate #42` | Link another issue |
| `/assign_reviewer @lee` | (MRs) request review |
| `/draft` | (MRs) mark as draft |

Type `/` in the box to see the full list in context.

## How issues connect to the rest

- From an issue: **Create merge request** → GitLab makes a branch named after
  the issue (`42-fix-login-timeout`) and an MR linked to the issue.
- In an MR description: `Closes #42` → merging the MR **auto-closes** issue 42.
- An issue shows its linked MRs and their pipeline status inline.

## A minimal team setup

1. Group labels: `type::{bug,feature,chore}`, `workflow::{ready,in-dev,review}`.
2. One issue board with columns for the `workflow::` values.
3. A milestone per sprint.
4. `.gitlab/issue_templates/Bug.md` and `Feature.md`.
5. Convention: every MR references an issue with `Closes #`.

## Check yourself

1. What happens to `workflow::ready` when you add `workflow::in-dev` to an
   issue?
2. You want the same `type::bug` label available in all 6 of your team's
   projects. Where do you define it?
3. What does dragging a card between board columns actually change?
4. An MR description contains `Closes #17`. What happens to issue 17 when the MR
   merges?

<details>
<summary>Answers</summary>

1. It's removed automatically — both are in the `workflow::` scope, and an issue
   can hold only one label per scope.
2. As a **group label** on the group that contains all 6 projects.
3. The issue's labels — the column is backed by a label, so moving the card
   swaps the label (removing the old column's label, adding the new one's).
4. Issue 17 is closed automatically, with a note linking the MR that closed it.

</details>

Next: [Module 05 — Merge requests](05-merge-requests.md)
