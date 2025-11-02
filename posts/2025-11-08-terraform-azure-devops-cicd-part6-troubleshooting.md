---
title: "Terraform + Azure DevOps CI/CD: Part 6 - Troubleshooting & Common Production Issues"
date: 2025-11-08
summary: "Real-world troubleshooting guide for Terraform CI/CD pipelines. These are the issues I've actually encountered in production - and how to fix them fast."
tags: ["Azure", "Terraform", "DevOps", "CICD", "IaC", "Troubleshooting"]
cover: "static/images/hero/terraform-devops-part6.png"
---

This is the guide I wish I had when I started running Terraform in production. These aren't hypothetical problems - these are **real issues I've encountered** with proven solutions.

**What's covered:**
- 🔥 Pipeline failures and error codes
- 🔒 Authentication and permission issues
- 💾 State file corruption and locking
- 🏗️ Resource drift and manual changes
- ⚡ Performance optimization
- 📊 Debugging strategies

Skip to the section that matches your current fire.

## Quick Diagnostic Checklist

Before diving into specific issues, run this diagnostic checklist:

### Is the Pipeline Healthy?

```bash
# Check if Terraform is installed correctly
terraform version

# Check Azure CLI authentication
az account show

# Check service principal credentials
az login --service-principal \
  --username $CLIENT_ID \
  --password $CLIENT_SECRET \
  --tenant $TENANT_ID

# Check Key Vault access
az keyvault secret show --vault-name kv-tfstate-1234 --name sttfstate1234-key1

# Check storage account access
az storage blob list \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --account-key $STORAGE_KEY
```

### Are There Stuck Locks?

```bash
# Check for state locks
az storage blob show \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --name prod/terraform.tfstate \
  --query "metadata.lock_id"
```

### Is There Drift?

```bash
# Compare state vs. actual Azure resources
terraform plan -detailed-exitcode
# Exit code 0 = no changes
# Exit code 1 = error
# Exit code 2 = changes detected (drift)
```

## Authentication Issues

### Error: "Failed to get credentials from Key Vault"

**Symptoms:**
```
Error: Failed to retrieve secret 'sttfstate1234-key1' from vault 'kv-tfstate-1234'
Status Code: 403
Error Code: Forbidden
```

**Cause:** Service principal doesn't have Get/List permissions on Key Vault.

**Solution:**
```powershell
$keyVaultName = "kv-tfstate-1234"
$spObjectId = "YOUR-SERVICE-PRINCIPAL-OBJECT-ID"

# Grant Get and List on secrets
Set-AzKeyVaultAccessPolicy `
  -VaultName $keyVaultName `
  -ObjectId $spObjectId `
  -PermissionsToSecrets Get,List

# Verify
Get-AzKeyVaultAccessPolicy -VaultName $keyVaultName | Where-Object { $_.ObjectId -eq $spObjectId }
```

**Prevention:** Create a script that validates service principal permissions before pipeline runs.

### Error: "The service principal does not have permission to perform action"

**Symptoms:**
```
Error: authorization.RoleAssignmentsClient#Create: Failure responding to request
StatusCode=403
Code="AuthorizationFailed"
Message="The client 'abc-123' does not have authorization to perform action 'Microsoft.Authorization/roleAssignments/write'"
```

**Cause:** Service principal has Contributor but needs User Access Administrator for role assignments.

**Solution:**
```powershell
$spId = "YOUR-SP-OBJECT-ID"
$subscriptionId = "YOUR-SUBSCRIPTION-ID"

# Add User Access Administrator role
New-AzRoleAssignment `
  -ObjectId $spId `
  -RoleDefinitionName "User Access Administrator" `
  -Scope "/subscriptions/$subscriptionId"

# Verify
Get-AzRoleAssignment -ObjectId $spId | Format-Table RoleDefinitionName, Scope
```

**Alternative:** If your security team restricts User Access Administrator, create a custom role with only the specific permissions Terraform needs.

### Error: "Service Principal password expired"

**Symptoms:**
```
Error: AADSTS7000222: The provided client secret keys are expired.
```

**Cause:** Service principal secret has expired (default: 1-2 years).

