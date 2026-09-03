# Exercise 02 — Issues & boards

**After:** Module 04 · **Time:** ~25 min · Uses the `gitlab-lab` project from
Exercise 01.

## Goal

Set up labels, create issues, build a board, and drive issues through it with
quick actions.

## Tasks

### 1. Labels

In `gitlab-lab` → **Manage → Labels → New label**. Create these (any colours):

- `type::bug`
- `type::feature`
- `type::chore`
- `workflow::ready`
- `workflow::in-dev`
- `workflow::review`

> If your course has a **group** with these as group labels already, skip this
> step — they'll be available in the project.

Note the `::` — these are **scoped** labels. An issue can hold only one
`type::` and one `workflow::` at a time.

### 2. A milestone

**Plan → Milestones → New milestone**: title `Sprint 1`, set a start and due
date a couple of weeks apart.

### 3. Create four issues

**Plan → Issues → New issue**. Create:

| Title | In the description, use quick actions |
| --- | --- |
| `greet() should handle an empty name` | `/label ~"type::bug" ~"workflow::ready"` `/milestone %"Sprint 1"` |
| `Add a farewell() function` | `/label ~"type::feature" ~"workflow::ready"` `/milestone %"Sprint 1"` |
| `Add a LICENSE file` | `/label ~"type::chore" ~"workflow::ready"` |
| `Support a custom greeting prefix` | `/label ~"type::feature" ~"workflow::ready"` `/milestone %"Sprint 1"` |

Write a sentence or two of real description for each (what and why).

### 4. Assign one to yourself

Open the `greet()` bug → in a comment, type `/assign @me` and submit. Confirm
the sidebar shows you as assignee.

### 5. Build a board

**Plan → Issue boards**. The default board has "Open" and "Closed". Add columns:

- **Create list** → **workflow::ready**
- **Create list** → **workflow::in-dev**
- **Create list** → **workflow::review**

Board now reads: `Open | workflow::ready | workflow::in-dev | workflow::review | Closed`.

Your four issues should appear in the **workflow::ready** column (that's the
label you gave them).

### 6. Move issues on the board

- Drag the `greet()` bug from **workflow::ready** to **workflow::in-dev**.
- Open the issue. Check its labels: `workflow::ready` should be **gone**,
  `workflow::in-dev` **added**. The `type::bug` label is untouched.
- Drag `Add a farewell() function` to **workflow::in-dev** as well.
- Drag `Add a LICENSE file` all the way to **Closed**. Reopen it (it wasn't
  actually done) by dragging it back to **workflow::ready** or using `/reopen`
  in a comment.

### 7. Link two issues

On `Support a custom greeting prefix`, add a comment: `/relate #<number of the
farewell issue>`. Both issues now show the link under "Linked items".

### 8. Filter

- On the **Issues** list, filter by `Milestone = Sprint 1` — 3 issues.
- Filter by `Label = type::feature` — 2 issues.
- On the **board**, use the search/filter bar to show only `type::feature` —
  columns now show only feature cards.

## Verify checklist

- [ ] Six labels exist (3 `type::`, 3 `workflow::`)
- [ ] `Sprint 1` milestone exists with 3 issues assigned to it
- [ ] The board has ready / in-dev / review columns
- [ ] Moving a card between `workflow::` columns swapped the label (and left
      `type::` alone)
- [ ] The `greet()` bug is assigned to you and sits in **workflow::in-dev**
- [ ] Two issues are linked via `/relate`
- [ ] You can filter the issue list by milestone and by label

## Questions to answer

1. You added `workflow::in-dev` to an issue that had `workflow::ready`. Why did
   `ready` disappear but `type::bug` stay?
2. Where should `type::bug` be defined if you want it identical across five
   projects?
3. What does dragging a card to a different column actually change in the issue?

<details>
<summary>Answers</summary>

1. `workflow::ready` and `workflow::in-dev` are in the same scope
   (`workflow::`), and an issue can hold only one label per scope, so adding one
   removes the other. `type::bug` is a different scope, so it's unaffected.
2. As a **group label** on the group containing the five projects.
3. Its labels — the board column is backed by a label, so the move removes the
   source column's label and adds the destination column's.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
