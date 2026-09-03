# Module 01 — Connecting to your git provider

Before Databricks can clone a private repo or push your commits, it needs
**credentials** for your git provider. You set these up once per user.

## Supported providers

| Provider | PAT auth | OAuth app auth |
| --- | --- | --- |
| GitHub / GitHub Enterprise Server | ✅ | ✅ (GitHub app) |
| GitLab (SaaS and self-managed) | ✅ | ✅ |
| Azure DevOps Services | ✅ | ✅ (Entra ID on Azure Databricks) |
| Bitbucket Cloud / Bitbucket Server | ✅ | — |
| AWS CodeCommit | ✅ (deprecated by AWS) | — |
| Any other git server | ✅ ("Custom" / bring-your-own) | — |

This course uses **GitHub** with a **personal access token** in the examples.
GitLab is nearly identical; the differences are noted.

## Two layers of "connecting"

Don't confuse them:

| Layer | Who sets it | What it does |
| --- | --- | --- |
| **Workspace admin: Git integration** | Workspace admin (once) | Enables Git folders, sets the allowed provider(s) and any URL allow-list, optionally enforces a proxy |
| **Your linked git credentials** | You (every user) | Authenticates *you* to the provider so your clones/pushes work and commits are attributed to you |

If Git folders are missing entirely from your workspace, it's the first layer —
ask an admin (**Settings → Advanced → Git integration** / the account console).

## Setting up your linked credentials (PAT)

### 1. Create the token in your git provider

**GitHub** → Settings → Developer settings → **Personal access tokens**:

- **Fine-grained token** (preferred): scope it to the specific repos, grant
  **Contents: Read and write** and **Metadata: Read-only** (fine-grained tokens
  need Metadata). Set an expiry.
- Or **classic token**: check the **`repo`** scope. Set an expiry.

**GitLab** → Profile → **Access Tokens** → scopes **`write_repository`** (and
`read_repository`). Set an expiry.

**Azure DevOps** → User settings → **Personal access tokens** → scope **Code:
Read & Write**.

Copy the token — you see it once.

### 2. Add it to Databricks

In Databricks: your **username (top right) → Settings → Linked accounts** (older
UIs: **User Settings → Git integration**).

- **Git provider**: GitHub (or GitLab, etc.)
- **Git provider username or email**: your username on that provider
- **Token**: paste the PAT
- **Save**

Databricks stores it encrypted and uses it for all your Git folder operations.

### 3. Verify

Create a throwaway Git folder from a small private repo (Module 03 / Exercise
01). If it clones, you're connected. If you get `Authentication failed` or
`could not read Username`, the token is wrong, expired, or missing the scope.

## OAuth instead of a PAT

For GitHub, GitLab, and Azure DevOps, Databricks can connect via an **OAuth
app** — you click "Link Git account", authorize in the provider's browser
dialog, and Databricks manages a short-lived token. No PAT to create, rotate, or
leak.

- Same place: **Settings → Linked accounts → Link Git account** and pick the
  OAuth flow if offered.
- Your workspace admin may need to enable/configure the OAuth application first
  (especially for GitHub Enterprise or self-managed GitLab).
- **Prefer OAuth** where available — tokens rotate automatically.

## Service principals (for jobs and CI — preview here)

Your *personal* credentials run *your* interactive Git folder operations. For
**automated** things — a job that runs from Git, a CI pipeline that deploys —
you use a **service principal** with its own git credentials, so automation
doesn't depend on any one person's token. Module 07 (jobs) and Module 10
(identities) cover this. For now, just know: personal token = your clicking;
service principal = automation.

## Token hygiene

- **Set an expiry.** A never-expiring token is a standing liability.
- **Scope it down** — one repo or one org, read/write to contents only. Not
  `admin`, not `workflow`, not `delete_repo`.
- **It's yours.** Commits made from your Git folder are attributed to your
  linked identity. Don't share the token or the account.
- If it leaks: revoke it in the provider immediately, create a new one, update
  **Settings → Linked accounts**.
- Rotate on your provider's schedule; Databricks just needs the new value pasted
  in.

## Troubleshooting

| Symptom | Likely cause |
| --- | --- |
| No "Git folders" / "Repos" in the workspace | Admin hasn't enabled Git integration, or the plan doesn't include it |
| `Authentication failed` on clone | PAT wrong/expired, or wrong provider username, or missing scope (`repo` / `write_repository`) |
| `Repository URL not allowed` | Admin has a URL allow-list; your repo host isn't on it |
| Clone works, push fails | Token has read but not write scope (fine-grained token missing "Contents: write") |
| Commits attributed to the wrong name | Wrong "Git provider username or email" in Linked accounts |
| OAuth link button missing | Admin hasn't configured the OAuth app for your provider |

## Check yourself

1. What are the two separate "connection" layers, and who configures each?
2. What GitHub token scope (classic) does a Git folder need to push?
3. Why prefer OAuth over a PAT when your provider supports it?
4. Your interactive Git folder works, but a scheduled job that runs from Git
   fails to clone. Whose credentials does the job use?

<details>
<summary>Answers</summary>

1. Workspace-admin **Git integration** (enables the feature and allowed
   providers), and your personal **Linked accounts / Git credentials**
   (authenticates you). Admin does the first once; every user does the second.
2. The `repo` scope (classic) — or a fine-grained token with **Contents: Read
   and write** plus **Metadata: Read-only**.
3. OAuth tokens are short-lived and rotate automatically — nothing to manually
   create, expire, or leak.
4. A **service principal's** git credentials, not yours. The service principal
   needs its own linked token/OAuth with access to the repo (Module 07/10).

</details>

Next: [Module 02 — Notebooks as source files](02-notebooks-as-source.md)