**Solution:**
```powershell
$appId = "YOUR-APP-ID"

# Create new secret (expires in 1 year)
$newSecret = New-AzADAppCredential `
  -ApplicationId $appId `
  -EndDate (Get-Date).AddYears(1)

Write-Host "New Secret: $($newSecret.SecretText)"

# Update Key Vault with new secret
Set-AzKeyVaultSecret `
  -VaultName "kv-tfstate-1234" `
  -Name "sp-terraform-devops-client-secret" `
  -SecretValue (ConvertTo-SecureString $newSecret.SecretText -AsPlainText -Force)

# Test authentication
az login --service-principal `
  --username $appId `
  --password $newSecret.SecretText `
  --tenant "YOUR-TENANT-ID"

# Remove old secret (after verifying new one works)
Remove-AzADAppCredential -ApplicationId $appId -KeyId OLD-KEY-ID
```

**Prevention:** 
1. Set Key Vault secret expiration notifications
2. Automate secret rotation with Azure Automation

### Error: "OAuth token has expired"

**Symptoms:**
```
Error: Failed to refresh access token
Error Code: invalid_grant
```

**Cause:** Pipeline running longer than token lifetime (typically 1 hour), or clock skew.

**Solution:**

**Immediate fix:** Re-run the pipeline (new token issued).

**Long-term fix:** Break large deployments into smaller stages:
```yaml
# Instead of one massive deployment
stages:
- stage: Deploy_Core_Infrastructure
- stage: Deploy_Networking (depends on core)
- stage: Deploy_Compute (depends on networking)
```

Each stage gets a fresh token.

## State File Issues

### Error: "Error locking state: another operation in progress"

**Symptoms:**
```
Error: Error acquiring the state lock
Lock Info:
  ID:        abc-123-def
  Path:      prod/terraform.tfstate
  Operation: OperationTypeApply
  Who:       john.doe@company.com
  Created:   2025-11-08 14:23:45.123 UTC
```

**Cause:** Previous pipeline run crashed or was canceled without releasing the lock.

**Solution:**

**Step 1: Verify the lock is stale**
```bash
# Check when the lock was created
az storage blob show \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --name prod/terraform.tfstate \
  --query "metadata.lock_id"
```

If the lock is more than 1 hour old and no pipeline is running, it's stale.

**Step 2: Force unlock**
```bash
# In the pipeline working directory
terraform force-unlock abc-123-def

# Confirm when prompted: yes
```

**Step 3: Re-run the pipeline**

**Prevention:** 
- Add a cleanup task to pipelines that always runs (even on failure):
```yaml
- task: Bash@3
  displayName: 'Force unlock on failure'
  condition: failed()
  inputs:
    script: |
      terraform force-unlock -force $(terraform show -json | jq -r '.values.lock_id')
```

### Error: "State file corrupted"

**Symptoms:**
```
Error: Failed to load state: state snapshot was created by Terraform v1.6.0, but this is v1.5.7
```

or

```
Error: Failed to parse state file: invalid JSON
```

**Cause:** State file corruption (rare but catastrophic).

**Solution:**

**Step 1: Stop all pipelines immediately**
Don't let multiple pipelines compete to fix the state.

**Step 2: Restore from backup**
```bash
# List available state file versions
az storage blob list \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --prefix prod/terraform.tfstate \
  --include v \
  --query "[].{Name:name, VersionId:versionId, LastModified:properties.lastModified}" \
  --output table

# Download a previous version
az storage blob download \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --name prod/terraform.tfstate \
  --version-id VERSION-ID-FROM-ABOVE \
  --file terraform-restored.tfstate

# Validate the restored state
terraform show terraform-restored.tfstate
```

**Step 3: Upload restored state**
```bash
az storage blob upload \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --name prod/terraform.tfstate \
  --file terraform-restored.tfstate \
  --overwrite
```

**Step 4: Run terraform refresh**
```bash
terraform refresh
```

**Step 5: Test with terraform plan**
```bash
terraform plan -detailed-exitcode
```

If exit code = 2, there's drift. Review the plan and decide whether to apply.

