---
title: "Terraform + Azure DevOps CI/CD: Part 3 - Release Pipeline & Approval Gates"
date: 2025-11-05
summary: "Build the release pipeline that deploys approved Terraform plans with pre-deployment approval gates and audit trails. This is where governance happens."
tags: ["azure", "Terraform", "devops", "CICD", "IaC", "Azure DevOps"]
cover: "static/images/hero/terraform-devops-part3.png"
---

Parts 1 and 2 built the pipelines that validate code and create artifacts. Now we build the pipeline that actually **deploys infrastructure** - with approval gates that prevent unauthorized changes.

**What we're building:**
- Release pipeline that triggers on new plan artifacts
- Pre-deployment approval gate (human review required)
- Terraform apply using the approved plan file
- Post-deployment notifications

## Why Release Pipelines (Not Build Pipelines)

**Build pipelines** create artifacts. **Release pipelines** deploy them.

Key difference: Release pipelines support **approval gates**. You can't click "Deploy" until someone approves it.

**The workflow:**
1. Code merges to `main` → Build pipeline creates `.tfplan` artifact
2. Artifact published → Release pipeline **queued** (not started)
3. **Approval gate** → Someone reviews and approves
4. Terraform apply runs → Infrastructure deployed

**This ensures:** What gets approved in the PR is what gets deployed. No surprises.

## Create the Release Pipeline

Release pipelines use a different interface than build pipelines. They're older but more powerful for deployment workflows.

### Step 1: Navigate to Releases

1. Go to **Pipelines > Releases**
2. Click **New pipeline**
3. Select template: **Empty job** (ignore other templates)

### Step 2: Configure the Artifact Source

Click **Add an artifact** (big red box).

**Settings:**
- **Source type:** Build
- **Project:** Your Azure DevOps project
- **Source (build pipeline):** `Terraform Plan (Create Artifact)`
- **Default version:** Latest
- **Source alias:** `_Terraform Plan (Create Artifact)` (auto-generated)

Click **Add**.

**What this does:** Links this release pipeline to the build pipeline. Every time a new artifact is published, this release pipeline can trigger.

### Step 3: Enable Continuous Deployment Trigger

Click the **lightning bolt icon** on the artifact box.

Toggle on: **Continuous deployment trigger**

**Branch filters:**
- Click **+ Add**
- Type: `Include`
- Branch: `main`

