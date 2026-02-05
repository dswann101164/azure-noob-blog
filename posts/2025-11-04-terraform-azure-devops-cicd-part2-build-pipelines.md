---
title: "Terraform + Azure DevOps CI/CD: Part 2 - Build Pipelines (Status Check & Plan)"
date: 2025-11-04
summary: "Build the two pipelines that validate Terraform code on pull requests and create deployment artifacts on merge. GUI-based, no YAML, full control."
tags: ["azure", "terraform", "devops", "cicd", "iac", "azure-devops"]
cover: "static/images/hero/terraform-devops-part2.png"
hub: governance
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
---
Part 1 covered prerequisites (storage, Key Vault, service principal). Now we build the pipelines that actually DO something.


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

**Two build pipelines:**
1. **Terraform Status Check** - Runs on PR creation (validate + plan, no artifact)
2. **Terraform Plan** - Runs on merge to main (plan + archive artifact)

Both use **classic GUI pipelines** (not YAML) for easier troubleshooting and visual control.

## Why Two Build Pipelines?

**Status Check Pipeline:**
- **Triggers:** Pull request created or updated
- **Purpose:** Fast feedback - is the code syntactically correct? What will it do?
- **Output:** Plan results displayed in PR, no artifact saved
- **Approval:** None required (automatic)