**Prevention:**
- Enable blob versioning (Part 1)
- Enable soft delete with 30-day retention
- Take manual state backups before major changes:
  ```bash
  az storage blob download \
    --account-name sttfstate1234 \
    --container-name terraform-state \
    --name prod/terraform.tfstate \
    --file "backup-$(date +%Y%m%d-%H%M%S).tfstate"
  ```

### Error: "Backend configuration changed"

**Symptoms:**
```
Error: Backend configuration changed
A change in the backend configuration has been detected, which may require migrating existing state.
```

**Cause:** You updated `backend.tf` (changed storage account, container, or key).

**Solution:**

**Step 1: Backup existing state**
```bash
terraform state pull > backup-before-migration.tfstate
```

**Step 2: Re-initialize with migration**
```bash
terraform init -migrate-state
```

**Step 3: Verify migration**
```bash
terraform state list
```

**Step 4: Clean up old state file (optional)**
```bash
# Remove old state from previous backend
az storage blob delete \
  --account-name OLD-STORAGE-ACCOUNT \
  --container-name OLD-CONTAINER \
  --name OLD-STATE-FILE
```

## Resource Drift Issues

### Error: "Resource already exists"

**Symptoms:**
```
Error: A resource with the ID "/subscriptions/.../resourceGroups/rsg-prod-001" already exists
To be managed via Terraform, this resource needs to be imported into the State.
```

**Cause:** Someone created the resource manually in the portal, and now Terraform wants to create it.

**Solution:**

**Option 1: Import the existing resource (preferred)**
```bash
# Import resource group
terraform import azurerm_resource_group.main /subscriptions/SUB-ID/resourceGroups/rsg-prod-001

# Verify import
terraform state show azurerm_resource_group.main

# Run plan (should show no changes)
terraform plan
```

**Option 2: Rename Terraform resource to avoid conflict**
```hcl
# Before
resource "azurerm_resource_group" "main" {
  name     = "rsg-prod-001"  # Conflicts with existing
  location = "northeurope"
}

# After
resource "azurerm_resource_group" "main" {
  name     = "rsg-prod-002"  # Different name
  location = "northeurope"
}
```

**Option 3: Delete the manually created resource (destructive)**
```bash
az group delete --name rsg-prod-001 --yes --no-wait
```

**Prevention:** 
- Implement Azure Policy: "Resources must have 'ManagedBy: Terraform' tag"
- Deny creation if tag is missing

### Error: "Inconsistent state after apply"

**Symptoms:**
```
Error: Provider produced inconsistent result after apply
When applying changes to azurerm_virtual_machine.main, the provider produced an unexpected new value.
```

**Cause:** Azure provider bug, race condition, or resource deleted mid-apply.

**Solution:**

**Step 1: Refresh state**
```bash
terraform refresh
```

**Step 2: Run plan to see actual drift**
```bash
terraform plan
```

**Step 3: Taint the problematic resource**
```bash
# Force Terraform to recreate the resource
terraform taint azurerm_virtual_machine.main
```

**Step 4: Re-apply**
```bash
terraform apply
```

**If that doesn't work:**
```bash
# Remove from state (doesn't delete from Azure)
terraform state rm azurerm_virtual_machine.main

# Re-import
terraform import azurerm_virtual_machine.main /subscriptions/SUB-ID/.../virtualMachines/vm-prod-001

# Re-apply
terraform apply
```

### Drift Detection: Resource Modified Outside Terraform

**Symptoms:**
Daily drift detection pipeline reports changes.

**Example:**
```
  ~ resource "azurerm_network_security_group" "main" {
      ~ security_rule {
          ~ description = "Allow RDP" -> "Allow RDP from VPN"
        }
    }
```

**Cause:** Someone edited the NSG rule in the portal.

**Solution:**

**Option 1: Accept the manual change (update Terraform code)**
```hcl
resource "azurerm_network_security_group_rule" "rdp" {
  name        = "Allow-RDP"
  description = "Allow RDP from VPN"  # Match portal change
  # ... rest of config
}
```

Commit, merge, deploy.

**Option 2: Revert the manual change (re-apply Terraform)**
```bash
terraform apply -auto-approve
```

This restores the Terraform-defined configuration.

