# Exercise 04 — Feature branch → PR → merge

**After:** Module 06 · **Time:** ~30 min · Best done **in pairs**.

## Goal

Run one change through the complete loop: branch in a Git folder → Commit & Push
→ Pull Request in the provider → review by a partner → merge → Pull `main`.

## Setup

- Use the **course repo** (protected `main`, you and your partner both have
  write access). If solo, use your `databricks-lab` and add branch protection
  (GitHub: Settings → Branches → add rule for `main`, require a PR + 1 approval;
  GitLab course Module 07).
- Each person has their **own** Git folder cloned from the course repo (Module
  03 — not a shared one).
- Decide who is **A** and who is **B**. You'll each make a change, then review
  each other.

## Tasks

### 1. (Both) Sync and branch

Git dialog → `main` → **Pull** → **Create Branch**:

- A: `a-add-row-count-check`
- B: `b-add-schema-print`

### 2. (Both) Make a small change

Add a notebook `checks` (or edit an existing one) in your Git folder:

- **A** — cell:
  ```python
  def assert_non_empty(df, name):
      n = df.count()
      assert n > 0, f"{name} is empty"
      print(f"{name}: {n} rows")
  ```
- **B** — cell:
  ```python
  def print_schema(df, name):
      print(f"--- {name} schema ---")
      df.printSchema()
  ```

(If you both edit the same `checks` notebook, put your function in your own new
cell — you'll see in step 6 whether that conflicts.)

### 3. (Both) Commit & Push

Git dialog → review the diff → message (`Add row-count check` / `Add schema
print helper`) → **Commit & Push**.

### 4. (Both) Open the PR

Click the **Create pull request** link. Fill in:

- Title: what it does.
- Description:
  ```
  ## What
  <one line>

  ## Why
  Part of the checks helpers. Closes #<ticket if you have one>

  ## How tested
  Ran the notebook on cluster <name>; called the function on a small DataFrame.
  ```
- Reviewer: **your partner**.
- Create.

### 5. (Both) Review your partner's PR

On the provider, open your partner's PR → **Files changed**:

- Leave at least one **comment** on a line (a question or a suggestion).
- If GitHub: use **Start a review** → add comments → **Submit review** with
  "Approve" or "Request changes".
- If the change is fine, **Approve**.

### 6. (Both) Address feedback (if any) and merge

- If your partner requested a change: make it in your Git folder on the **same
  branch**, Commit & Push — the PR updates. Reply to the comment; re-request
  review.
- Once approved + checks green: **Merge** the PR on the provider. Delete the
  branch when prompted.

### 7. (Both) Pull main

Databricks → Git dialog → `main` → **Pull**.

- Confirm **both** your change and your partner's change are now on `main` in
  your Git folder.
- If you both edited the same notebook in non-overlapping cells, the second
  merge may have needed a trivial conflict resolution on the provider — note
  whether it did.

### 8. Inspect

- Git dialog history (or `git log --oneline` in a terminal) shows both merges.
- Open the `checks` notebook on `main` — both helper functions are present.

## Verify checklist

- [ ] Each person worked on their **own** Git folder and **own** branch
- [ ] Each PR had a real description (what / why / how tested)
- [ ] Each person **reviewed and approved** the other's PR on the provider
- [ ] At least one review comment was left and responded to
- [ ] Both changes merged to `main`; both branches deleted
- [ ] After **Pull**, both Git folders show both changes on `main`

## Questions

1. Why does each person need their own Git folder for this?
2. Your partner requested a change. Do you make a new branch?
3. Where did the merge happen — Databricks or the provider?
4. You both added a function to the same notebook. Why might the *second* merge
   have hit a conflict even though you used different cells?

<details>
<summary>Answers</summary>

1. A Git folder has one working state (branch + uncommitted changes). Two people
   committing from one folder overwrite each other. Isolation = separate folders
   + separate branches.
2. No — commit on the **same** branch and push; the PR updates in place.
3. The provider (GitHub/GitLab). Databricks pushed the branch; the merge button
   is on the provider.
4. Adding cells near the same location edits adjacent lines in the same `.py`
   file (the `# COMMAND ----------` region), so git may not be able to
   auto-combine them — a small conflict to resolve on the provider or locally.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
