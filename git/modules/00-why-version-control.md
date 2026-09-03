# Module 00 — Why version control

## The problem

You have probably done some version of this:

```
report.docx
report_v2.docx
report_v2_final.docx
report_v2_final_ACTUAL.docx
report_v2_final_ACTUAL_jane_edits.docx
```

This "works" until you need to answer questions like:

- What exactly changed between `v2` and `v2_final`?
- Who wrote this paragraph, and when, and why?
- Jane and I both edited `ACTUAL` at the same time — how do we combine our work?
- This version was fine last Tuesday. Can I get *exactly* that back?

A **version control system** (VCS) answers all of those. Git is the most widely
used one by a wide margin.

## What git actually does

Git records **snapshots** of a folder over time. Each snapshot is called a
**commit**. A commit stores:

- the full state of your tracked files at that moment,
- who made it and when,
- a short message describing *why*,
- a link to the commit that came before it.

Because every commit links to its parent, your project history is a **chain of
snapshots** (later, a branching tree). You can move back and forth along that
chain, compare any two points, and see who changed what.

> **Snapshots, not differences.** Many people assume git stores "the changes."
> Conceptually it stores the whole state at each commit (it's clever about not
> wasting disk space). Thinking "each commit is a complete saved version" will
> steer you right.

## The three areas (the core mental model)

This is the one picture to hold in your head. Every file in a git project lives
in one of three places at any moment:

```
   working directory          staging area              repository
   (your actual files)   →     (the next snapshot,  →    (permanent history
                                being assembled)          of commits)

        edit files          git add <file>            git commit
        ───────────►        ──────────────►           ──────────────►
```

| Area | What it is | You put things here with |
| --- | --- | --- |
| **Working directory** | The real files on disk you edit | your editor |
| **Staging area** (a.k.a. "index") | A holding area for what will go into the *next* commit | `git add` |
| **Repository** | The saved history — commits, permanent | `git commit` |

Why a staging area in the middle? It lets you commit *some* of your current
changes and not others, so each commit can be one clean, logical unit even if
your working directory is a mess of half-finished ideas.

You will run `git status` constantly to see which files are in which area.
That's normal and expected.

## Local first

Git runs entirely on your machine. You do **not** need a network connection, a
server, or a GitHub/GitLab account to use it. All of Modules 02–06 happen purely
on your laptop.

A **remote** (Module 07) is just another copy of the repository somewhere else —
often on a server like GitHub or GitLab — that you sync with. Collaboration is
built on top of the local fundamentals, not instead of them.

## Vocabulary you'll meet

| Term | Meaning |
| --- | --- |
| **repository / repo** | A project tracked by git (a folder with a hidden `.git/` subfolder) |
| **commit** | One saved snapshot, with a message and an author |
| **branch** | A movable label pointing at a commit; lets you develop in parallel |
| **`HEAD`** | "Where I am right now" — usually the tip of the current branch |
| **remote** | Another copy of the repo you sync with (e.g. on GitLab) |
| **clone** | Make a local copy of a remote repo |
| **push / pull** | Send your commits to a remote / get commits from a remote |
| **merge** | Combine the work from two branches |
| **conflict** | Git can't auto-combine two edits to the same lines; you decide |

Don't try to memorize this. You'll use each term enough over the next few hours
that it will stick.

## Watch

Two short videos reinforce this module — see [`../videos/links.md`](../videos/links.md):

- *Git Explained in 100 Seconds* — the elevator pitch
- *How Git Works: Explained in 4 Minutes* — the snapshot model

## Check yourself

1. What three things does a commit record besides the file contents?
2. Name the three areas a file can be in. Which command moves a file from the
   first to the second?
3. True or false: you need an internet connection to make a commit.
4. What is `HEAD`?

<details>
<summary>Answers</summary>

1. Author, timestamp, a message, and a link to the parent commit.
2. Working directory → staging area → repository. `git add` moves a file into
   the staging area.
3. False. Git is local; commits never need a network.
4. A pointer to "where you are now" in history — normally the latest commit on
   the branch you're on.

</details>

Next: [Module 01 — Setup & configuration](01-setup.md)
