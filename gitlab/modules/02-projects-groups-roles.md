# Module 02 — Projects, groups & roles

## Projects

A **project** is the GitLab unit that wraps one git repository. It also holds
that repo's issues, merge requests, pipelines, wiki, settings, and more. When
someone says "the repo" in GitLab, they usually mean the project.

### Creating one

**New project** (top nav `+` → **New project/repository**), then:

| Choice | When |
| --- | --- |
| **Create blank project** | Starting fresh |
| **Create from template** | Want a language/framework skeleton |
| **Import project** | Moving from GitHub, Bitbucket, another GitLab, or a bare repo URL |

Key fields:

- **Project name** → also sets the URL slug (`my-project`).
- **Project URL** → the namespace: your personal namespace, or a group.
- **Visibility**: Private (members only), Internal (any logged-in user on the
  instance), Public (anyone).
- **Initialize with a README** → leave **unchecked** if you're about to push an
  existing local repo (an initial commit on the server makes your first push a
  non-fast-forward).

### Pushing an existing local repo to a new empty project

GitLab shows these commands on the empty project page:

```bash
cd my-existing-repo
git remote add origin git@gitlab.com:your-group/my-project.git
git push -u origin main
```

(Exactly the Git course, Module 07.)

## Groups

A **group** is a namespace that contains projects and/or other groups
(subgroups, nested as deep as you like):

```
acme-corp/                        (group)
├── platform/                     (subgroup)
│   ├── api                       (project)
│   └── infra                     (project)
└── mobile/                       (subgroup)
    └── android-app               (project)
```

Groups give you:

- **Shared membership** — add someone to `acme-corp/platform` once and they get
  access to every project under it, at the role you assign.
- **Inherited settings** — CI/CD variables, runners, labels, milestones,
  templates defined on a group apply to all its projects.
- **Group-level views** — issues and MRs aggregated across all projects,
  epics (Premium), a group board.

### Creating a group

Top nav `+` → **New group**. Give it a name and URL. Then create projects
inside it, or **transfer** existing projects in (project → **Settings** →
**General** → **Advanced** → **Transfer project**).

Personal projects live in your **personal namespace** (`gitlab.com/your-username/…`).
For anything shared, prefer a group — moving later is possible but changes URLs.

## Roles (permission levels)

Every member of a project or group has exactly one **role**. From least to most
access:

| Role | Can, roughly | Typical use |
| --- | --- | --- |
| **Guest** | View issues, comment, view public code; **cannot** see private repo code | Stakeholders, reporters |
| **Reporter** | Everything Guest + view code, pull, view pipelines, manage issues/labels/boards | PMs, QA, read-only devs |
| **Developer** | Everything Reporter + push to **unprotected** branches, create MRs, run pipelines, push to the container registry | Most engineers |
| **Maintainer** | Everything Developer + push to **protected** branches, merge MRs, manage project settings, add members up to Maintainer, manage CI/CD variables | Team leads, senior devs |
| **Owner** | Everything Maintainer + delete the project, transfer it, manage Owners | Group owners (project-level Owner only exists in groups) |

Points that trip people up:

- A **Developer cannot merge into `main`** if `main` is a protected branch
  (Module 07) — by default only Maintainers can. This is intentional.
- Roles **inherit downward**: your role on a group applies to every project in
  it. You can be granted a *higher* role on a specific project, never lower.
- Adding a member: project/group → **Manage** → **Members** → **Invite
  members**, choose the role and an optional expiry.

## Project settings you'll actually touch

Project → **Settings**:

| Section | What's there |
| --- | --- |
| **General** | Name, description, visibility, default branch, "merge request" defaults, project features on/off (wiki, snippets, CI/CD…) |
| **Repository** | Protected branches, protected tags, default branch, branch rules, mirroring, deploy keys |
| **Merge requests** | Merge method (merge commit / squash / fast-forward), approval rules, "pipelines must succeed", auto-close issues |
| **CI/CD** | Runners, variables, pipeline schedules, general pipeline settings, token |
| **Members** | Who's in, at what role |

## Check yourself

1. What does a project contain besides the git repository?
2. Your team has 8 repos and everyone needs access to all of them. Better: add 8
   people to 8 projects, or...?
3. A new engineer has the **Developer** role. They open an MR, the pipeline
   passes, they click Merge — and it's greyed out. Why?
4. Can someone with the **Reporter** role push code?

<details>
<summary>Answers</summary>

1. Its issues, merge requests, CI/CD pipelines and config, wiki, snippets,
   settings, members, releases, container images, and packages.
2. Put the 8 projects in a **group** and add the 8 people to the group once.
   Access inherits down to every project.
3. `main` is a protected branch, and by default only **Maintainers** can merge
   into a protected branch. A Maintainer needs to merge it, or the protected-
   branch rule needs to allow Developers to merge.
4. No. Reporter is read-only for code (pull/view). Pushing requires at least
   **Developer**, and even then only to unprotected branches.

</details>

Next: [Module 03 — The GitLab web UI](03-web-ui.md)
