# Instructor Guide — Git Training

For whoever is running the session. The modules are written so a participant
could self-study; your job is pacing, live demos, catching people who fall
behind, and answering "but why?"

## Format and timing

Designed as a **one-day workshop (~6 hours + breaks)** for complete beginners,
or split into 3 × 2-hour sessions. Every module pairs reading/demo with
hands-on time — do not lecture for more than ~15 minutes without people typing.

| Block | Modules | Time | Hands-on |
| --- | --- | --- | --- |
| 1. Foundations | 00, 01 | 45 min | Everyone gets `git --version` and `git config` working |
| 2. The core loop | 02 | 60 min | **Exercise 01** |
| 3. Reading history | 03 | 30 min | Explore their Exercise 01 repo |
| *break* | | 15 min | |
| 4. Undoing | 04 | 45 min | **Exercise 05** (part 1: local undo) |
| 5. Branching | 05 | 60 min | **Exercise 02** |
| *lunch* | | 45 min | |
| 6. Conflicts | 06 | 45 min | **Exercise 03** |
| 7. Remotes | 07 | 60 min | **Exercise 04** |
| *break* | | 15 min | |
| 8. Teamwork | 08, 09 | 45 min | Exercise 05 (part 2) + discussion |
| 9. Wrap | — | 15 min | Q&A, cheat sheet, where to go next |

Adjust freely. If the room is slow, cut Module 03's filters and Module 08's
rebase aside; never cut the hands-on time.

## Setup before day one

Send participants:

1. Install git ahead of time (Module 01, steps 1–2). Offer a 15-min drop-in the
   day before — install problems eat classroom time.
2. Install VS Code (or confirm their editor).
3. Clone this repo.
4. Windows users: use **Git Bash**, not PowerShell or CMD, so commands match.

Have ready:

- A projected terminal with a **large font** (18pt+) and a high-contrast theme.
- Your prompt showing the current branch (starship, oh-my-zsh, or
  `__git_ps1`). Participants need to see branch changes happen.
- `git config --global alias.lg` set so `git lg` works in demos.
- A backup plan for no-network (Exercise 04 is offline by design; the rest is
  local anyway).

## Teaching notes per module

### 00 — Why version control

- Open by asking the room how they currently track versions of documents. The
  `report_final_ACTUAL.docx` pain is universal — let them supply examples.
- Draw the **three areas** diagram on a whiteboard and leave it up all day.
  Refer back to it every time someone is confused about `add` vs `commit`.
- Play the two short videos here or assign as pre-work.
- Don't mention branches/remotes yet beyond naming them.

### 01 — Setup

- Do this live, projected, and walk the room. Everyone must finish with
  `git config --global --list` showing their name and email.
- Push the editor config hard. The #1 lost-15-minutes event in a beginner class
  is someone trapped in vim. Have them set `nano` or `code --wait` now.
- Explain the three config levels briefly; don't dwell.

### 02 — Your first repository

- The heart of the day. Type every command projected; have them mirror you,
  then set them loose on **Exercise 01**.
- Hammer `git status` after *every* step. Make them predict what it'll say
  before you run it.
- Common confusion: "I edited the file after `git add`, why isn't my change in
  the commit?" — this is the staging-area concept landing. Demo it deliberately
  (Exercise 01 has a checkpoint for exactly this).
- `.gitignore` only affecting untracked files trips people up — show the
  `git rm --cached` fix.

### 03 — Looking at history

- Keep it light and exploratory. These commands don't change anything; say so,
  so people poke around fearlessly.
- The `HEAD` / `HEAD~n` notation matters for Module 04 — make sure it lands.
- `git blame` always gets an "oh, nice" — good energy going into a break.

### 04 — Undoing things

- Frame it as **reassurance**, not a warning. "Git is a safety net" is the
  message.
- The decision table at the top is the deliverable. Walk each row with a live
  demo in a scratch repo.
- Be explicit and repeat: **`git restore <file>` and `git reset --hard` and
  `git clean` lose uncommitted work; nothing else does.**
- Demo `git reflog` recovering from `git reset --hard HEAD~3`. This is the
  moment people stop being afraid of git. Don't skip it.
- Emphasise `revert` vs `reset` by whether it's been pushed — this is the bridge
  to Module 07/08.

### 05 — Branching & merging

- Lead with "a branch is just a movable label" and the pointer diagram.
  Creating a branch copies nothing.
- Demo switching branches and watching files appear/disappear in the file
  explorer. Very concrete, very convincing.
- Be crystal clear: **you merge *into* the branch you're on.** `git switch main`
  first. This is the #1 branching mistake.
- Show both a fast-forward and a real merge commit (Exercise 02 produces one of
  each).
- Mention `git checkout` = old spelling; we use `switch`/`restore`.

