# Exercises

Hands-on labs for the Git course. Do each one after the module noted below.

| # | Exercise | After module | You practise |
| --- | --- | --- | --- |
| 01 | [First repository](01-first-repository/) | 02 | init, status, add, commit, staging area, `.gitignore` |
| 02 | [Branching](02-branching/) | 05 | branch, switch, merge, fast-forward vs merge commit |
| 03 | [Merge conflict](03-merge-conflict/) | 06 | create and resolve a real conflict, `merge --abort` |
| 04 | [Remotes](04-remotes/) | 07 | clone, push, pull, rejected-push recovery — all offline |
| 05 | [Undo lab](05-undo-lab/) | 04 (revisit after 07) | restore, reset (×3), amend, revert, reflog |

## How to work through one

1. Open the exercise's `README.md`.
2. Do the **Setup** section exactly.
3. Work the **Tasks** in order. Try each yourself first.
4. Check your work against **Verify**.
5. Only then open `SOLUTION.md` to compare.

## Ground rules

- Every exercise builds its own throwaway repo (usually under `/tmp` or your
  home dir). Nothing here touches the training repo itself.
- If you wedge a repo badly, just `rm -rf` its folder and start the exercise
  over. That's expected and fine.
- Type the commands. Copy-paste teaches nothing.
