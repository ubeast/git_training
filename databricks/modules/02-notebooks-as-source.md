# Module 02 — Notebooks as source files

The thing that makes git-in-Databricks work at all: **a notebook is stored as a
plain text source file.** Understand this format and the rest of the course is
easy.

## What a notebook looks like on disk

A Python notebook `analysis` is committed as `analysis.py`:

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Sales analysis
# MAGIC Loads the daily sales table and computes weekly totals.

# COMMAND ----------

import pyspark.sql.functions as F

sales = spark.table("main.sales.daily")

# COMMAND ----------

weekly = (
    sales.groupBy(F.date_trunc("week", "order_ts").alias("week"))
         .agg(F.sum("amount").alias("total"))
)
display(weekly)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM main.sales.weekly_totals ORDER BY week DESC LIMIT 10
```

The markers:

| Marker | Meaning |
| --- | --- |
| `# Databricks notebook source` | **Must be the first line.** Tells Databricks this `.py` file is a notebook, not a plain script. |
| `# COMMAND ----------` | Cell separator. Everything between two of these is one cell. |
| `# MAGIC %md` / `# MAGIC %sql` / `# MAGIC %run ...` | A magic command. The `# MAGIC ` prefix lets non-Python cell content live in a `.py` file. |
| plain code | A normal Python cell |

Other languages use the same idea with their comment character:

| Notebook language | File | First line | Cell separator |
| --- | --- | --- | --- |
| Python | `.py` | `# Databricks notebook source` | `# COMMAND ----------` |
| SQL | `.sql` | `-- Databricks notebook source` | `-- COMMAND ----------` |
| Scala | `.scala` | `// Databricks notebook source` | `// COMMAND ----------` |
| R | `.r` | `# Databricks notebook source` | `# COMMAND ----------` |

**You almost never edit these markers by hand** — the Databricks editor writes
them. But recognising them means notebook diffs in a PR are readable to you.

## Source format vs `.ipynb` (Jupyter) format

Databricks can store notebooks in two formats. It's a per-user setting:
**Settings → Developer → Notebook default format** (older: **Editor**):

| | **Source** (`.py`, `.sql`, …) | **Jupyter** (`.ipynb`) |
| --- | --- | --- |
| On disk | Text with `# COMMAND` markers | JSON (the standard Jupyter schema) |
| Diffs | Clean line diffs — very reviewable | JSON diffs — noisier, but GitHub/GitLab render `.ipynb` visually |
| Cell outputs | Never stored | *Can* be stored (controlled — see below) |
| Metadata (language, widgets) | Minimal | Richer |
| Best for | Most repos, especially with code review | Notebooks where you want rendered outputs in the repo, or interop with Jupyter tooling |

**Recommendation for a team repo: Source format.** It produces the cleanest
diffs and can't accidentally commit large or sensitive outputs. Use `.ipynb`
deliberately, when you have a reason.

The format applies when you **create** or **import** a notebook. Existing
notebooks in a Git folder keep their current format; you can convert via **File
→ Change notebook format** (or re-create).

## Cell outputs are not committed (by default)

When you commit a Source-format notebook, **only the code is committed** — not
the tables, charts, or `print()` output from your last run. This is what you
want:

- Outputs can be huge (a `display()` of a million rows).
- Outputs can contain **data** — PII, secrets echoed to a cell, customer
  records. You do not want those in git history.
- Outputs create noisy diffs that aren't about the change.

For **`.ipynb`** notebooks, outputs *can* be included, but it's gated:

- **Workspace admin** setting: *"Allow committing .ipynb notebook outputs"* —
  off by default on many workspaces.
- **Per-notebook** toggle in the notebook's settings when the admin allows it.

If you need a result captured for review, put a screenshot in the PR
description, or write a small summary table to a location the reviewer can query
— don't rely on committed outputs.

## `%run` and importing Python modules

Two ways to reuse code across notebooks in a Git folder:

### `%run` — inline another notebook

```python
# MAGIC %run ./utils/common
```

Executes `utils/common` (a notebook) *in the current context* — its functions
and variables become available. Path is relative to the current notebook.
Simple, but: no real imports, hard to test, everything shares one namespace.

### Import a real Python module (preferred for logic)

A Git folder puts the **repo root on `sys.path`**, so a plain `.py` module
(no `# Databricks notebook source` line) can be imported:

```
myrepo/
├── notebooks/
│   └── analysis.py          # the notebook
└── src/
    └── sales_metrics.py     # a normal module: def weekly_totals(df): ...
```

```python
# in analysis (the notebook)
from src.sales_metrics import weekly_totals
weekly = weekly_totals(sales)
```

Now `sales_metrics.py` is unit-testable with `pytest`, reviews cleanly, and
doesn't drag notebook machinery around. **Put real logic in modules; keep
notebooks thin.** (Module 11.)

> Editing an imported module and re-running the notebook? Enable
> **autoreload** (`%load_ext autoreload` / `%autoreload 2`) or detach/reattach,
> so the notebook picks up your module changes.

## Non-notebook files

Modern Git folders support **arbitrary files** — `.py` modules, `.json`, `.yml`,
`.txt`, `requirements.txt`, `databricks.yml`, `.gitignore`, images, small
reference CSVs. They're edited in the same file editor. (There are size limits —
Module 03.)

## Check yourself

1. What must be the very first line of a Python notebook's source file, and what
   separates its cells?
2. You commit a Source-format notebook after running it. Does the chart it
   produced get committed?
3. Why is Source format usually better than `.ipynb` for a team repo?
4. You have a 200-line data-cleaning function used by three notebooks. Where
   should it live, and how do the notebooks use it?

<details>
<summary>Answers</summary>

1. `# Databricks notebook source` (first line); cells are separated by
   `# COMMAND ----------`.
2. No. Source format commits only the code — outputs are never stored.
3. Cleaner, reviewable line diffs; no risk of committing large or sensitive cell
   outputs; less metadata noise.
4. In a plain `.py` module (e.g. `src/cleaning.py`, no notebook-source header).
   The notebooks `from src.cleaning import clean_...` — the Git folder root is
   on `sys.path`. It's then unit-testable and reviews cleanly.

</details>

Next: [Module 03 — Git folders: your first clone](03-git-folders.md)