Click **Save** (but don't close the trigger pane yet).

**What this does:** Automatically creates a new release whenever the build pipeline publishes an artifact from `main` branch.

**Why filter by branch?** If you later create feature branches with build artifacts (for testing), you don't want them auto-deploying.

### Step 4: Rename the Stage

The default stage name is "Stage 1". Let's fix that.

Click **Stage 1** and rename to: `Deploy Infrastructure`

**Stages** in release pipelines are deployment targets. You might have `Dev`, `Test`, `Prod`. We're starting with one stage.

### Step 5: Configure Pre-Deployment Approval

This is the **critical governance control**. Nobody can deploy infrastructure without approval.

Click the **lightning bolt with person icon** on the left side of `Deploy Infrastructure` stage.

**Pre-deployment approvals:**
- Toggle on: **Pre-deployment approvals**
- **Approvers:** Add yourself and any other authorized deployers
- **Timeout:** 7 days (max time to wait for approval before auto-rejecting)
- **Approval policies:**
  - Check: **Approvers receive an email notification**
  - Uncheck: **The user requesting a release should not approve it** (optional, but good for separation of duties)

Click **Save**.

**What this does:** 
- When a release is created, it immediately queues
- An email is sent to approvers: "Release X is waiting for approval"
- Release STOPS and waits
- Only after approval does it proceed to deployment tasks

### Step 6: Configure Agent Job

Click **1 job, 0 task** inside the `Deploy Infrastructure` stage.

**Agent job settings:**
- **Display name:** `Terraform Apply`
- **Agent pool:** `Azure Pipelines`
- **Agent Specification:** `ubuntu-latest`

Click **Save**.

## Add Release Pipeline Tasks

Now we add the actual deployment tasks. These are similar to the build pipeline, but with a critical difference: we use the **artifact** (not the current Git repo).

### Task 1: Download Pipeline Artifact

We need to download the `.tfplan` artifact from the build pipeline.

Click the **+** button on `Terraform Apply` job.

Search for "Download Pipeline Artifact" and add it.

**Settings:**
- **Display name:** `Download Terraform Artifact`
- **Download artifacts produced by:** `Current build`
- **Matching patterns:** `**/*` (all files)
- **Destination directory:** `$(System.DefaultWorkingDirectory)`

**What this does:** Downloads the entire artifact (the `.tar.gz` file containing Terraform code and the plan file).

### Task 2: Extract Archive

The artifact is compressed. We need to extract it.

Add a **Command Line** task.

**Settings:**
- **Display name:** `Extract Terraform Artifact`
- **Script:**

```bash
cd $(System.DefaultWorkingDirectory)
tar -xzf *-tfplan.tar.gz -C $(System.DefaultWorkingDirectory)/terraform
```

**What this does:**
- Finds the `.tar.gz` file (named with build ID)
- Extracts it to `/terraform` folder
- Now we have all Terraform files + the `tfplan` file

**Why wildcard `*-tfplan.tar.gz`?** The build ID changes. This pattern matches any build.

### Task 3: Install Terraform

Same as in build pipelines - ensures correct version.

Add the **Terraform installer** task.

**Settings:**
- **Display name:** `Install Terraform 1.5.7`
- **Version:** `1.5.7`

### Task 4: Download Key Vault Secrets

We need storage account keys and service principal credentials.

Add the **Azure Key Vault** task.

**Settings:**
- **Display name:** `Download secrets from Key Vault`
- **Azure subscription:** `terraform-azure-connection`
- **Key vault:** `kv-tfstate-1234` (your Key Vault name)
- **Secrets filter:** `*`

### Task 5: Terraform Init

We need to initialize Terraform in the release environment (even though we did it in the build pipeline).

Add a **Command Line** task.

**Settings:**
- **Display name:** `Terraform Init`
- **Script:**

```bash
terraform init \
  -backend-config="access_key=$(sttfstate1234-key1)"
```

**Advanced > Working Directory:** `$(System.DefaultWorkingDirectory)/terraform`

**Why init again?** The release agent is a clean environment. It doesn't have the `.terraform` directory from the build pipeline.

### Task 6: Terraform Apply

**This is the deployment task.** It applies the approved plan.

Add a **Command Line** task.

**Settings:**
- **Display name:** `Terraform Apply (Approved Plan)`
- **Script:**

```bash
terraform apply \
  -auto-approve \
  -input=false \
  tfplan
```

**Advanced > Working Directory:** `$(System.DefaultWorkingDirectory)/terraform`

**Critical flags:**
- `-auto-approve` - Don't prompt for confirmation (we already approved the release)
- `-input=false` - No interactive prompts
- `tfplan` - Apply the EXACT plan file from the artifact (not a new plan)

**This is why the workflow is secure:**
1. PR reviewer sees the plan output
2. PR gets approved and merged
3. Build pipeline creates artifact with that EXACT plan
4. Release approver reviews again
5. Terraform applies that EXACT plan

No drift. What was reviewed is what deploys.

### Task 7: Clean Up Plan File (Optional Security)

After deployment, delete the plan file (it contains sensitive info).

Add a **Command Line** task.

**Settings:**
- **Display name:** `Delete Plan File`
- **Script:**

```bash
rm -f tfplan
rm -f *-tfplan.tar.gz
```

**Why?** Plan files can contain sensitive data. Delete them after use.

### Link Variable Group

Click the **Variables** tab, then **Variable groups**.

Click **Link variable group** and select: `terraform-keyvault-secrets`

Add a regular variable:
- Name: `subscription-id`
- Value: Your subscription GUID

**Save** the pipeline.

## Configure Notifications (Optional)

Let's send emails when releases succeed or fail.

### Enable Email Notifications

1. Click the **pipeline name** at the top (to get to pipeline settings)
2. Click **Options** tab
3. Scroll to **Integrations**
4. Check: **Send email notifications**

**Recipients:**
- Add yourself
- Add your team
- Add any stakeholders

**When to send:**
- Check: **A deployment completes**
- Check: **A deployment fails**
- Check: **A deployment is pending approval**

Click **Save**.

## Test the Full Workflow (End-to-End)

Time to test the complete workflow: PR → Build → Release → Approval → Deploy.

### Step 1: Create a Feature Branch

```bash
git checkout main
git pull
git checkout -b add-resource-group
```

### Step 2: Add a New Resource

Create or edit `terraform/main.tf`:

```hcl
resource "azurerm_resource_group" "demo" {
  name     = "rsg-terraform-demo-001"
  location = "northeurope"
  
  tags = {
    Environment = "Test"
    ManagedBy   = "Terraform"
    Purpose     = "CI/CD Demo"
  }
}
```

### Step 3: Commit and Push

```bash
git add terraform/main.tf
git commit -m "Add demo resource group for testing"
git push origin add-resource-group
```

### Step 4: Create Pull Request

1. Go to **Repos > Pull requests**
2. Click **New pull request**
3. **Source branch:** `add-resource-group`
4. **Target branch:** `main`
5. **Title:** "Add demo resource group"
6. **Description:** "Testing full CI/CD pipeline with approval gates"
7. Click **Create**

**What happens next:**
- Status check pipeline should trigger automatically (if you set up branch policies in Part 4)
- Plan output appears in PR comments
- PR requires approval before merge

### Step 5: Review and Merge PR

1. Click the **Checks** tab (or **Status checks**)
2. Review the Terraform plan output
3. Verify it says: `Plan: 1 to add, 0 to change, 0 to destroy`
4. Click **Approve** (top right)
5. Click **Complete** (merge options)
6. Select: **Delete branch after merge** (clean up)
7. Click **Complete merge**

**What happens next:**
- Code merges to `main`
- Build pipeline (`Terraform Plan`) triggers automatically
- Build creates artifact and publishes it
- Release pipeline **queues** (but doesn't start)

### Step 6: Approve the Release

You should receive an email: "Release Release-1 is waiting for your approval."

1. Go to **Pipelines > Releases**
2. You should see a release in **In progress** state with a **pause icon**
3. Click into the release
4. You'll see: `Deploy Infrastructure` stage with **Approval pending**
5. Click **Approve** (or **Reject** if something looks wrong)
6. **Comments:** "Approved for testing - deploying demo resource group"
7. Click **Approve**

**What happens next:**
- Release pipeline starts running
- Tasks execute: Download artifact, extract, init, apply
- Terraform deploys the resource group
- You see: `Apply complete! Resources: 1 added, 0 changed, 0 destroyed`

### Step 7: Verify in Azure

```powershell
Get-AzResourceGroup -Name "rsg-terraform-demo-001"
```

You should see the resource group with your tags.

**Success!** Your full CI/CD pipeline works.

## The Complete Audit Trail

One of the best features of this setup is the **complete audit trail**. You can always answer:

### "Who deployed this resource?"

1. Go to **Pipelines > Releases**
2. Find the release
3. Check the **Approved by** field
4. Check the Git commit author

### "When was it deployed?"

1. Release pipeline shows start time and duration
2. Azure Activity Log shows exact deployment time
3. Git commit has timestamp

### "What exactly was deployed?"

1. Download the artifact from the build
2. Extract the `tfplan` file
3. Run: `terraform show tfplan` (requires Terraform installed locally)

Or just look at the Git diff in the merged PR.

### "Why was it deployed?"

1. Read the PR description
2. Read the PR comments and reviews
3. Read the release approval comments

**This satisfies audit requirements** for SOC 2, ISO 27001, and most compliance frameworks.

## Common Issues & Fixes

### Issue: Release doesn't trigger after build completes

**Cause:** Continuous deployment trigger is disabled or branch filter doesn't match.

**Fix:**
1. Go to release pipeline
2. Click the artifact lightning bolt
3. Verify: **Continuous deployment trigger** is ON
4. Verify: Branch filter includes `main`

### Issue: "Artifact not found" error

**Cause:** The artifact name doesn't match what the build pipeline published.

**Fix:**
1. Go to the build pipeline run
2. Check the **published artifact name** (should be something like `123-tfplan`)
3. Update the release pipeline download task to match

Or simplify by using `**/*` wildcard pattern.

### Issue: Terraform apply fails with "Invalid plan file"

**Cause:** The plan file is from a different state version, or the state changed between plan and apply.

**Fix:**
1. Check if someone manually deployed resources in the portal
2. Reject the release
3. Create a new PR to re-plan with current state
4. Re-approve and merge

**Prevention:** Don't allow manual Azure Portal changes. Enforce this policy.

### Issue: "Backend initialization failed" in release pipeline

**Cause:** Storage account key is missing or incorrect.

**Fix:**
1. Verify Key Vault has the storage account key
2. Verify variable group is linked to the release pipeline
3. Check the init task uses the correct variable: `$(sttfstate1234-key1)`

### Issue: Approval email not received

**Cause:** Notification settings not configured.

**Fix:**
1. Go to release pipeline **Options** tab
2. Verify **Send email notifications** is checked
3. Verify your email is in the recipients list
4. Check your spam folder

### Issue: Can't approve own release

**Cause:** You enabled the policy "The user requesting a release should not approve it."

**Fix:** Either:
1. Have someone else approve releases you create
2. Disable that policy (if you're a one-person team)

## Security Best Practices

### 1. Rotate Service Principal Secrets

Service principal secrets should rotate regularly (every 90-180 days).

**Rotation process:**
1. Create new secret for service principal in Azure AD
2. Update Key Vault with new secret
3. Test pipelines
4. Delete old secret

**Automation tip:** Use Azure Key Vault secret expiration notifications.

### 2. Limit Approval Permissions

Don't make everyone an approver. Only:
- Infrastructure leads
- Platform team leads
- Security team (for high-risk changes)

**How to add approvers:**
1. Go to release pipeline
2. Click pre-deployment approval settings
3. Add/remove approvers

### 3. Use Multiple Approval Gates for Production

For production deployments, add **two approval gates**:

**Gate 1: Technical Review**
- Approvers: Infrastructure team
- Purpose: Verify technical correctness

**Gate 2: Change Advisory Board (CAB)**
- Approvers: CAB members
- Purpose: Verify business justification and timing

**How to add:**
1. Create two stages in release pipeline: `Prod-Technical-Review` and `Prod-CAB-Approval`
2. Both have pre-deployment approvals
3. Second stage depends on first stage completing

### 4. Implement Deployment Windows

Only deploy during approved maintenance windows.

**How:**
1. Use **scheduled releases** (release pipeline option)
2. Set allowed hours: e.g., Saturday 2 AM - 6 AM
3. Auto-reject releases outside the window

### 5. Archive Release Logs

Keep release logs for at least 1 year (compliance requirement).

**Azure DevOps retains:**
- Build logs: 30 days (default)
- Release logs: 30 days (default)

**Extend retention:**
1. Go to **Project Settings > Pipelines > Retention**
2. Set: **Days to keep releases** = 365

## What We've Built

You now have a **production-ready release pipeline** with:

✅ **Automated artifact deployment** - No manual Terraform commands  
✅ **Human approval gates** - No surprise deployments  
✅ **Email notifications** - Stay informed  
✅ **Audit trails** - Full history of approvals and deployments  
✅ **Consistency** - Approved plan is exactly what deploys  
✅ **Security** - Secrets from Key Vault, plan files cleaned up  

## Key Takeaways

1. **Release pipelines handle deployment** - Build pipelines create artifacts
2. **Approval gates prevent unauthorized changes** - Human review required
3. **Artifacts preserve intent** - No drift between plan and apply
4. **Notifications keep teams informed** - Email on approval, success, failure
5. **Audit trails satisfy compliance** - Who, what, when, why all documented

Next, we wire up pull request automation and branch policies to enforce this workflow.

---

**Next:** [Part 4 - Branch Policies & Pull Request Automation](/blog/terraform-azure-devops-cicd-part4-branch-policies/)

*All code and pipeline configurations from this series are available in my [GitHub repo](https://github.com/dswann101164).*
