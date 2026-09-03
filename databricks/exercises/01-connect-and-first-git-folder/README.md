# Exercise 01 — Connect & first Git folder

**After:** Modules 01–04 · **Time:** ~30 min

## Goal

Link your git credentials, create a Git folder, make a branch, edit a notebook,
and Commit & Push — then see the branch in your git provider.

## Setup

You need a repo you can push to. One of:

- The **course repo** your instructor shared (you have write access).
- **Your own new repo**: on GitHub/GitLab, create an empty repo
  `databricks-lab` (add a README so it's not empty), private.

## Part 1 — link credentials

### 1. Create a provider token

- **GitHub**: Settings → Developer settings → Personal access tokens →
  **Fine-grained** → repo access = `databricks-lab` (or the course repo) →
  Permissions: **Contents: Read and write**, **Metadata: Read-only** → expiry
  90 days → generate, copy.
  (Classic token also fine: scope `repo`.)
- **GitLab**: Profile → Access Tokens → scopes `write_repository`,
  `read_repository` → create, copy.

### 2. Add it to Databricks

- Databricks → your **username (top-right) → Settings → Linked accounts**.
- Git provider: GitHub (or GitLab).
- Git provider username/email: your username on that provider.
- Token: paste.
- **Save.**

You should see a connected/linked state. If not, the token or username is
wrong.

## Part 2 — create the Git folder

### 3. Get the clone URL

From your repo on the provider: **Code / Clone → HTTPS**, e.g.
`https://github.com/you/databricks-lab.git`.

### 4. Create the Git folder

- Databricks → **Workspace** → your user folder → **Create → Git folder**.
- Git repository URL: paste the HTTPS URL.
- Git provider: auto-detected — confirm it matches.
- Git folder name: `databricks-lab`.
- **Create Git folder.**

It clones. You now have `/Workspace/Users/<you>/databricks-lab` on the default
branch (`main`).

## Part 3 — the loop

### 5. Pull, then branch

- Open the Git folder → click the **branch / Git button** in the header to open
  the **Git dialog**.
- Confirm branch is `main`. Click **Pull**.
- Click **Create Branch** → name it `add-hello-notebook` → **Create**. The
  dialog now shows you're on `add-hello-notebook`.

### 6. Add a notebook

- In the Git folder, **Create → Notebook** → name `hello` → language **Python**
  → attach to your cluster.
- In cell 1:
  ```python
  greeting = "Hello from a Git folder"
  print(greeting)
  ```
- Add a cell (`# COMMAND ----------` appears automatically), in cell 2:
  ```python
  spark.range(5).show()
  ```
- **Run all** so the notebook has outputs (you'll use this in Exercise 02).

### 7. Review the diff and commit

- Open the **Git dialog**. Under **Changes** you should see `hello.py` as a new
  file.
- Click it — read the diff. Note the `# Databricks notebook source` line and the
  `# COMMAND ----------` separator.
- Commit message: `Add hello notebook`.
- **Commit & Push.**

### 8. See it in the provider

- Databricks usually shows a **Create pull request** link — click it, or go to
  your repo on the provider.
- Confirm: branch `add-hello-notebook` exists, contains `hello.py`, and the file
  is readable source (not JSON, unless your default format is `.ipynb`).
- **Don't open a PR yet** — Exercise 04 does the full PR flow.

### 9. Switch back and forth

- Git dialog → branch selector → `main`. Notice `hello.py` **disappears** from
  the Git folder (it's not on `main`).
- Switch back to `add-hello-notebook` — it returns.

## Verify checklist

- [ ] **Settings → Linked accounts** shows your provider connected
- [ ] The Git folder exists and its header shows a branch name
- [ ] `add-hello-notebook` branch exists **on the provider** with `hello.py`
- [ ] The committed `hello.py` starts with `# Databricks notebook source`
- [ ] Switching to `main` in the Git dialog removes `hello.py` from view;
      switching back restores it
- [ ] You can state the git CLI equivalent of "Create Branch" and "Commit &
      Push"

## Troubleshooting

| Problem | Fix |
| --- | --- |
| No "Git folder" option | Admin hasn't enabled Git integration / Community Edition. Ask an admin. |
| `Authentication failed` on create | Token wrong/expired/mis-scoped, or wrong provider username in Linked accounts. |
| Commit & Push fails but clone worked | Token lacks write (fine-grained: "Contents: Read and write"). |
| `hello.py` committed as JSON / huge diff | Your notebook default format is Jupyter. Settings → Developer → Notebook default format → **Source**, then re-create the notebook. |
| Can't switch to `main` | Uncommitted changes — commit or discard first. |

Compare with [`SOLUTION.md`](SOLUTION.md).
