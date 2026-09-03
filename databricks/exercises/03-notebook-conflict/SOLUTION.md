# Exercise 03 — Solution

## Setup

`config` notebook on `main`, cell 1:

```python
# Databricks notebook source
CATALOG = "training"
SCHEMA = "sandbox"
BATCH_SIZE = 1000
```

## 3–4. Two branches, same line

| Branch | Change | Commit |
| --- | --- | --- |
| `tune-batch-size` (from `main`) | `BATCH_SIZE = 5000` | "Raise batch size to 5000" |
| `lower-batch-size` (from fresh `main`) | `BATCH_SIZE = 250` | "Lower batch size to 250 for memory safety" |

Both pushed.

## 5. Merge A

PR `tune-batch-size` → `main`, merged. `main` now has `BATCH_SIZE = 5000`.

## 6–7. Conflict B

On `lower-batch-size`, merging `main` in:

```
Auto-merging config.py
CONFLICT (content): Merge conflict in config.py
```

`config.py`:

```python
# Databricks notebook source
CATALOG = "training"
SCHEMA = "sandbox"
<<<<<<< HEAD
BATCH_SIZE = 5000
=======
BATCH_SIZE = 250
>>>>>>> lower-batch-size
```

- `<<<<<<< HEAD` … `=======` → what you merged in (from `main`): `5000`.
- `=======` … `>>>>>>> lower-batch-size` → your branch: `250`.
- `CATALOG`, `SCHEMA` — outside the markers, merged fine.

## 8. Resolve

```python
# Databricks notebook source
CATALOG = "training"
SCHEMA = "sandbox"
BATCH_SIZE = 250  # contested: raised to 5000 on main, lowered here for memory safety
```

All three marker lines deleted. Commit the resolution (dialog or CLI).

## 9. CLI fallback

```bash
cd /Workspace/Users/<you>/databricks-lab
git switch lower-batch-size
git fetch
git merge origin/main
# resolve config.py by hand
git add config.py
git commit
git push
```

Then Pull in the Databricks Git dialog. Abort option: `git merge --abort`.

## 10. Verify

- `config` renders as one clean cell in Databricks.
- Runs without `SyntaxError`.
- `git log --oneline --graph`:
  ```
  *   f1e2d3c Merge branch 'main' into lower-batch-size
  |\
  | * a9b8c7d Raise batch size to 5000
  * | 5d4e3f2 Lower batch size to 250 for memory safety
  |/
  * 1a2b3c4 Add config notebook
  ```

## Key takeaways

- Notebook conflicts are ordinary git conflicts, shown in the **source** form of
  the notebook (`# COMMAND` markers intact).
- Only lines changed on both sides conflict.
- Resolve = edit to final content + delete all three marker lines + `add` +
  `commit`. A stray marker can break the cell, not just a line.
- Git dialog first; provider web editor or CLI as fallback — using the CLI is a
  normal choice, not a failure.
- `git merge --abort` / discard = clean escape hatch.
