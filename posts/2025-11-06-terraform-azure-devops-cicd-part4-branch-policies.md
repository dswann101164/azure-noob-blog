---
title: "Terraform + Azure DevOps CI/CD: Part 4 - Branch Policies & Pull Request Automation"
date: 2025-11-06
summary: "Enforce GitOps workflow with branch policies that require reviews, trigger automated validation, and prevent direct commits to main. No cowboy deployments allowed."
tags: ["azure", "Terraform", "devops", "CICD", "IaC", "Azure DevOps", "GitOps"]
cover: "static/images/hero/terraform-devops-part4.png"
hub: ai
---
We've built the pipelines (Parts 1-3). Now we enforce the workflow with **branch policies** that make it impossible to bypass reviews and automated validation.


This guide is part of our [AI-Assisted Azure Operations hub](/hub/ai/) exploring how AI tools transform cloud administration and productivity workflows.

**What we're enforcing:**
- ❌ No direct commits to `main` branch
- ✅ All changes through pull requests
- ✅ Automated status checks required
- ✅ Human review required
- ✅ Auto-delete feature branches after merge

This is what separates hobby projects from enterprise infrastructure.

## Why Branch Policies Matter

Without branch policies, someone can:
1. Write bad Terraform code
2. Commit directly to `main`
3. Auto-deploy broken infrastructure
4. Blame "the process" when things break

**With branch policies:**
1. Write Terraform code in a feature branch
2. Create pull request (triggers validation)
3. Status checks run: validate + plan
4. Another human reviews the plan
5. Both pass → merge allowed
6. Build and release pipelines take over

**The result:** Every infrastructure change has two reviews (automated + human) before deployment.

## Configure Branch Policies for Main Branch

### Step 1: Navigate to Branch Policies

1. Go to **Repos > Branches**
2. Find the `main` branch
3. Click the **...** menu
4. Click **Branch policies**

### Step 2: Require Pull Requests

**Require a minimum number of reviewers:**
- Toggle on: **Require a minimum number of reviewers**
- **Minimum number of reviewers:** `1`
- Check: **Requester cannot approve their own changes** (if you have a team)
- Check: **Prohibit the most recent pusher from approving their own changes**
- **When new changes are pushed:**
  - Select: **Reset all approval votes (does not reset votes to reject or wait)**

**What this does:**
- Nobody (including you) can merge without approval
- If you push new commits to the PR, approvals reset (forces re-review)
- Author can't approve their own work (if multiple team members)

**Single-person team?** Set minimum reviewers to `1` and uncheck "requester cannot approve." You'll still review your own plans (good practice).

### Step 3: Check for Linked Work Items (Optional)

If you use Azure Boards for work tracking:

