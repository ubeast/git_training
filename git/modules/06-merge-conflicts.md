# Module 06 — Merge conflicts

A conflict is **not an error and not a bug**. It's git saying: "two people
changed the same lines and I won't guess which one wins — you decide."

[Exercise 03](../exercises/03-merge-conflict/) has you create one deliberately
and resolve it.

## When conflicts happen

Only when **the same region of the same file** was changed on both branches
since they split. If two branches edit different files, or different parts of
one file, git merges them automatically with no drama.

## What it looks like

```bash
git switch main
git merge add-toppings
```

```
Auto-merging pancakes.md
CONFLICT (content): Merge conflict in pancakes.md
Automatic merge failed; fix conflicts and then commit the result.
```

`git status` now guides you:

```
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   pancakes.md
```

## Reading the conflict markers

Open `pancakes.md`. Git has inserted markers around the disputed region:

```
## Pancakes
Flour, milk, eggs.
<<<<<<< HEAD
Serve with maple syrup.
=======
Serve with fresh berries and cream.
>>>>>>> add-toppings
Mix, then fry.
```

| Marker | Meaning |
| --- | --- |
| `<<<<<<< HEAD` | Start of **your current branch's** version (`main`) |
| `=======` | Divider between the two versions |
| `>>>>>>> add-toppings` | End — the part above the divider is `HEAD`, below is the incoming branch |

Everything outside the markers merged fine and is already correct.

## Resolving it

**You edit the file by hand** to what it should finally be, and **delete all
three marker lines**. Your options for the disputed part:

- Keep yours (delete the incoming version and markers)
- Keep theirs (delete your version and markers)
- Combine them
- Write something new entirely

Say you want both toppings:

```
## Pancakes
Flour, milk, eggs.
Serve with maple syrup, or with fresh berries and cream.
Mix, then fry.
```

No `<<<<<<<`, `=======`, or `>>>>>>>` left anywhere. (Search the whole project
for `<<<<<<<` before committing — leftover markers are a classic mistake.)

## Finishing the merge

```bash
git add pancakes.md        # marks this file's conflict as resolved
git status                 # confirm nothing still "both modified"
git commit                 # completes the merge (pre-filled message is fine)
```

If several files conflicted, resolve and `git add` each one, then a single
`git commit`.

## Backing out

Decided you don't want to deal with it right now?

```bash
git merge --abort
```

Everything returns to exactly how it was before you ran `git merge`. Safe.

## Tools that make this easier

- **VS Code** shows conflicts with "Accept Current / Accept Incoming / Accept
  Both / Compare" buttons above each region. Clicking them edits the file for
  you; you still `git add` and `git commit`.
- `git mergetool` launches a configured 3-way merge tool.
- `git checkout --ours pancakes.md` / `--theirs pancakes.md` takes one whole
  side for that file (blunt — only when you're sure).

## Reducing how often you hit conflicts

- Pull / merge from the shared branch **often** so you're never far behind.
- Keep branches **short-lived** and focused.
- Keep commits small — smaller changes overlap less.
- Agree on formatting (a shared formatter) so whitespace churn doesn't collide.

Conflicts are routine on a team. Being calm and methodical about the markers is
the whole skill.

## Check yourself

1. Your branch is `feature`; you ran `git merge main` and hit a conflict. In the
   markers, which side is between `<<<<<<< HEAD` and `=======`?
2. After editing the file to resolve it, what two commands finish the merge?
3. You realise mid-resolution you want no part of this. One command?
4. The merge "succeeded" but the app is broken because a file still contains
   `=======` on its own line. What happened?

<details>
<summary>Answers</summary>

1. Your current branch's version — `feature`, since that's where `HEAD` is.
2. `git add <file>` (for each resolved file), then `git commit`.
3. `git merge --abort`.
4. You committed without deleting all the conflict markers. Edit the file to
   remove the stray markers, then `git add` + `git commit` (a normal follow-up
   commit is fine, or `git commit --amend` if it wasn't pushed).

</details>

Next: [Module 07 — Working with remotes](07-remotes.md)
