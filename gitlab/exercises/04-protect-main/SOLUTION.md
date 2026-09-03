# Exercise 04 — Solution

Mostly settings clicks; the value is in seeing each guard fire.

## 1. Baseline

A fresh project protects `main` but lets Maintainers push directly. So:

```bash
echo "" >> README.md
git commit -am "Direct commit to main"
git push        # SUCCEEDS — you're a Maintainer/Owner
```

## 2. Tighten

**Settings → Repository → Protected branches → main**:

| Field | Set to |
| --- | --- |
| Allowed to push and merge | **No one** |
| Allowed to merge | **Maintainers** |
| Allowed to force push | Off |

## 3. Direct push now blocked

```bash
echo "" >> README.md
git commit -am "Another direct commit to main"
git push
```

```
remote: GitLab: You are not allowed to push code to protected branches on this project.
To gitlab.com:you/gitlab-lab.git
 ! [remote rejected] main -> main (pre-receive hook declined)
error: failed to push some refs to 'gitlab.com:you/gitlab-lab.git'
```

Clean up the local-only commit:

```bash
git reset --hard origin/main
```

## 4. Pipeline + approval requirements

**Settings → Merge requests**:

- ✅ Pipelines must succeed
- ✅ All threads must be resolved
- Approval rule: **Approvals required = 1**
- ✅ Prevent approval by the author
- ✅ Remove all approvals when commits are added

## 5. CODEOWNERS via MR

```bash
git switch -c add-codeowners
mkdir -p .gitlab
cat > .gitlab/CODEOWNERS <<'EOF'
*                 @your-username
/.gitlab-ci.yml   @your-username
EOF
git add .gitlab/CODEOWNERS
git commit -m "Add CODEOWNERS"
git push -u origin add-codeowners
```

On the MR: the **Approve** button is disabled for you (author). The merge widget
shows "Requires 1 approval."

## 6. Merge

- Partner clicks **Approve** (a Developer *can* approve; they just can't
  *merge*).
- A **Maintainer** clicks **Merge**.
- Solo fallback: Approvals required → 0, merge, → back to 1.

```bash
git switch main && git pull
git branch -d add-codeowners
```

## 7. CODEOWNERS auto-assign

```bash
git switch -c tweak-ci
touch .gitlab-ci.yml
git add .gitlab-ci.yml
git commit -m "Add empty CI file"
git push -u origin tweak-ci
```

MR page → right sidebar → **Reviewers** now shows `@your-username`
auto-added, with a "Codeowner" tag, because the diff touches `/.gitlab-ci.yml`.
On Free that's a hint; on Premium with "require code owner approval" it would
block merge.

Close the MR (**Close merge request**), delete the branch:

```bash
git push origin --delete tweak-ci
git switch main
git branch -D tweak-ci
```

## The resulting policy for `main`

Nothing reaches `main` unless:

1. It's in an MR (direct push = rejected).
2. The MR's pipeline is green (once Exercise 05 adds one).
3. All discussion threads are resolved.
4. At least 1 non-author approval exists.
5. A Maintainer clicks Merge.

That's the Module 00 loop, now mandatory.

## Key takeaways

- **"Allowed to push and merge = No one"** kills direct pushes — even yours.
- **"Allowed to merge = Maintainers"** is a separate control for the Merge
  button.
- Approvals: require ≥ 1, block self-approval, reset on new commits.
- **"Pipelines must succeed"** ties CI (next exercise) into the merge gate.
- CODEOWNERS auto-assigns reviewers by path; hard enforcement is Premium.
- Once `main` is locked, *you* have to follow the MR flow too — that's the
  point.