**Plan Pipeline:**
- **Triggers:** Code merged to `main` branch
- **Purpose:** Create deployment artifact from approved code
- **Output:** `.tfplan` file archived as build artifact
- **Approval:** None (artifact doesn't deploy anything yet)

**Why separate?** Status checks need to be fast (< 1 minute). Creating artifacts takes longer and isn't needed for every PR update. Separation keeps feedback loops tight.

## Pipeline 1: Terraform Status Check

This pipeline runs **every time** someone creates or updates a pull request. It validates syntax and shows what Terraform will do.

### Create the Pipeline

1. Go to **Pipelines > Pipelines**
2. Click **New pipeline**
3. Click **Use the classic editor** (bottom link, easy to miss)
4. Select your repo and branch: `main`
5. Choose template: **Empty job**

### Configure Pipeline Settings

**Pipeline name:** `Terraform Status Check (Validate + Plan)`

**Agent pool:**
- Pool: **Azure Pipelines**
- Agent Specification: **ubuntu-latest** (or `ubuntu-22.04`)

**Why Ubuntu?** Faster than Windows agents, Terraform works the same on Linux, no licensing concerns.

### Add Tasks

Click **Agent job 1** and rename to: `Terraform Status Check`

Now add tasks (click the **+** button):

#### Task 1: Use Terraform (Installer)

Search for "Terraform" and add the **Terraform installer** task.

**Settings:**
- **Display name:** `Install Terraform 1.5.7`
- **Version:** `1.5.7` (or whatever version you're standardizing on)

**Why specify version?** Hosted agents pre-install Terraform, but the version changes. Explicitly installing ensures consistency.

#### Task 2: Download Key Vault Secrets

We need the storage account access key before running `terraform init`.

Search for "Azure Key Vault" and add the task.

**Settings:**
- **Display name:** `Download secrets from Key Vault`
- **Azure subscription:** Your service connection (`terraform-azure-connection`)
- **Key vault:** Your Key Vault name (`kv-tfstate-1234`)
- **Secrets filter:** `*` (downloads all secrets you have access to)

**What this does:** Pulls all secrets from Key Vault and makes them available as environment variables in subsequent tasks.

**Example:** Secret `sttfstate1234-key1` becomes `$(sttfstate1234-key1)` in pipeline variables.

#### Task 3: Terraform Init (Command Line)

We're NOT using the marketplace Terraform tasks. Why? Full control over flags and environment variables.

Search for "Command Line" and add the task.

**Settings:**
- **Display name:** `Terraform Init`
- **Script:**

```bash
terraform init \
  -backend-config="access_key=$(sttfstate1234-key1)"
```

**Advanced > Working Directory:** `$(System.DefaultWorkingDirectory)/terraform`

**What this does:**
- Changes to the `/terraform` folder in your repo
- Runs `terraform init`
- Injects the storage account access key at runtime (from Key Vault)
- Connects to remote backend and downloads existing state

**Why `-backend-config`?** The `backend.tf` file doesn't include the access key (we never commit that). This flag passes it securely at runtime.

**Replace `sttfstate1234-key1`** with YOUR storage account secret name from Key Vault.

#### Task 4: Terraform Validate

Clone the previous command line task (right-click > Clone).

**Settings:**
- **Display name:** `Terraform Validate`
- **Script:**

```bash
terraform validate
```

**Advanced > Working Directory:** `$(System.DefaultWorkingDirectory)/terraform`

**What this does:** Checks Terraform syntax and configuration validity. Fails the pipeline if there are errors.

#### Task 5: Terraform Plan

Clone the command line task again.

**Settings:**
- **Display name:** `Terraform Plan`
- **Script:**

```bash
terraform plan \
  -input=false \
  -var="subscription_id=$(subscription-id)" \
  -var="spn_client_id=$(sp-terraform-devops-client-id)" \
  -var="spn_client_secret=$(sp-terraform-devops-client-secret)" \
  -var="spn_tenant_id=$(sp-terraform-devops-tenant-id)"
```

**Advanced > Working Directory:** `$(System.DefaultWorkingDirectory)/terraform`

**What this does:**
- Runs `terraform plan` (but doesn't save output to a file)
- Passes service principal credentials as variables (from Key Vault)
- Shows what would deploy in the pipeline logs
- `-input=false` prevents prompts (important for automation)

**Critical:** Replace the variable names with YOUR Key Vault secret names:
- `subscription-id` - Your Azure subscription ID (add this as a regular pipeline variable, not a secret)
- `sp-terraform-devops-client-id` - Service principal client ID (from Key Vault)
- `sp-terraform-devops-client-secret` - Service principal secret (from Key Vault)
- `sp-terraform-devops-tenant-id` - Tenant ID (from Key Vault)

**Where to add subscription ID?** Since it's not sensitive, add it as a regular pipeline variable:
1. Click **Variables** tab at the top
2. Click **+ Add**
3. Name: `subscription-id`
4. Value: Your subscription GUID
5. Keep secret: **Unchecked**

### Link Variable Group

Click the **Variables** tab, then **Variable groups**.

Click **Link variable group** and select: `terraform-keyvault-secrets`

This gives the pipeline access to all Key Vault secrets.

### Configure Trigger

**Important:** We do NOT want this pipeline to run on every commit. It should ONLY run via branch policies (on pull requests).

Click **Triggers** tab:
- **Uncheck:** Enable continuous integration

**Why disable CI?** We'll trigger this pipeline via branch policies later. If you leave CI enabled, it runs on every commit to `main`, which we don't want.

### Save the Pipeline

Click **Save** (not Save & Queue). Name it: `Terraform Status Check`

## Pipeline 2: Terraform Plan

This pipeline runs when code is **merged to main**. It creates a deployment artifact (the `.tfplan` file).

### Clone the Status Check Pipeline

Instead of creating from scratch, clone what we just built:

1. Go to **Pipelines > Pipelines**
2. Find: `Terraform Status Check`
3. Click the **...** menu
4. Click **Clone**
5. Rename to: `Terraform Plan (Create Artifact)`

### Modify Tasks

The first 4 tasks are identical (Install Terraform, Download Secrets, Init, Validate). Leave them alone.

#### Change Task 5: Terraform Plan (Save Output)

Edit the **Terraform Plan** task and update the script:

```bash
terraform plan \
  -input=false \
  -out=tfplan \
  -var="subscription_id=$(subscription-id)" \
  -var="spn_client_id=$(sp-terraform-devops-client-id)" \
  -var="spn_client_secret=$(sp-terraform-devops-client-secret)" \
  -var="spn_tenant_id=$(sp-terraform-devops-tenant-id)"
```

**What changed?** Added `-out=tfplan` which saves the plan to a binary file.

**Why?** This file contains the exact changes Terraform will make. We'll deploy THIS file (not re-run the plan later).

#### Add Task 6: Archive Files

We need to package the `.tfplan` file (and all Terraform files) into a single archive.

Search for "Archive files" and add the task.

**Settings:**
- **Display name:** `Archive Terraform Plan`
- **Root folder or file to archive:** `$(System.DefaultWorkingDirectory)/terraform`
- **Archive type:** `tar` (with gzip compression)
- **Tar compression:** `gz`
- **Archive file to create:** `$(Build.ArtifactStagingDirectory)/$(Build.BuildId)-tfplan.tar.gz`

**What this does:**
- Takes the entire `/terraform` folder (including `tfplan` file)
- Compresses it into a `.tar.gz` archive
- Saves it to the artifact staging directory
- Names it with the build ID (e.g., `123-tfplan.tar.gz`)

**Why archive the whole folder?** The `.tfplan` file references other Terraform files. We need everything together for `terraform apply` to work.

#### Add Task 7: Publish Pipeline Artifact

Now publish the archive so the release pipeline can download it.

Search for "Publish Pipeline Artifact" and add the task.

**Settings:**
- **Display name:** `Publish Terraform Artifact`
- **File or directory path:** `$(Build.ArtifactStagingDirectory)`
- **Artifact name:** `$(Build.BuildId)-tfplan`
- **Artifact publish location:** `Azure Pipelines`

**What this does:**
- Takes the archived file from the staging directory
- Publishes it as a pipeline artifact
- Names it with the build ID for tracking
- Makes it available to release pipelines

### Configure Trigger

Unlike the status check pipeline, this one SHOULD run on commits to `main`.

Click **Triggers** tab:
- **Check:** Enable continuous integration
- **Branch filters:**
  - **Include:** `main`
- **Path filters (optional):**
  - **Include:** `terraform/*` (only trigger if Terraform code changes)

**Why path filter?** If someone updates the README or other files outside `/terraform`, there's no point running this pipeline.

### Save the Pipeline

Click **Save**.

## Test the Status Check Pipeline

Before we set up pull requests, let's manually test the status check pipeline.

### Create a Test Branch

```bash
git checkout -b test-status-check
```

### Add a Simple Terraform File

Create `terraform/test.tf`:

```hcl
resource "azurerm_resource_group" "test" {
  name     = "rsg-pipeline-test-001"
  location = "northeurope"
}
```

### Commit and Push

```bash
git add terraform/test.tf
git commit -m "Test status check pipeline"
git push origin test-status-check
```

### Manually Run the Pipeline

Since we disabled CI, manually queue it:

1. Go to **Pipelines > Pipelines**
2. Click **Terraform Status Check**
3. Click **Run pipeline**
4. Select branch: `test-status-check`
5. Click **Run**

### Watch the Pipeline

Click into the running pipeline and watch each task:

1. **Install Terraform** - Downloads Terraform 1.5.7
2. **Download secrets** - Retrieves Key Vault secrets (values masked in logs)
3. **Terraform Init** - Connects to remote backend, downloads state
4. **Terraform Validate** - Syntax check (should pass)
5. **Terraform Plan** - Shows plan output: `Plan: 1 to add, 0 to change, 0 to destroy`

**Success?** Great! Your status check pipeline works.

**Failed?** Common issues:
- **Key Vault access denied** - Service principal doesn't have Get/List permissions
- **Backend initialization failed** - Storage account key is wrong or Key Vault secret name doesn't match
- **Provider authentication failed** - Service principal credentials are incorrect

## Test the Plan Pipeline

Now test the pipeline that creates artifacts.

### Merge to Main

```bash
git checkout main
git merge test-status-check
git push origin main
```

This triggers the **Terraform Plan** pipeline automatically (because we enabled CI on `main`).

### Watch the Pipeline

1. Go to **Pipelines > Pipelines**
2. The **Terraform Plan** pipeline should be running
3. Click into it

Watch the tasks run:
1. Install, Download, Init, Validate, Plan (same as before)
2. **Archive Terraform Plan** - Creates `123-tfplan.tar.gz`
3. **Publish Terraform Artifact** - Uploads artifact

### Verify the Artifact

After the pipeline completes:

1. Click **1 published** (near the top of the pipeline run)
2. You should see: `123-tfplan` (or whatever build number ran)
3. Click **Download artifact**
4. Extract the `.tar.gz` file
5. You should see all files from `/terraform` folder, including `tfplan`

**Success?** Your plan pipeline is creating artifacts correctly.

## Common Issues & Fixes

### Issue: "Backend initialization failed: storage account not found"

**Cause:** Storage account name in `backend.tf` doesn't match your actual storage account.

**Fix:** Update `backend.tf` with the correct name.

### Issue: "Key Vault access denied"

**Cause:** Service principal doesn't have permissions on Key Vault.

**Fix:**
```powershell
$keyVaultName = "kv-tfstate-1234"
$spObjectId = "YOUR-SP-OBJECT-ID"

Set-AzKeyVaultAccessPolicy -VaultName $keyVaultName -ObjectId $spObjectId -PermissionsToSecrets Get,List
```

### Issue: "Secret not found in variable group"

**Cause:** The secret name in your pipeline script doesn't match the Key Vault secret name.

**Fix:** Check spelling. Secret names are case-sensitive in Linux agents.

**Example:** If Key Vault has `sp-terraform-devops-client-id`, your script must use exactly that:
```bash
-var="spn_client_id=$(sp-terraform-devops-client-id)"
```

### Issue: "Terraform plan shows unwanted changes"

**Cause:** Someone manually changed infrastructure in the portal (or another pipeline).

**Fix:** Either:
1. Revert the manual change in the portal
2. Update your Terraform code to match current state
3. Run `terraform refresh` and commit the updated state (advanced)

### Issue: "Archive task failed: no files found"

**Cause:** The `tfplan` file wasn't created because `terraform plan` failed.

**Fix:** Check the Terraform Plan task logs. Fix any errors there first.

### Issue: Pipeline runs but plan shows no changes

**Cause:** Your test resource already exists in Azure (from a previous run).

**Fix:** Either:
1. Delete the resource group manually
2. Change the resource name in your Terraform code
3. This is actually fine - it proves state management is working!

## Variable Reference Table

Here's every variable you need to configure (copy this for reference):

| Variable Name | Source | Used In | Example Value |
|--------------|---------|---------|---------------|
| `subscription-id` | Pipeline variable | Plan script | `12345678-1234-1234-1234-123456789012` |
| `sttfstate1234-key1` | Key Vault | Init script | `(secret from storage account)` |
| `sp-terraform-devops-client-id` | Key Vault | Plan script | `87654321-4321-4321-4321-210987654321` |
| `sp-terraform-devops-client-secret` | Key Vault | Plan script | `(secret from service principal)` |
| `sp-terraform-devops-tenant-id` | Key Vault | Plan script | `11111111-1111-1111-1111-111111111111` |

**Replace these with YOUR values** from Part 1.

## What We Built

You now have two working build pipelines:

**Terraform Status Check:**
- Triggers: Manual (via branch policy later)
- Actions: Validate syntax, show plan
- Output: Console logs only
- Duration: ~30-60 seconds

**Terraform Plan:**
- Triggers: Commits to `main` branch
- Actions: Validate, plan, archive, publish
- Output: Build artifact (`.tfplan` file)
- Duration: ~60-90 seconds

**What's missing?** We haven't set up:
- Branch policies (force PRs)
- Pull request automation
- Release pipeline (actual deployment)
- Approval gates

That's all coming in Parts 3 and 4.

## Key Takeaways

1. **Status check pipelines run fast** - No artifact creation = faster feedback
2. **Plan pipelines save artifacts** - The `.tfplan` file preserves intent
3. **Key Vault integration is seamless** - Secrets injected at runtime, never logged
4. **Classic GUI pipelines are easier** - Visual debugging, clear task ordering
5. **Path filters prevent wasted builds** - Only run when Terraform code changes

The foundation is solid. Now we build the release pipeline and wire up pull requests.

---

**Next:** [Part 3 - Release Pipeline & Approval Gates](/blog/terraform-azure-devops-cicd-part3-release-pipeline/)

*All code and pipeline configurations from this series are available in my [GitHub repo](https://github.com/dswann101164).*
