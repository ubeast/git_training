# Exercises

Hands-on labs for the GitLab course. Do each after the module noted.

| # | Exercise | After module | You practise |
| --- | --- | --- | --- |
| 01 | [Connect & push](01-connect-and-push/) | 01–03 | SSH key, create a project, push an existing repo, browse it |
| 02 | [Issues & boards](02-issues-and-boards/) | 04 | Issues, labels, milestone, a board, quick actions |
| 03 | [Your first merge request](03-first-merge-request/) | 05–06 | Branch → MR → review (in pairs) → merge, `Closes #` |
| 04 | [Protect main](04-protect-main/) | 07 | Protected branch + approval rule; watch a direct push get rejected |
| 05 | [Your first pipeline](05-first-pipeline/) | 08 | Write `.gitlab-ci.yml`, break a job, read the log, fix it |
| 06 | [A deploy job](06-deploy-job/) | 09 | `environment`, `when: manual` gate, `needs:` |

## Prerequisites for all of these

- A **verified** gitlab.com account (Module 01 — verification is required for
  shared CI runners, which Exercises 05–06 need).
- SSH key set up (Exercise 01 does this) **or** a personal access token.
- Git configured locally (`git config --global --list` shows your name/email).
- For a pairs-based Exercise 03: a partner, and both of you added to the same
  project.

## How to work through one

1. Read the exercise's `README.md`.
2. Do the **Setup** exactly.
3. Work the **Tasks** in order — try each yourself first.
4. Check against **Verify**.
5. Then compare with `SOLUTION.md`.

## Ground rules

- Use a throwaway project (e.g. `<your-username>-gitlab-lab`). Nothing here
  touches the training repo.
- Wedged a project? Delete it (Settings → General → Advanced → Delete project)
  and redo the exercise. Cheap.
- If shared runners aren't working, ask the instructor about the course project
  runner (`tags: [course]`).
