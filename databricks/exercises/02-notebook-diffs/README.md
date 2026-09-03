# Exercise 02 — Notebook diffs & the source format

**After:** Module 02 · **Time:** ~20 min · Uses the `databricks-lab` Git folder
and `add-hello-notebook` branch from Exercise 01.

## Goal

See exactly what a notebook looks like in git, prove that outputs aren't
committed, and read a source diff both in Databricks and in the provider.

## Tasks

### 1. Read the committed source

On the provider (GitHub/GitLab), open `hello.py` on the `add-hello-notebook`
branch. Identify and write down:

- [ ] The first line
- [ ] The cell separator between your two cells
- [ ] Where the output of `spark.range(5).show()` is (trick question)

### 2. Confirm outputs aren't committed

Back in Databricks, on `add-hello-notebook`:

- Open `hello`. **Run all** again — you have fresh outputs (a table, printed
  text).
- Open the **Git dialog → Changes**.
- Is `hello.py` listed as changed? **It should not be** — running a notebook
  doesn't change its source, and outputs aren't tracked.
- Conclusion: your last run's results are *not* going anywhere near git.

### 3. Make a real change and read the diff in Databricks

- In `hello` cell 1, change the greeting:
  ```python
  greeting = "Hello from Databricks Git folders"
  ```
- Add a third cell:
  ```python
  # COMMAND ----------  (added automatically)
  print(greeting.upper())
  ```
- Open the **Git dialog → Changes → `hello.py`**. Read the diff:
  - One line changed (the greeting string) — `-` old, `+` new.
  - A new cell block added at the end (`# COMMAND ----------` + the `print`).
- Commit: `Tweak greeting and add uppercase cell`. **Commit & Push.**

### 4. Read the same diff in the provider

- On the provider, open the **commit** you just pushed (or the branch's file
  history).
- You see the *same* line-level diff: the changed string, the added cell. It's
  reviewable like any code change.
- If your provider renders `.py` notebooks specially, toggle to the raw/source
  view to see the markers.

### 5. Compare: what an `.ipynb` diff looks like (optional, instructive)

If you have time:

- Databricks → **Settings → Developer → Notebook default format → Jupyter**.
- Create a new notebook `hello_ipynb` in the Git folder, add a cell, **run it**,
  Commit & Push.
- Look at `hello_ipynb.ipynb` on the provider — it's **JSON**, and (depending on
  workspace settings) may include an `"outputs"` array.
- Switch the setting **back to Source**. Note why Source is the team default:
  the `.py` diff in step 4 was readable; the JSON one is not.

### 6. The `.gitignore` check

- In the Git folder, create a file `.gitignore` (Create → File):
  ```
  __pycache__/
  *.pyc
  data/
  .databricks/
  ```
- Create a folder `data/` with a file `data/sample.txt` (any content).
- Open the **Git dialog → Changes**. `.gitignore` should be listed;
  `data/sample.txt` should **not** (it's ignored).
- Commit `.gitignore` as `Add .gitignore`. **Commit & Push.**

## Verify checklist

- [ ] You located the source markers in `hello.py` on the provider
- [ ] Running the notebook produced **no** entry in the Git dialog's Changes
- [ ] The Databricks diff and the provider diff for step 3 show the same
      line-level change
- [ ] (If done) you saw the `.ipynb` JSON diff and can say why Source is
      preferred
- [ ] `data/sample.txt` was ignored by `.gitignore`; `.gitignore` itself was
      committed

## Questions

1. You ran a notebook that `display()`s a 2-million-row table, then committed.
   How big is that addition to the repo?
2. Why does a Databricks PR reviewer prefer Source-format notebooks?
3. `.gitignore` in a Git folder — does it work the same as in a normal repo?
4. Where did the output of `spark.range(5).show()` go, if not into git?

<details>
<summary>Answers</summary>

1. Zero — Source format commits code only. The table never touches git.
2. The diff is readable line-by-line source, so they can actually review the
   logic change. `.ipynb` diffs are JSON and hard to read (though providers
   render them visually).
3. Yes — `.gitignore` behaves exactly as in any git repo; the Git dialog
   respects it and won't list ignored files as changes.
4. It was rendered in the notebook UI and stored in Databricks' own notebook
   state / revision history — not in the git commit.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
