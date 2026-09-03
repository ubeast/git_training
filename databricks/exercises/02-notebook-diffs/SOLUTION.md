# Exercise 02 — Solution

## 1. The committed source

`hello.py`:

```python
# Databricks notebook source          ← line 1: marks this .py as a notebook
greeting = "Hello from a Git folder"

# COMMAND ----------                   ← cell separator

spark.range(5).show()
```

The output of `spark.range(5).show()` is **nowhere** in the file — Source format
commits code only.

## 2. Outputs aren't committed

After **Run all**, the Git dialog's **Changes** list is **empty** for
`hello.py`. Running a notebook changes its *displayed state* (stored in
Databricks), not its *source file*. Nothing to commit.

## 3. Databricks diff

After editing the greeting and adding a cell, `hello.py` diff:

```diff
  # Databricks notebook source
- greeting = "Hello from a Git folder"
+ greeting = "Hello from Databricks Git folders"

  # COMMAND ----------

  spark.range(5).show()
+
+ # COMMAND ----------
+
+ print(greeting.upper())
```

One changed line + one added cell. Commit `Tweak greeting and add uppercase
cell`, push.

## 4. Provider diff

The commit on GitHub/GitLab shows the identical line diff. That's the whole
point of Source format — the notebook change is reviewable like any code
change. (Toggle to "source"/"raw" view if the provider renders notebooks.)

## 5. `.ipynb` comparison

`hello_ipynb.ipynb` on the provider is JSON:

```json
{
 "cells": [
  {
   "cell_type": "code",
   "source": ["print('hi')"],
   "outputs": [
    {"output_type": "stream", "text": ["hi\n"]}
   ],
   "execution_count": 1
  }
 ],
 "metadata": { ... }
}
```

- Diffs are JSON — execution counts, output blocks, and metadata all churn.
- Whether `"outputs"` is populated depends on the workspace admin setting
  "Allow committing .ipynb notebook outputs" + the per-notebook toggle.
- **Set the format back to Source.** Use `.ipynb` only deliberately.

## 6. `.gitignore`

```
__pycache__/
*.pyc
data/
.databricks/
```

`data/sample.txt` → not listed in Changes (ignored). `.gitignore` → listed,
committed. Behaves exactly like `.gitignore` in any repo.

## Key takeaways

- A Source-format notebook = a readable `.py` with `# Databricks notebook
  source` + `# COMMAND ----------`.
- Outputs are **never** in a Source commit — running before committing is fine
  and adds nothing.
- Databricks diff and provider diff are the same source-level diff → normal code
  review works.
- `.ipynb` = JSON, noisier diffs, can carry outputs — team default should be
  Source.
- `.gitignore` works normally in Git folders.
