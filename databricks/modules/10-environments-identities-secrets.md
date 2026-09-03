# Module 10 — Environments, identities & secrets

The plumbing that makes "the same code, safely, in dev / staging / prod"
actually work.

## Environments

An "environment" in Databricks terms is usually one of:

| Isolation approach | What separates dev/staging/prod |
| --- | --- |
| **Separate workspaces** | Different Databricks workspaces (often different cloud accounts). Strongest isolation. |
| **Separate catalogs in one workspace** | One workspace, Unity Catalog catalogs `main_dev` / `main_staging` / `main_prod`. Common for smaller orgs. |
| **Both** | Separate workspaces *and* separate catalogs. Typical at scale. |

Your Asset Bundle **targets** (Module 08) map onto whichever you use — each
target sets the `workspace.host` and/or the catalog variable.

**Rule:** code is identical across environments; only **config** differs
(catalog, storage paths, cluster size, schedule on/off, which service
principal). That config lives in `databricks.yml` targets and job parameters —
never in the notebook.

## Identities

| Identity | Is | Used for |
| --- | --- | --- |
| **Your user account** | You, SSO login | Interactive work: Git folders, running notebooks on all-purpose clusters, dev bundle deploys |
| **Service principal** | A non-human account with its own credentials | Jobs, CI/CD deploys, anything scheduled or automated |
| **Groups** | Collections of users/SPs | Granting permissions (never grant to individuals) |

### Service principals — why and how

Automation must not run as a person:

- People leave; their tokens get revoked; their permissions change.
- A person's token can do everything *they* can — far more than a deploy needs.

So: **one service principal per environment** (`ci-sp-staging`, `ci-sp-prod`),
each with:

- An **OAuth client ID + secret** (for CI — Module 09).
- A **linked git credential** (a scoped PAT or OAuth) if jobs use a Git source
  (Module 07) — the SP needs its own, created via the account console / API.
- **Least-privilege grants**: `CAN_MANAGE` on its jobs, `USE CATALOG` /
  `MODIFY` on exactly the schemas it writes, and nothing else. Prod SP has no
  access to dev, and vice versa.
- Membership in a group, with permissions granted to the group.

Set a job's executing identity with **Run as** (job → permissions). Set a
bundle target's identity with `run_as: service_principal_name:` (Module 08).

## Secrets

**Never** put a secret in:

- a notebook cell (it's in git history and in the notebook revision history),
- `databricks.yml` or any file in the repo,
- a job parameter's default value,
- a cell's printed output.

### Secret scopes

Databricks stores secrets in **secret scopes**. Two kinds:

| Backend | Setup | Use |
| --- | --- | --- |
| **Databricks-backed** | `databricks secrets create-scope <name>` then `databricks secrets put-secret <scope> <key>` | General use |
| **Azure Key Vault-backed** | Create the scope pointing at a Key Vault (Azure Databricks only) | When secrets are already managed in Key Vault |

Read them at runtime:

```python
token = dbutils.secrets.get(scope="external-apis", key="stripe_token")
```

- The value is **redacted** if you try to `print` it (`[REDACTED]`).
- Grant access per scope with ACLs: `databricks secrets put-acl <scope>
  <principal> READ` — give the **service principal** (or group) READ, not
  individuals.
- Per environment: `external-apis` scope in the prod workspace holds prod
  credentials; the dev workspace's scope of the same name holds dev credentials.
  The notebook code is identical.

### Secrets in CI

The CI system has its own secret store (GitHub Actions secrets, GitLab CI/CD
variables). The **only** secrets there are the ones CI itself needs — the
deploy service principal's OAuth client ID/secret. Everything the *workloads*
need stays in Databricks secret scopes.

## Unity Catalog and data governance (brief)

Unity Catalog is where table/volume permissions live. For this course's
purposes:

- Catalogs (`main_dev`, `main_prod`) are a natural environment boundary.
- Grant the environment's **service principal** the minimum
  (`USE CATALOG`, `USE SCHEMA`, `SELECT`/`MODIFY` on specific schemas).
- The catalog name is a **bundle variable / job parameter**, so the same
  notebook writes to `main_dev` in dev and `main_prod` in prod.

## Putting it together

```
repo (one codebase)
  │
  ├── PR ──► CI: pytest + bundle validate                  [no Databricks identity needed for tests]
  │
  ├── merge to main ──► CI as ci-sp-staging (OAuth M2M) ──► bundle deploy -t staging
  │                        catalog = main_staging
  │                        secrets from "external-apis" scope in staging workspace
  │
  └── tag v* ──► (manual approval) ──► CI as ci-sp-prod ──► bundle deploy -t prod
                           catalog = main_prod
                           secrets from "external-apis" scope in prod workspace
```

One codebase. Config per target. Identity per environment. Secrets in scopes,
per environment. Nothing sensitive in git.

## Check yourself

1. What should be the *only* difference between how code runs in dev vs prod?
2. Why must scheduled jobs and CI deploys run as a service principal, not a
   user?
3. You need a third-party API key in a notebook. Where does it go, and how does
   the notebook read it?
4. The same `dbutils.secrets.get(scope="apis", key="token")` call is in a
   notebook that runs in both dev and prod. How does it get different values?

<details>
<summary>Answers</summary>

1. Configuration — catalog, storage paths, cluster size, schedule enabled,
   executing service principal. The code itself is identical.
2. A user's credentials expire, get revoked, or leave with them, and carry far
   more privilege than a deploy needs. A per-environment service principal is
   stable and least-privilege.
3. In a **secret scope** in that environment's workspace (Databricks-backed or
   Key Vault-backed). The notebook reads it with
   `dbutils.secrets.get(scope=..., key=...)`; the value is redacted if printed.
4. Each workspace (dev, prod) has its own secret scope of the same name holding
   that environment's value. Same code, same key, different scope contents.

</details>

Next: [Module 11 — Everyday good habits](11-good-habits.md)