**Check for linked work items:**
- Toggle on: **Check for linked work items**
- Select: **Required** (or **Optional** if you don't always have work items)

**What this does:** Forces PRs to link to a user story or task. Good for traceability.

**Don't use Boards?** Skip this.

### Step 4: Require Comment Resolution

**Check for comment resolution:**
- Toggle on: **Check for comment resolution**
- Select: **Required** (all comments must be resolved or marked "Won't Fix")

**What this does:** Prevents merging if there are unresolved discussion threads.

**Example:** Reviewer comments "Why are we using westeurope instead of northeurope?" - Must be answered before merge.

### Step 5: Limit Merge Types

**Limit merge types:**
- Toggle on: **Limit merge types**
- Check: **Squash merge** only
- Uncheck: Basic merge, Rebase merge, Rebase and fast-forward

**What this does:** Enforces clean Git history. All commits in a PR get squashed into one commit on `main`.

**Why?** Your `main` branch history reads like: 
- "Add demo resource group"
- "Update network security group rules"
- "Add Azure SQL database"

Not: 
- "WIP"
- "Fix typo"
- "Fix typo again"
- "Undo last fix"

Clean history = easier rollbacks.

### Step 6: Build Validation (Status Check Pipeline)

This is the **critical automation**. Status checks run automatically on every PR.

**Build validation:**
- Click **+ Add build policy**

**Settings:**
- **Build pipeline:** `Terraform Status Check (Validate + Plan)`
- **Trigger:** `Automatic`
- **Policy requirement:** `Required`
- **Build expiration:** `Immediately when main is updated`
- **Display name:** `Terraform Validation`

**What this does:**
- Creates or updates a PR → Status check pipeline triggers
- Pipeline runs validate + plan
- Must succeed before merge is allowed
- If someone commits to `main` while your PR is open, your PR re-runs validation (ensures no conflicts)

**Click Save**.

### Step 7: Automatically Include Reviewers (Optional)

Useful for teams with designated approvers.

**Automatically include code reviewers:**
- Click **+ Add automatic reviewers**

**Settings:**
- **Reviewers:** Add specific people or groups
- **For changes to:** `**/*.tf` (only when Terraform files change)
- **Reviewers:** Required

**Example use case:** Your security team must review any changes to network security groups or Key Vault access policies.

**Single-person team?** Skip this.

### Step 8: Save All Policies

Click **Save changes** at the bottom.

## Test Branch Policies (Intentional Failure)

Let's test that the policies actually prevent bad code from merging.

### Step 1: Create a Feature Branch with Bad Terraform

```bash
git checkout main
git pull
git checkout -b test-branch-policies
```

Create `terraform/test-bad.tf` with **intentionally invalid syntax**:

```hcl
# Missing equals sign (syntax error)
resource "azurerm_resource_group" "bad" {
  name "rsg-test-bad"  # <-- WRONG
  location = "northeurope"
}
```

Commit and push:

```bash
git add terraform/test-bad.tf
git commit -m "Test branch policies with invalid syntax"
git push origin test-branch-policies
```

### Step 2: Create Pull Request

1. Go to **Repos > Pull requests**
2. Click **New pull request**
3. **Source:** `test-branch-policies`
4. **Target:** `main`
5. Click **Create**

### Step 3: Watch Status Checks Fail

Within seconds, you'll see:
- ❌ **Terraform Validation** - Failed

Click the **Checks** tab (or **Status checks**) to see details.

You'll see the error:
```
Error: Invalid argument
  on test-bad.tf line 3, in resource "azurerm_resource_group" "bad":
  3:   name "rsg-test-bad"
  
Argument name requires a value, but no value was supplied.
```

### Step 4: Try to Complete the PR

Click **Complete** (top right).

You'll see: **Cannot complete because status checks must succeed**

**The merge button is disabled.** Branch policies are working!

### Step 5: Fix the Code

```bash
git checkout test-branch-policies
```

Edit `terraform/test-bad.tf` to fix the syntax:

```hcl
resource "azurerm_resource_group" "bad" {
  name     = "rsg-test-bad"  # Fixed
  location = "northeurope"
}
```

Commit and push:

```bash
git add terraform/test-bad.tf
git commit -m "Fix syntax error"
git push
```

### Step 6: Watch Status Checks Pass

The PR page auto-updates. Within a minute:
- ✅ **Terraform Validation** - Succeeded

Now the **Complete** button is enabled.

### Step 7: Clean Up

Don't merge this test PR. Instead:
1. Click **Abandon** (dropdown next to Complete)
2. Delete the branch: `git branch -D test-branch-policies`

**Lesson learned:** Branch policies enforce quality. Bad code can't merge.

## Customize Status Check Comments (Optional)

Want Terraform plan output posted as PR comments? Use the Azure Pipelines extension API.

### Add a Script Task to Status Check Pipeline

Edit your **Terraform Status Check** pipeline.

After the `Terraform Plan` task, add a **PowerShell** task:

**Settings:**
- **Display name:** `Post Plan to PR`
- **Type:** Inline
- **Script:**

```powershell
# Capture plan output
$planOutput = terraform plan -input=false -no-color

# Post to PR using REST API
$uri = "$($env:SYSTEM_TEAMFOUNDATIONCOLLECTIONURI)$($env:SYSTEM_TEAMPROJECT)/_apis/git/repositories/$($env:BUILD_REPOSITORY_ID)/pullRequests/$($env:SYSTEM_PULLREQUEST_PULLREQUESTID)/threads?api-version=6.0"

$body = @{
    comments = @(
        @{
            parentCommentId = 0
            content = "## Terraform Plan Output```terraform`n$planOutput`n```"
            commentType = 1
        }
    )
    status = 1
} | ConvertTo-Json -Depth 10

$headers = @{
    Authorization = "Bearer $($env:SYSTEM_ACCESSTOKEN)"
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Uri $uri -Method Post -Body $body -Headers $headers
```

**Environment variables:**
- Add a variable: `SYSTEM_ACCESSTOKEN` = `$(System.AccessToken)`
- Check: **Allow scripts to access the OAuth token** (in agent job settings)

**What this does:** Posts the Terraform plan output directly as a PR comment.

**Warning:** This exposes plan output in PR comments. If your state includes sensitive data, skip this step.

## Workflow Walkthrough (Full Cycle)

Here's what the complete workflow looks like with branch policies enforced.

### Day 1: Create Feature Branch

```bash
git checkout main
git pull
git checkout -b feature/add-storage-account
```

### Day 2: Write Terraform Code

```hcl
# storage.tf
resource "azurerm_resource_group" "storage" {
  name     = "rsg-storage-001"
  location = "northeurope"
}

resource "azurerm_storage_account" "demo" {
  name                     = "stdemostorage${random_integer.suffix.result}"
  resource_group_name      = azurerm_resource_group.storage.name
  location                 = azurerm_resource_group.storage.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  
  tags = {
    Environment = "Development"
    ManagedBy   = "Terraform"
  }
}

resource "random_integer" "suffix" {
  min = 1000
  max = 9999
}
```

Commit locally (but don't push yet):

```bash
git add terraform/storage.tf
git commit -m "Add storage account for demo"
```

### Day 3: Test Locally (Optional)

```bash
cd terraform
terraform init
terraform plan
```

Review plan output. Looks good? Push:

```bash
git push origin feature/add-storage-account
```

### Day 4: Create Pull Request

1. Go to **Repos > Pull requests**
2. Azure DevOps automatically shows: "Create a pull request for feature/add-storage-account"
3. Click **Create a pull request**
4. **Title:** "Add storage account for demo"
5. **Description:**
   ```
   ## What
   - Adds resource group for storage
   - Adds storage account with LRS replication
   
   ## Why
   - Needed for demo data storage
   
   ## Testing
   - Ran terraform plan locally
   - Verified naming conventions
   ```
6. **Reviewers:** Add your teammate (or yourself if solo)
7. Click **Create**

### Day 5: Automated Validation Runs

Within seconds:
- ⏳ **Terraform Validation** - Running

After ~30-60 seconds:
- ✅ **Terraform Validation** - Succeeded

Click **Checks** to see plan output:
```
Terraform will perform the following actions:

  # azurerm_resource_group.storage will be created
  + resource "azurerm_resource_group" "storage" {
      + name     = "rsg-storage-001"
      + location = "northeurope"
    }

  # azurerm_storage_account.demo will be created
  + resource "azurerm_storage_account" "demo" {
      + name                     = "stdemostorage1234"
      + resource_group_name      = "rsg-storage-001"
      + location                 = "northeurope"
      + account_tier             = "Standard"
      + account_replication_type = "LRS"
    }

Plan: 2 to add, 0 to change, 0 to destroy.
```

### Day 6: Human Review

Your teammate (or you) reviews:
1. **Files** tab - Review code changes
2. **Checks** tab - Review plan output
3. **Commits** tab - Verify clean commit messages

Looks good. Click **Approve** (top right).

### Day 7: Merge to Main

1. Click **Complete** (now enabled because status checks passed and review approved)
2. **Merge type:** Squash commit (only option, enforced by policy)
3. **Merge commit message:** Keep the PR title
4. Check: **Delete feature/add-storage-account after merge** (automatically checked)
5. Click **Complete merge**

### Day 8: Automated Deployment

Immediately after merge:
1. **Build pipeline** (`Terraform Plan`) triggers
   - Runs validate, plan, archives artifact
   - Publishes artifact: `456-tfplan`
2. **Release pipeline** queues
   - Sends approval email
   - Waits for approval
3. You approve the release
4. **Release pipeline** deploys
   - Runs terraform apply with the artifact
   - Creates resource group + storage account
   - Sends success notification

### Day 9: Verify in Azure

```powershell
Get-AzResourceGroup -Name "rsg-storage-001"
Get-AzStorageAccount -ResourceGroupName "rsg-storage-001"
```

Both exist. Success!

## Advanced: Multiple Reviewers for Critical Changes

For high-risk changes (networking, security, production), require multiple approvers.

### Create a Code Owners File

Create `/.azuredevops/CODEOWNERS` in your repo:

```
# Default owner for everything
* @your-username

# Networking changes require network team approval
/terraform/networking/** @network-team

# Security policies require security team approval
/terraform/policies/** @security-team

# Production environment requires both infra and security
/terraform/production/** @infra-team @security-team
```

Commit to `main`:

```bash
git add .azuredevops/CODEOWNERS
git commit -m "Add code owners for critical paths"
git push
```

### Update Branch Policy

1. Go to **Repos > Branches > main > Branch policies**
2. **Automatically include code reviewers:**
   - Check: **Enable code owners**
3. Save

**What this does:**
- PRs that change networking code automatically add the network team as required reviewers
- PRs that touch production require BOTH infrastructure and security team approval
- Can't merge until all code owners approve

## Handling Urgent Changes

What if you need to bypass policies for an emergency hotfix?

### Option 1: Use Policy Override (Admin Only)

Azure DevOps admins can override branch policies.

1. Create PR as normal
2. Click **Complete**
3. If you have admin permissions, you'll see: **Override branch policies**
4. Check the box
5. **Reason:** "Emergency hotfix for production outage - approved by [Name]"
6. Complete merge

**Audit:** The override is logged. Use sparingly and document why.

### Option 2: Create an Emergency Bypass Branch

For planned maintenance windows or emergency processes:

1. Create a branch policy exception for `hotfix/*` branches
2. These branches can merge with reduced requirements (but still require one approval)

**Configure:**
1. Go to **Repos > Branches**
2. Find **Branch policies** for `main`
3. **Override branch policies** section
4. Click **Add exception**
5. Branch name pattern: `refs/heads/hotfix/*`
6. Allowed overrides: Check **Require minimum reviewers (1 instead of standard 2)**

## Common Issues & Fixes

### Issue: Can't push to main after setting policies

**Cause:** Branch policies block direct pushes to `main`.

**Fix:** This is intentional. Always work in feature branches:
```bash
git checkout -b feature/my-change
# make changes
git push origin feature/my-change
# create PR
```

### Issue: Status check runs forever (never completes)

**Cause:** Build validation policy has a stuck pipeline.

**Fix:**
1. Go to **Pipelines > Pipelines**
2. Find the stuck `Terraform Status Check` run
3. Click **Cancel**
4. Go back to the PR - it should retry

### Issue: "Squash commit" option is grayed out

**Cause:** Branch policy requires squash merge, but the option is disabled.

**Fix:**
1. Go to **Project Settings > Repositories > your repo**
2. Click **Policies** tab
3. Check: **Squash merge** is allowed

### Issue: PR shows "No changes" after pushing commits

**Cause:** The commits were force-pushed or rebased incorrectly.

**Fix:**
```bash
# Reset your branch to match main
git fetch origin
git checkout your-feature-branch
git reset --hard origin/main

# Re-apply your changes (copy them first!)
# Then commit and push
git push origin your-feature-branch --force
```

### Issue: Status check fails with "Unable to access Key Vault"

**Cause:** Service principal doesn't have permissions on Key Vault.

**Fix:**
```powershell
$keyVaultName = "kv-tfstate-1234"
$spObjectId = "YOUR-SP-OBJECT-ID"

Set-AzKeyVaultAccessPolicy -VaultName $keyVaultName -ObjectId $spObjectId -PermissionsToSecrets Get,List
```

## Branch Policies Checklist

Copy this checklist for new repos:

- [ ] **Require pull requests** (minimum 1 reviewer)
- [ ] **Require comment resolution** (all discussions resolved)
- [ ] **Limit merge types** (squash commit only)
- [ ] **Build validation** (status check pipeline)
- [ ] **Automatically delete feature branches** (on merge completion)
- [ ] **Check for linked work items** (if using Azure Boards)
- [ ] **Automatically include reviewers** (for critical paths)
- [ ] **Code owners file** (for team-based approval)

## Key Takeaways

1. **Branch policies enforce GitOps workflow** - No bypassing the process
2. **Status checks run automatically** - Fast feedback on code quality
3. **Human + automated review** - Two layers of defense
4. **Clean Git history** - Squash merge keeps `main` readable
5. **Emergency overrides exist** - But are logged and auditable

You now have a fully automated, policy-enforced infrastructure deployment workflow. 

---

**Next:** [Part 5 - Production Best Practices & Multi-Environment Setup](/blog/terraform-azure-devops-cicd-part5-production-best-practices/)

*All code and pipeline configurations from this series are available in my [GitHub repo](https://github.com/dswann101164).*
