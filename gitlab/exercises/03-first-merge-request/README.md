# Exercise 03 — Your first merge request

**After:** Modules 05–06 · **Time:** ~35 min · Uses `gitlab-lab` from Exercise
01 and the issues from Exercise 02.

## Goal

Take an issue through a full merge request: branch, commits, MR with `Closes #`,
review, address feedback, merge, watch the issue auto-close.

## Pairing

This exercise is best done **in pairs**. If you have a partner:

- Both of you are members of the **same** project (either share one, or each add
  the other as **Developer** to your `gitlab-lab`).
- You each do Parts 1–2 on your own MR, then **swap** for Part 3 (review each
  other), then Part 4.

Solo? Do it all yourself — you'll "review" your own MR (GitLab lets you comment;
if approvals require a non-author, temporarily set "Approvals required" to 0 for
this exercise, or have the instructor approve).

## Part 1 — branch and commits

Work on the `greet() should handle an empty name` issue (Exercise 02).

### 1. Start from a fresh main

```bash
cd ~/gitlab-lab
git switch main
git pull
```

### 2. Branch from the issue

Two ways — use the first:

- **From the issue page**: open the issue → **Create merge request** dropdown →
  **Create branch** (name it `<issue-number>-greet-empty-name`). Then locally:
  ```bash
  git fetch
  git switch <issue-number>-greet-empty-name
  ```
- Or purely locally: `git switch -c <issue-number>-greet-empty-name`.

### 3. Make the change

Edit `src/app.py` so an empty name raises a clear error:

```python
def greet(name):
    if not name:
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"
```

Add a tiny test file `tests/test_app.py`:

```python
import pytest
from src.app import greet

def test_greet_normal():
    assert greet("Sam") == "Hello, Sam!"

def test_greet_empty_raises():
    with pytest.raises(ValueError):
        greet("")
```

Commit in two logical steps:

```bash
git add src/app.py
git commit -m "Raise ValueError from greet() on empty name"
git add tests/test_app.py
git commit -m "Add tests for greet()"
git push -u origin <issue-number>-greet-empty-name
```

## Part 2 — open the MR

### 4. Create it

Open the link git printed, **or** **Code → Merge requests → New merge request**,
source = your branch, target = `main`.

Fill in:

- **Title**: `Handle empty name in greet()`
- **Description**:
  ```
  ## What
  greet() now raises ValueError for an empty/falsy name instead of returning
  "Hello, !".

  ## Why
  Closes #<issue-number>

  ## How to test
  pytest tests/test_app.py
  ```
- Right sidebar: set **Reviewer** to your partner (or leave blank if solo).
- Tick **Delete source branch when merged** and **Squash commits** (try squash
  this time).
- **Create merge request.**

### 5. Look around the MR

- **Changes** tab — your diff.
- **Commits** tab — your two commits.
- The **merge widget** at the bottom: note what it's waiting on (reviewer
  approval, maybe "no pipeline" since there's no `.gitlab-ci.yml` yet — that's
  fine, Exercise 05 adds one).

### 6. Mark it ready

If you opened it as a Draft, click **Mark as ready**.

## Part 3 — review (swap with your partner)

Open your partner's MR → **Changes**.

### 7. Leave review feedback

- Click **Start a review** (not "Add comment") so your notes batch.
- Add at least:
  - One **thread** on a line asking for a real change. Example: on the
    `raise ValueError` line, suggest also handling `name` that is only
    whitespace.
  - One ` ```suggestion ` block. Example, on the message line:
    ````
    ```suggestion
        raise ValueError("name must be a non-empty string")
    ```
    ````
  - One plain positive comment.
- Click **Submit review**.

### 8. As the author: respond

Back on your own MR:

- **Apply** the suggestion (button in the thread) — it becomes a commit.
- For the whitespace thread: make the change locally, commit, push:
  ```python
      if not name or not name.strip():
          raise ValueError(...)
  ```
  ```bash
  git commit -am "Also reject whitespace-only names"
  git push
  ```
- Reply in each thread describing what you did. Let the **reviewer** resolve the
  threads (they raised them).
- Re-request review (sidebar re-request icon, or `/assign_reviewer @partner`).

### 9. As the reviewer: approve

- Re-check the **Changes** — use the "Compare versions" dropdown to see just the
  new commits.
- Resolve your threads if satisfied.
- Click **Approve**.

## Part 4 — merge

### 10. Merge it

- The widget should now be green: approved, threads resolved, no conflicts.
- Click **Merge** (it'll say "Squash and merge" given your settings).
- Watch:
  - the source branch is deleted,
  - issue `#<issue-number>` **closes automatically** (open it — "closed via
    merge request !N"),
  - `main` now has a single squashed commit for the whole change.

### 11. Sync locally

```bash
git switch main
git pull
git branch -d <issue-number>-greet-empty-name    # local branch cleanup
git log --oneline -3
```

## Verify checklist

- [ ] The MR description contained `Closes #<n>` and the issue auto-closed on
      merge
- [ ] You used **Start a review** → batched comments → **Submit review**
- [ ] At least one ` ```suggestion ` was applied as a commit via the button
- [ ] At least one thread was resolved by the reviewer, not the author
- [ ] The branch merged as a **single squashed commit** on `main`
- [ ] The source branch was deleted automatically
- [ ] `git log` on `main` locally shows the squashed commit

## Questions

1. Why let the reviewer resolve threads rather than the author?
2. What did `Closes #<n>` do, and when exactly did it fire?
3. You pushed two more commits during review but `main` only gained one. Why?

<details>
<summary>Answers</summary>

1. The person who raised the concern confirms it's actually addressed — the
   author saying "done" isn't the same as the reviewer agreeing.
2. It linked the issue to the MR and closed the issue automatically — at the
   moment the MR merged into the default branch (`main`).
3. **Squash commits** was on: all the branch's commits (original two + the
   review fixes) were combined into one commit when merging.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