**Prevention:**
- Educate team: "No manual portal changes"
- Azure Policy: Enforce tags on all resources
- Alerting: Daily drift detection emails

## Pipeline Performance Issues

### Issue: Pipeline takes > 10 minutes to run

**Symptoms:** `terraform plan` or `apply` runs very slowly.

**Common causes:**

#### 1. Large state file

**Check state file size:**
```bash
az storage blob show \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --name prod/terraform.tfstate \
  --query "properties.contentLength"
```

If > 10 MB, state is too large.

**Solution:** Split into multiple state files by logical boundaries:
```
terraform/
├── core-infrastructure/     (VNets, NSGs, state: core.tfstate)
├── compute/                 (VMs, AVDs, state: compute.tfstate)
├── storage/                 (Storage accounts, state: storage.tfstate)
└── databases/               (SQL, CosmosDB, state: databases.tfstate)
```

Each has its own backend config:
```hcl
terraform {
  backend "azurerm" {
    key = "core-infrastructure/terraform.tfstate"
  }
}
```

#### 2. Provider rate limiting

**Check pipeline logs for:**
```
Error: Error waiting for creation: Code="TooManyRequests"
```

**Solution:**
Add delays between resource creation:
```hcl
resource "time_sleep" "wait_30_seconds" {
  depends_on = [azurerm_resource_group.main]
  create_duration = "30s"
}

resource "azurerm_storage_account" "main" {
  depends_on = [time_sleep.wait_30_seconds]
  # ... config
}
```

**Better solution:** Use the provider's built-in retry logic:
```hcl
provider "azurerm" {
  features {}
  
  # Automatically retry on throttling
  skip_provider_registration = false
  storage_use_azuread        = true
  
  # Increase timeout for slow operations
  timeouts {
    create = "60m"
    update = "60m"
    delete = "60m"
  }
}
```

#### 3. Inefficient dependencies

**Check for unnecessary depends_on:**
```hcl
# BAD: Forces sequential creation
resource "azurerm_virtual_network" "vnet1" {
  name = "vnet-1"
  # ...
}

resource "azurerm_virtual_network" "vnet2" {
  depends_on = [azurerm_virtual_network.vnet1]  # Unnecessary!
  name = "vnet-2"
  # ...
}
```

**GOOD: Allows parallel creation**
```hcl
resource "azurerm_virtual_network" "vnet1" {
  name = "vnet-1"
  # ...
}

resource "azurerm_virtual_network" "vnet2" {
  name = "vnet-2"
  # ... (no depends_on)
}
```

Terraform will create both VNets in parallel (if no implicit dependency).

## Provider Version Issues

### Error: "Provider version mismatch"

**Symptoms:**
```
Error: Could not load plugin
Plugin reinitialization required. Please run "terraform init".
```

**Cause:** Terraform or provider version changed between plan and apply.

**Solution:**

**Short-term:** Pin exact versions (you should already have this from Part 5):
```hcl
terraform {
  required_version = "= 1.5.7"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "= 3.80.0"  # Exact version
    }
  }
}
```

**Long-term:** Create a version upgrade process:
1. Test new provider version in dev
2. Update version in dev `providers.tf`
3. Commit: "Upgrade azurerm provider to 3.85.0 in dev"
4. Test for 1 week
5. If stable, promote to test
6. Test for 1 week
7. If stable, promote to prod

### Error: "Feature flag not supported in provider version"

**Symptoms:**
```
Error: Unsupported argument
An argument named "public_network_access_enabled" is not expected here.
```

**Cause:** Using a new feature that doesn't exist in your pinned provider version.

**Solution:**

Check the provider changelog:
```bash
# Find when the feature was added
curl -s https://api.github.com/repos/hashicorp/terraform-provider-azurerm/releases | jq '.[] | select(.tag_name == "v3.80.0")'
```

If the feature was added in v3.85.0 but you're on v3.80.0:

**Option 1:** Upgrade provider (preferred)
```hcl
terraform {
  required_providers {
    azurerm = {
      version = "= 3.85.0"
    }
  }
}
```

**Option 2:** Work around the feature
```hcl
# Instead of provider feature flag
public_network_access_enabled = true

# Use a separate resource or workaround
resource "azurerm_storage_account_network_rules" "main" {
  # ...
}
```

