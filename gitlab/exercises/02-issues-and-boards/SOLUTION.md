# Exercise 02 — Solution

This exercise is mostly UI clicking; the solution is the reasoning and the
expected end state.

## 1. Labels

**Manage → Labels → New label**, six times. Naming with `::` is what makes them
scoped — nothing else to configure on Free. Prefer creating them as **group
labels** if a course group exists, so every project shares one definition.

## 2. Milestone

**Plan → Milestones → New milestone** → `Sprint 1` + dates. A milestone with
dates gives you a burndown chart on its page.

## 3. Issues + quick actions

When you type `/label ~"type::bug" ~"workflow::ready"` in the description and
submit, GitLab:

- applies both labels,
- removes the quick-action lines from the saved description,
- adds a system note ("added type::bug workflow::ready labels").

Quick actions also work in the **comment** box after creation, and via `glab`:

```bash
glab issue create --title "greet() should handle an empty name" \
  --label "type::bug,workflow::ready" --milestone "Sprint 1"
```

## 4. Assign

`/assign @me` in a comment → sidebar "Assignee: you". Equivalent to clicking
**Assignee → Edit** in the sidebar.

## 5. Board

**Plan → Issue boards → Create list** for each `workflow::` label. GitLab only
offers labels that exist, which is why step 1 came first.

Issues land in `workflow::ready` because that's the label they carry. An issue
with no `workflow::` label sits only in **Open**.

## 6. Moving cards

Dragging `greet()` bug from `ready` → `in-dev`:

- system note: "removed workflow::ready label / added workflow::in-dev label"
- `type::bug` unchanged — different scope.

Dragging to **Closed** actually closes the issue (state change, not a label).
`/reopen` or dragging back out reopens it.

## 7. Link

`/relate #N` creates a bidirectional "relates to" link, shown under **Linked
items** on both issues. (Premium adds "blocks / is blocked by".)

## 8. Filter

Issue list filter bar: `Milestone := Sprint 1`, `Label := type::feature`, etc.
The board has its own filter bar that narrows every column at once.

## Expected end state

- 6 labels, 1 milestone (`Sprint 1`, 3 issues).
- Board: `Open | workflow::ready | workflow::in-dev | workflow::review | Closed`.
- `greet()` bug: `type::bug` + `workflow::in-dev`, assigned to you.
- `farewell()` feature: `type::feature` + `workflow::in-dev`, in Sprint 1.
- `LICENSE` chore: `type::chore` + `workflow::ready` (reopened after a trip to
  Closed).
- `custom prefix` feature: `type::feature` + `workflow::ready`, Sprint 1, linked
  to the `farewell()` issue.

## Key takeaways

- Scoped labels (`scope::value`) behave like a state machine — one value per
  scope — and that's what powers board columns.
- The board **is** the labels, visualised; dragging cards edits labels.
- Quick actions (`/label`, `/assign`, `/milestone`, `/relate`, `/close`) are the
  fast path and work in descriptions and comments.
- Define shared vocabulary (labels, milestones) at the **group** level.
