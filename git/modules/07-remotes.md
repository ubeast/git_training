# Module 07 — Working with remotes

Everything so far was local. A **remote** is another copy of the repository —
usually on a server like GitLab, GitHub, or Bitbucket — that you and your
teammates sync with.

[Exercise 04](../exercises/04-remotes/) sets up a remote on your own machine so
you can practise without any account.

## The model

```
   your laptop                         the server (e.g. GitLab)
   ┌─────────────┐    git push  ──►    ┌─────────────┐
   │ local repo  │                      │ remote repo │
   │             │    ◄──  git fetch    │  "origin"   │
   └─────────────┘                      └─────────────┘
```

- The remote is a full repo, just like yours. Neither is "the master copy" as
  far as git is concerned — teams *decide* the server's `main` is authoritative.
- You sync explicitly. Git never contacts the network on its own.
- `origin` is the conventional name for "the remote I cloned from." Nothing
  special about the word; it's just the default.

## Getting a copy: `git clone`

```bash
git clone https://gitlab.com/some/project.git
cd project
```

This:
- downloads the whole repo (all history),
- creates the folder,
- sets up the remote named `origin` pointing back at that URL,
- checks out the default branch (`main`).

```bash
git remote -v
```

```
origin  https://gitlab.com/some/project.git (fetch)
origin  https://gitlab.com/some/project.git (push)
```

## Adding a remote to an existing local repo

If you started with `git init` locally and *then* made a server repo:

```bash
git remote add origin https://gitlab.com/you/recipes.git
git push -u origin main
```

`-u` (short for `--set-upstream`) links your local `main` to `origin/main` so
future `git push` / `git pull` need no arguments.

## `origin/main` — the remote-tracking branch

After talking to the remote, git keeps a **read-only** local pointer called
`origin/main` that records "where `main` was on the server last time I checked."

```
local main         →  commit C   (your latest, maybe not pushed)
origin/main        →  commit B   (what the server had at last sync)
```

`origin/main` only updates when you `fetch`, `pull`, `push`, or `clone` — not
magically.

## `git fetch` — download, don't touch my work

```bash
git fetch origin
```

Downloads new commits from the server and updates `origin/main`, but does
**not** change your working directory or your `main`. Totally safe — you can
then inspect what's new:

```bash
git log --oneline main..origin/main     # commits on the server you don't have
git log --oneline origin/main..main     # commits you have that aren't pushed
```

## `git pull` — fetch *and* integrate

```bash
git pull
```

is exactly `git fetch` followed by `git merge origin/main` into your current
branch. So:

- If you have no local commits of your own, it fast-forwards — easy.
- If both you and the server have new commits, it creates a **merge commit**
  (and can hit a conflict — resolve it exactly as in Module 06).

> The Module 01 setting `git config --global pull.rebase false` makes `pull` use
> merge, which is the most predictable behaviour for beginners.

**Habit:** `git pull` before you start work, and again before you push.

## `git push` — upload your commits

```bash
git push                 # once upstream is set with -u
git push origin main     # explicit form
```

### Push rejected

```
 ! [rejected]        main -> main (fetch first)
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do
hint: not have locally.
```

This means someone pushed while you were working. **Do not force.** Do:

```bash
git pull        # integrate their work (merge, maybe resolve a conflict)
git push        # now it goes through
```

### `git push --force` — the footgun

Force-push overwrites the server's branch with yours, **discarding commits other
people may have based work on.** Rule for this course: never force-push a shared
branch. (`--force-with-lease` is a safer variant for rewriting *your own*
un-shared feature branch, but you won't need it here.)

## Pushing a new branch

```bash
git switch -c add-desserts
# ... commits ...
git push -u origin add-desserts
```

On GitLab/GitHub the output includes a link to open a **merge request / pull
request** — that's [Module 08](08-collaboration-workflow.md).

## Deleting a remote branch

```bash
git push origin --delete add-desserts    # after it's merged on the server
git fetch --prune                        # clean up stale origin/* pointers locally
```

## Authentication (briefly)

- **HTTPS**: the server asks for a username and a **personal access token**
  (not your password). A credential helper caches it so you're not retyping.
- **SSH**: you add a public key to your account once; URLs look like
  `git@gitlab.com:you/project.git`. No prompts after setup.

Either is fine. The GitLab course covers setup in detail.

## Command recap

| Command | Does |
| --- | --- |
| `git clone <url>` | Copy a remote repo locally, set up `origin` |
| `git remote -v` | Show configured remotes |
| `git remote add origin <url>` | Point an existing local repo at a server |
| `git fetch` | Download remote commits; don't touch working files |
| `git pull` | `fetch` + `merge` into the current branch |
| `git push` | Upload your commits to the remote |
| `git push -u origin <branch>` | Push and link a branch for future short commands |
| `git fetch --prune` | Drop local `origin/*` pointers for branches deleted on the server |

## Check yourself

1. What's the difference between `git fetch` and `git pull`?
2. Your push is rejected with "fetch first." What do you do — and what do you
   *not* do?
3. What is `origin/main`, and when does it change?
4. You made a local repo with `git init` and now have an empty repo on GitLab.
   Which two commands connect and populate it?

<details>
<summary>Answers</summary>

1. `fetch` only downloads and updates `origin/*` pointers — your files and
   branches are untouched. `pull` does that *and* merges the remote branch into
   your current one (possibly creating a merge commit or a conflict).
2. Run `git pull` to integrate the other person's commits (resolve any
   conflict), then `git push` again. Do **not** `git push --force`.
3. A read-only local pointer recording where the server's `main` was at your
   last sync. It updates on `fetch`, `pull`, `push`, and `clone` — never on its
   own.
4. `git remote add origin <url>` then `git push -u origin main`.

</details>

Next: [Module 08 — A collaboration workflow](08-collaboration-workflow.md)