## Debugging Strategies

### Enable Terraform Debug Logging

For deep troubleshooting, enable verbose logging:

**Add to pipeline task:**
```bash
# Set log level
export TF_LOG=DEBUG
export TF_LOG_PATH=terraform-debug.log

terraform plan

# Upload debug log as pipeline artifact
```

**In Azure DevOps pipeline:**
```yaml
- task: Bash@3
  displayName: 'Terraform Plan (Debug Mode)'
  env:
    TF_LOG: DEBUG
  inputs:
    script: |
      terraform plan -no-color > plan-output.txt 2>&1
      cat plan-output.txt
    
- task: PublishBuildArtifacts@1
  displayName: 'Publish Debug Logs'
  condition: always()
  inputs:
    pathToPublish: '$(System.DefaultWorkingDirectory)/terraform'
    artifactName: 'terraform-debug-logs'
```

### Use Terraform Graph for Dependency Visualization

**Generate dependency graph:**
```bash
terraform graph | dot -Tpng > graph.png
```

**Requires:** Graphviz installed on your machine.

**In pipeline:**
```bash
terraform graph > graph.dot

# Upload as artifact
```

View the graph to understand why resources are being created in a specific order.

### Test Locally Before Pipeline

**Mirror pipeline environment locally:**
```bash
# Set environment variables like the pipeline does
export ARM_SUBSCRIPTION_ID="YOUR-SUB-ID"
export ARM_CLIENT_ID="YOUR-CLIENT-ID"
export ARM_CLIENT_SECRET="YOUR-SECRET"
export ARM_TENANT_ID="YOUR-TENANT-ID"
export ARM_ACCESS_KEY="YOUR-STORAGE-KEY"

# Run Terraform commands
terraform init
terraform plan
```

**Benefits:**
- Faster feedback (no waiting for pipeline queue)
- Full control over debug settings
- Can use debugger tools

**Warning:** Never run `terraform apply` locally in production. This bypasses all approval gates.

### Query Azure Resource Graph

For complex drift scenarios, query Azure directly:

```kusto
// Find resources NOT managed by Terraform
Resources
| where tags.ManagedBy != "Terraform"
| where type == "microsoft.compute/virtualmachines"
| project name, resourceGroup, location, tags
| order by name asc
```

**Or via CLI:**
```bash
az graph query -q "Resources | where tags.ManagedBy != 'Terraform' | project name, resourceGroup"
```

## Production War Stories (Real Issues I've Faced)

### War Story 1: The 3 AM State Lock

**What happened:**
- Prod deployment failed at 3 AM during maintenance window
- State file remained locked
- Morning team couldn't deploy anything
- Escalated to me at 9 AM

**Root cause:**
- Pipeline agent crashed mid-apply (infrastructure issue)
- Lock never released
- No monitoring on lock duration

**Fix:**
```bash
# Force unlock
terraform force-unlock LOCK-ID

# Verify state integrity
terraform plan -detailed-exitcode
# Exit code 0 = good to go
```

**Prevention implemented:**
- Monitoring alert: State locked > 15 minutes
- Auto-unlock script in pipeline cleanup task
- Redundant Azure DevOps agent pool

### War Story 2: The Disappearing Resource Group

**What happened:**
- Terraform plan showed: `Plan: 0 to add, 0 to change, 0 to destroy`
- Ran apply
- Production resource group deleted
- Application down for 2 hours

**Root cause:**
- Resource group was manually removed from Terraform state (someone ran `terraform state rm` locally)
- State said "resource doesn't exist"
- Terraform deleted it from Azure to match state

**Fix:**
```bash
# Restore resource group from backup (thankfully we had ARM template exports)
az deployment sub create --location northeurope --template-file backup-rg.json
```

**Prevention implemented:**
- Disabled local Terraform commands in production
- All changes through pipelines only
- Daily state file backups with retention
- Audit: Who ran `terraform state rm`?

### War Story 3: The Provider Upgrade Disaster

**What happened:**
- Upgraded azurerm provider from 3.70.0 to 3.80.0 in prod
- 50+ resources marked for replacement (destroy + recreate)
- Included production databases