### 06 — Merge conflicts

- Set the tone: **conflicts are normal, not failure.** Everyone will look
  slightly panicked at the markers — pre-empt it.
- Do it live first (small, one-line conflict), then Exercise 03.
- Decode `<<<<<<< HEAD` / `=======` / `>>>>>>>` slowly. "HEAD is where you are;
  above the `====` is yours, below is theirs."
- Make them search for leftover `<<<<<<<` before committing — demo the broken
  result of not doing so.
- Show VS Code's merge UI *and* the raw-text method. Some people trust the text
  more; that's fine.
- Show `git merge --abort` early so nobody feels trapped.

### 07 — Remotes

- Diagram: two full repos that sync explicitly. Neither is inherently "master."
- The offline local-remote setup in Exercise 04 lets everyone practise
  `push`/`pull` without accounts or network. Walk through creating the bare repo.
- `fetch` vs `pull`: fetch is safe/read-only-ish; pull merges. Draw
  `origin/main` as a separate pointer.
- Rehearse the **rejected push** → `git pull` → `git push` recovery. They *will*
  hit it in real life. Say "never force-push" three times.
- Auth: keep it to one slide. It's a rabbit hole and the GitLab course covers it.

### 08 — Collaboration workflow

- This is where the commands become a routine. Walk the diagram.
- If you have a real GitLab/GitHub instance available, demo opening an actual
  MR/PR from a pushed branch — seeing the web UI ties it together.
- "Keep your branch current by merging `main` into it" — explain that resolving
  conflicts on your own branch keeps them off the team's critical path.
- Rebase: mention it exists, say "use merge for now," move on. Do not teach
  interactive rebase to beginners today.
- Validate that solo/direct-to-`main` is legitimate — not everything needs an MR.

### 09 — Good habits

- Discussion-led. Show real (sanitised) commit messages from your own projects,
  good and bad.
- The secrets point is important — make sure "rotate the key, history keeps it
  forever" lands.
- End on the daily-routine block and the cheat sheet.

## Common participant problems and fixes

| Symptom | Cause / fix |
| --- | --- |
| Stuck in a full-screen editor after `git commit` | Landed in vim. `Esc`, type `:wq`, Enter. Then set `core.editor` (Module 01). |
| `Please tell me who you are` on first commit | `user.name` / `user.email` not set. Module 01 step 3. |
| `fatal: not a git repository` | Not inside a repo folder, or `cd`'d out. `git status` and `pwd` to orient. |
| Committed the wrong thing / too much | Module 04 table. Usually `git reset --soft HEAD~1` and redo. |
| "My files disappeared!" | They switched branches. `git switch <other>` brings them back. Nothing is lost. |
| `git push` rejected | Someone else pushed. `git pull` then `git push`. Module 07. |
| Conflict markers committed into a file | Didn't delete `<<<<<<<`/`=======`/`>>>>>>>`. Edit, `git add`, `git commit`. |
| Huge file / video committed, push is slow | `.gitignore` after the fact doesn't help. `git rm --cached`, commit; for real cleanup, mention `git filter-repo` as a follow-up, not in class. |
| `git pull` made a "weird merge commit" | Expected when both sides had commits. Explain, don't fight it. |
| Detached HEAD warning | They `switch`ed to a commit hash. `git switch main` to return. Harmless. |

## Facilitation tips

- **Predict-then-run.** Before every `git status` / `git log`, ask the room what
  it will show. Keeps everyone modelling the state, not just typing.
- **Whiteboard the pointers.** Branches and `HEAD` are pointer arrows. Draw
  them; move them as commands run.
- **Pair the strugglers.** By Module 05 the spread widens. Pair someone stuck
  with someone comfortable; both learn.
- **Scratch repos are free.** Encourage `mkdir /tmp/scratch && cd /tmp/scratch
  && git init` for trying anything scary. Nothing to break.
- **"Stop and look" is a skill.** Model it: when a demo goes sideways, narrate
  `git status` → `git log` → decision. That habit is half the course.

## Assessment / "did it land?"

Quick end-of-day check — each person, in a fresh repo, unassisted:

1. Init, make two commits.
2. Branch, commit on the branch, merge back to `main`.
3. Create a conflict with a second branch and resolve it.
4. `git reset --soft HEAD~1` and re-commit with a better message.
5. Explain out loud what `git pull` does.

If they can do 1–4 and answer 5, the course worked.

## Where to send people next

- `git help <command>` and `git <command> --help` — the built-in manual.
- *Pro Git* book — free at <https://git-scm.com/book> (chapters 2, 3, 5).
- The **GitLab** course in this repo (merge requests, CI, permissions).
- The **Git in Databricks** course for anyone working in notebooks.
- `learngitbranching.js.org` — visual branch/merge practice.
