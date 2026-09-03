# Exercise 04 — Protect main

**After:** Module 07 · **Time:** ~20 min · Uses `gitlab-lab`.

## Goal

Lock down `main` so nothing reaches it except a reviewed, approved, green MR —
and feel each guard by hitting it.

## Tasks

### 1. See the current state

```bash
cd ~/gitlab-lab
git switch main && git pull
```

- **Settings → Repository → Protected branches** — `main` is protected, but
  "Allowed to push and merge" probably includes Maintainers (i.e. you).
- Prove it: make a direct commit to `main` and push.
  ```bash
  echo "" >> README.md
  git commit -am "Direct commit to main (this should stop working soon)"
  git push
  ```
  It **succeeds** right now. Note that.

### 2. Tighten the protected branch

**Settings → Repository → Protected branches → `main`**:

- **Allowed to push and merge** → **No one**
- **Allowed to merge** → **Maintainers**
- **Allowed to force push** → off

Save.

### 3. Try to push to main directly

```bash
echo "" >> README.md
git commit -am "Another direct commit to main"
git push
```

Expected:

```
remote: GitLab: You are not allowed to push code to protected branches on this project.
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to '...'
```

**Undo that local commit** so your branch matches the server:

```bash
git reset --hard origin/main
```

### 4. Require a pipeline and approvals

**Settings → Merge requests**:

- **Merge checks**: tick **Pipelines must succeed**.
- **Merge checks**: tick **All threads must be resolved**.
- **Approval rules** → **Approvals required** = **1**.
- Tick **Prevent approvals by the author of the merge request**.
- Tick **Remove all approvals when commits are added to the source branch**.

Save.

### 5. Add a CODEOWNERS file (through an MR, because you must now)

```bash
git switch -c add-codeowners
mkdir -p .gitlab
cat > .gitlab/CODEOWNERS <<'EOF'
# Everything
*                 @your-username

# CI config needs a platform reviewer
/.gitlab-ci.yml   @your-username
EOF
git add .gitlab/CODEOWNERS
git commit -m "Add CODEOWNERS"
git push -u origin add-codeowners
```

Open the MR. Observe:

- It **cannot** be merged without 1 approval.
- You **cannot approve it yourself** (you're the author) — the Approve button is
  disabled or absent.

### 6. Get it merged

For the course, one of:

- Your **partner** (added as Developer won't be enough to *merge*, but can
  *approve*) approves; then a **Maintainer** (you, or the instructor) merges.
- Solo with no Maintainer helper: temporarily set **Approvals required = 0**,
  merge, then set it back to 1. (In real life you'd never approve-bypass your
  own change — this is just to unblock the lab.)

After merge:

```bash
git switch main && git pull        # CODEOWNERS is now on main
git branch -d add-codeowners
```

### 7. See CODEOWNERS auto-assign

```bash
git switch -c tweak-ci
touch .gitlab-ci.yml
git add .gitlab-ci.yml
git commit -m "Add empty CI file"
git push -u origin tweak-ci
```

Open the MR. Because it touches `/.gitlab-ci.yml`, the CODEOWNERS entry
auto-adds `@your-username` as a reviewer. (On Free this is a suggestion, not a
hard requirement — note the difference.)

Close this MR without merging (**Close merge request**) and delete the branch —
Exercise 05 builds the real CI file.

## Verify checklist

- [ ] A direct `git push` to `main` is now **rejected** with "not allowed to
      push code to protected branches"
- [ ] `main`'s MRs require **1 approval**, and you **can't approve your own**
- [ ] "Pipelines must succeed" and "All threads must be resolved" are enabled
- [ ] `CODEOWNERS` is on `main` (merged via an MR, not pushed directly)
- [ ] An MR touching `.gitlab-ci.yml` auto-adds the code owner as reviewer
- [ ] You can explain the difference between "Allowed to push and merge" and
      "Allowed to merge"

## Questions

1. After step 2, can *you* (Maintainer/Owner) still `git push origin main`? Can
   you still click **Merge** on an MR?
2. What's the difference between "Allowed to push and merge = No one" and
   "Allowed to merge = Maintainers"?
3. On GitLab Free, does CODEOWNERS *force* the code owner to approve before
   merge?
4. Why enable "Remove all approvals when commits are added"?

<details>
<summary>Answers</summary>

1. No to `git push origin main` — "No one" means no one, including you. Yes to
   clicking **Merge** on an MR — that's governed by "Allowed to merge =
   Maintainers".
2. "Allowed to push and merge" controls direct `git push` to the branch (set to
   No one = MR-only). "Allowed to merge" controls who can click the Merge button
   on an MR targeting the branch.
3. No — on Free it auto-assigns the owner as a reviewer but doesn't block merge
   on their approval. Enforced code-owner approval is Premium.
4. So an approval always reflects the exact code being merged; a later push
   can't ride in on a stale approval without re-review.

</details>

Compare with [`SOLUTION.md`](SOLUTION.md).