**Root cause:**
- Provider 3.80.0 changed default behavior for a resource attribute
- Existing resources didn't have the attribute explicitly set
- Terraform interpreted this as "needs to be recreated"

**Fix:**
```bash
# Revert provider version immediately
# Update code to explicitly set the attribute
# Re-upgrade in dev first
```

**Prevention implemented:**
- Provider version testing workflow: dev (1 week) → test (1 week) → prod
- Never upgrade providers in prod without testing
- Always read provider changelogs: "BREAKING CHANGES" section

### War Story 4: The Concurrent Apply

**What happened:**
- Two release pipelines triggered simultaneously
- Both acquired state lock somehow
- Both started applying changes
- Chaos: Half-deployed infrastructure, corrupted state

**Root cause:**
- Race condition: Both got lock before Azure Blob lease expired
- Network latency caused delayed lock propagation

**Fix:**
```bash
# Restored state from backup (15 minutes prior)
# Manually validated all resources in Azure
# Re-ran deployment from scratch
```

**Prevention implemented:**
- Release pipeline serialization: Only one release per environment at a time
- Added inter-pipeline mutex (release queues if another is running)
- Increased state lock timeout

## Emergency Runbook

Print this and keep it handy:

### Emergency: Pipeline Failing in Prod

**Step 1: Assess Impact**
- Is prod currently down? → Rollback immediately
- Is prod still working? → Investigate before action

**Step 2: Stop All Pipelines**
- Go to Pipelines → Running
- Cancel all Terraform pipelines

**Step 3: Check Logs**
- Last successful pipeline run
- What changed since then?

**Step 4: Verify State File Integrity**
```bash
terraform show
```

If this fails, state is corrupted → Restore from backup.

**Step 5: Rollback Options**
1. Revert the last merged PR (if code issue)
2. Restore state from backup (if state corrupted)
3. Manually fix the issue in Azure (last resort)

**Step 6: Post-Incident**
- Document what happened
- Update runbook
- Add monitoring to prevent recurrence

## Key Takeaways

1. **Always have state file backups** - Versioning + soft delete + manual backups
2. **Lock timeouts need monitoring** - Alert on locks > 15 minutes
3. **Test provider upgrades in dev first** - Never upgrade prod directly
4. **Drift detection is critical** - Run daily, alert on changes
5. **Local testing saves time** - Mirror pipeline environment locally for faster debugging
6. **Document your fixes** - Future you will thank you

## Useful Commands Reference

```bash
# State management
terraform state list                    # List all resources in state
terraform state show ADDRESS            # Show specific resource
terraform state rm ADDRESS              # Remove from state (doesn't delete Azure resource)
terraform state mv OLD NEW              # Rename resource in state

# Debugging
terraform plan -detailed-exitcode       # Exit code indicates drift
terraform refresh                       # Update state from Azure
terraform force-unlock LOCK-ID          # Clear stale lock
terraform validate                      # Syntax check

# Provider management
terraform providers                     # List providers
terraform version                       # Show Terraform version

# Dangerous (production use with caution)
terraform taint ADDRESS                 # Mark for recreation
terraform untaint ADDRESS               # Remove taint
terraform destroy                       # Delete all resources (DON'T USE IN PROD)
```

---

## Series Complete!

You've now completed the full Terraform + Azure DevOps CI/CD series:
- **Part 1:** Prerequisites & Architecture
- **Part 2:** Build Pipelines
- **Part 3:** Release Pipeline & Approval Gates
- **Part 4:** Branch Policies & Pull Request Automation
- **Part 5:** Production Best Practices
- **Part 6:** Troubleshooting (this post)

This is the exact setup I run in production at Synovus for deploying Azure infrastructure. It's battle-tested, audit-ready, and scalable.

**Want to discuss Terraform pipelines?** My blog doesn't have comments (by design), but you can open an issue in my [GitHub repo](https://github.com/dswann101164) or tag me in your own blog posts.

Good luck deploying infrastructure - may your state files never corrupt.

---

*All code and pipeline configurations from this series are available in my [GitHub repo](https://github.com/dswann101164).*
