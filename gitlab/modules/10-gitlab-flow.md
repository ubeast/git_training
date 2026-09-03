# Module 10 — GitLab Flow

You now have all the pieces: branches, MRs, protected `main`, pipelines,
environments. **GitLab Flow** is a lightweight way to arrange them into a
branching strategy. It sits between "commit straight to main" (too loose for a
team) and Git Flow (heavy, with long-lived `develop`/`release`/`hotfix`
branches).

## The core rule

> **`main` is the single source of truth. Every change reaches `main` through a
> merge request from a short-lived feature branch. Deployments flow *out* of
> `main`, never back into it.**

```
issue #42
   │
   ▼
feature branch  (42-fix-login-timeout)
   │  commits, push, open MR
   ▼
merge request   →  pipeline runs  →  review + approval
   │
   ▼
main  ──●──●──●──●──►   (protected; only MRs land here; always deployable)
        │
        └─► pipeline on main deploys to staging, then (gated) production
```

That's the whole model for most teams. The variations below add branches only
when you actually need them.

## Variation A — environment branches

When you can't deploy every `main` commit straight to production (regulated
releases, batched deploys, a manual QA gate), add branches that *represent
environments*:

```
main  ──●──●──●──●──●──►      feature MRs merge here; auto-deploys to staging
              │
              ▼  (MR: main → pre-production, when QA signs off)
pre-prod ─────●──────●──►     auto-deploys to pre-production
                     │
                     ▼  (MR: pre-production → production)
production ──────────●──►     auto-deploys to production
```

- Code only ever moves **downstream**: `main → pre-prod → production`, each hop
  an MR.
- A fix goes into `main` first, then flows down — never patched directly into
  `production`.
- Each branch is protected; merging into it triggers that environment's deploy
  job (`rules: if: $CI_COMMIT_BRANCH == "pre-production"`).

## Variation B — release branches

When you support multiple released versions at once (installed software, APIs
with version guarantees):

```
main  ──●──●──●──●──●──●──●──►
         │           │
         ▼           ▼
      release/1.4  release/2.0     cut when you start stabilising a version
         │           │
      v1.4.0      v2.0.0           tag releases off the release branch
         │
      v1.4.1  ← cherry-pick a fix from main:  git cherry-pick <sha>
```

- Branch `release/X.Y` off `main` when a version is feature-frozen.
- Bug fixes land on `main` first, then are **cherry-picked** into the release
  branch(es) that need them (GitLab's MR page has a **Cherry-pick** button for
  exactly this).
- Tag versions (`v1.4.1`) on the release branch; CI builds the release
  (Module 09).
- Protect `release/*` with a wildcard rule.

## Choosing

| Your situation | Use |
| --- | --- |
| Web app, deploy continuously, one production version | **Just `main` + feature branches** (the core rule) |
| Deploy in batches / need a QA gate before prod | Core rule **+ environment branches** |
| Support several shipped versions simultaneously | Core rule **+ release branches** |
| You think you need `develop` + `release` + `hotfix` + ... | You probably don't. Start with the core rule; add a branch only when a concrete need appears. |

## How it maps to what you've learned

| GitLab Flow needs | Provided by |
| --- | --- |
| `main` can't be pushed to directly | Protected branch, "Allowed to push = No one" (Module 07) |
| Nothing merges broken | "Pipelines must succeed" + approvals (Module 07) |
| Merging `main` deploys staging | `deploy-staging` job with `rules: if branch == main` (Module 08–09) |
| Promoting to prod is deliberate | `when: manual` + protected environment (Module 09) |
| Fixes reach every supported version | Cherry-pick button on the MR (this module) |
| Feature branches stay short | Team discipline + small MRs (Module 11) |

## Anti-patterns

- **Long-lived feature branches.** Weeks of divergence = painful merges and
  stale code. Break the work up; merge behind a feature flag if needed.
- **A permanent `develop` branch** that everything targets and that periodically
  merges to `main`. That's Git Flow; it doubles your integration work. Target
  `main` directly.
- **Hotfixing production directly.** The fix must exist on `main` or it's lost
  in the next deploy. Fix `main`, then flow/cherry-pick down.
- **Environment branches when you deploy continuously.** Pure overhead if every
  `main` commit already goes to prod.

## Check yourself

1. In GitLab Flow, which direction does code move between `main` and environment
   branches — and can it ever go the other way?
2. A critical bug is in production. Where do you commit the fix first?
3. You support v1.x and v2.x in the field. A bug affects both. What's the flow?
4. Someone proposes a long-lived `develop` branch. What's the objection?

<details>
<summary>Answers</summary>

1. Downstream only: `main → pre-prod → production`, each hop via MR. Code never
   flows back up — fixes always start at `main`.
2. On `main` (via a normal feature branch + MR). Then promote/cherry-pick it
   down to the environment or release branches. Never patch production directly.
3. Fix it on `main` first. Then cherry-pick the fix commit into `release/1.x`
   and `release/2.x`, and tag a patch release (`v1.4.1`, `v2.3.1`) on each.
4. It adds a second permanent integration point — every change gets merged
   twice (into `develop`, then `develop` into `main`), doubling conflict
   resolution and CI work, with little benefit over targeting `main` directly
   with short branches.

</details>

Next: [Module 11 — Everyday good habits](11-good-habits.md)
