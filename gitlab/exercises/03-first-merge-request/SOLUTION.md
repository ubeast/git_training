# Exercise 03 — Solution

## Part 1 — branch and commits

```bash
cd ~/gitlab-lab
git switch main && git pull
git switch -c 12-greet-empty-name        # use your real issue number
```

`src/app.py`:

```python
def greet(name):
    if not name:
        raise ValueError("name must not be empty")
    return f"Hello, {name}!"
```

`tests/test_app.py`:

```python
import pytest
from src.app import greet

def test_greet_normal():
    assert greet("Sam") == "Hello, Sam!"

def test_greet_empty_raises():
    with pytest.raises(ValueError):
        greet("")
```

```bash
git add src/app.py && git commit -m "Raise ValueError from greet() on empty name"
git add tests/test_app.py && git commit -m "Add tests for greet()"
git push -u origin 12-greet-empty-name
```

Output includes:

```
remote: To create a merge request for 12-greet-empty-name, visit:
remote:   https://gitlab.com/you/gitlab-lab/-/merge_requests/new?merge_request%5Bsource_branch%5D=12-greet-empty-name
```

## Part 2 — the MR

Create via that link. Description:

```markdown
## What
greet() now raises ValueError for an empty/falsy name instead of returning
"Hello, !".

## Why
Closes #12

## How to test
pytest tests/test_app.py
```

Sidebar: Reviewer = partner. Options: **Squash commits** ✓, **Delete source
branch** ✓.

The merge widget will say something like:

```
Ready to merge!
Approval is required.          ← if approvals required ≥ 1
No pipeline for the latest commit    ← fine; no .gitlab-ci.yml yet
```

## Part 3 — review

Reviewer, on **Changes**, clicks **Start a review** and adds:

**Thread (blocking):**
> This handles `""` and `None` but not `"   "`. A whitespace-only name would
> still produce `Hello,    !`. Can we `name.strip()` too?

**Suggestion:**
````markdown
```suggestion
        raise ValueError("name must be a non-empty string")
```
````

**Plain comment:**
> Nice, tests cover both paths.

Then **Submit review** — author gets one notification.

## Part 3 — author responds

- Click **Apply suggestion** on the thread → commit "Apply suggestion..." lands
  on the branch.
- Whitespace fix:

```python
def greet(name):
    if not name or not name.strip():
        raise ValueError("name must be a non-empty string")
    return f"Hello, {name}!"
```

```bash
git pull                       # get the applied-suggestion commit first!
git commit -am "Also reject whitespace-only names"
git push
```

> Note the `git pull` — applying a suggestion in the UI made a commit on the
> branch you don't have locally yet.

- Reply in each thread ("Done in <sha>"), re-request review.

## Part 3 — reviewer approves

- Use **Compare versions** to view only the new commits.
- Resolve both threads.
- **Approve.**

## Part 4 — merge

Widget is green → **Squash and merge**. GitLab asks for a squash commit message
— the MR title/description pre-fills it. Confirm.

Result:

- `main` gains **one** commit: `Handle empty name in greet() (!N)`.
- Branch `12-greet-empty-name` deleted on the server.
- Issue #12 → **Closed**, with "closed via merge request !N".

```bash
git switch main && git pull
git branch -d 12-greet-empty-name
git log --oneline -3
# e9f0a1b Handle empty name in greet() (!7)
# d4e5f6a Note course origin in README
# a1b2c3d Initial project skeleton
```

## Key takeaways

- The whole loop: issue → branch (named for the issue) → commits → MR with
  `Closes #` → pipeline (none yet) → review → approve → merge → issue closes →
  branch deleted.
- **Start a review** batches feedback into one notification.
- **Suggestions** turn a review note into a commit with one click — but you then
  need to `git pull` to get it locally.
- **Squash** collapses a messy branch (original work + review fixes) into one
  clean commit on `main`.
- Threads are resolved by whoever raised them.
