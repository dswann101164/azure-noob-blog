---
title: "Terraform + Azure DevOps CI/CD: Part 5 - Production Best Practices & Multi-Environment Setup"
date: 2025-11-07
summary: "Scale from single environment to Dev/Test/Prod with separate state files, environment-specific approvals, and production hardening. This is how enterprises actually run Terraform."
tags: ["azure", "Terraform", "devops", "CICD", "IaC", "Azure DevOps", "Production"]
cover: "static/images/hero/terraform-devops-part5.png"
---

Parts 1-4 built a working CI/CD pipeline for Terraform. Now we make it production-ready with **multiple environments**, **separate state files**, and **environment-specific approval workflows**.

**What we're adding:**
- 🏗️ Dev/Test/Prod environment separation
- 📦 State file isolation (one per environment)
- 🔐 Environment-specific service principals
- ✅ Multi-stage approvals for production
- 🚨 Production deployment windows
- 📊 Deployment metrics and reporting

This is the difference between "I can deploy infrastructure" and "I can run infrastructure at scale."

## Environment Strategy

### The Three-Environment Model

**Development (Dev):**
- Purpose: Active development and testing
- Approval: Auto-deploy (no human approval)
- Cost: Minimal (small VMs, dev-tier services)
- Uptime: 9-5 business hours (deallocate at night to save cost)
- State file: `terraform-dev.tfstate`

**Test (Staging):**
- Purpose: Pre-production validation
- Approval: Single approver (any platform team member)
- Cost: Moderate (matches prod scale, but fewer instances)
- Uptime: 24/7 during testing cycles
- State file: `terraform-test.tfstate`

**Production (Prod):**
- Purpose: Live customer-facing systems
- Approval: Two approvers (infra lead + security/CAB)
- Cost: Full production workload
- Uptime: 24/7 with HA/DR
- State file: `terraform-prod.tfstate`

### Why Separate State Files?

**Without separation:**
- One corrupted state file affects all environments
- Terraform can't distinguish what's in dev vs. prod
- Accidental `terraform destroy` in wrong workspace = disaster

**With separation:**
- Each environment has isolated state
- State corruption limited to one environment
- Clear separation of concerns

## File Structure for Multi-Environment

Update your repository structure:

```
repo/
├── terraform/
│   ├── environments/
│   │   ├── dev/
│   │   │   ├── backend.tf
│   │   │   ├── terraform.tfvars
│   │   │   └── variables.tf (overrides)
│   │   ├── test/
│   │   │   ├── backend.tf
│   │   │   ├── terraform.tfvars
│   │   │   └── variables.tf (overrides)
│   │   └── prod/
│   │       ├── backend.tf
│   │       ├── terraform.tfvars
│   │       └── variables.tf (overrides)
│   ├── modules/
│   │   ├── networking/
│   │   ├── compute/
│   │   └── storage/
│   ├── providers.tf
│   ├── main.tf
│   └── variables.tf (global defaults)
├── .gitignore
└── README.md
```

**Key principles:**
- **Shared code** in `/terraform` (modules, providers, main logic)
- **Environment-specific config** in `/terraform/environments/{env}/`
- **No secrets in Git** (still using Key Vault)

## Configure Multiple State Files

### Create Environment-Specific Backend Configs

**File: `terraform/environments/dev/backend.tf`**

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rsg-terraform-state"
    storage_account_name = "sttfstate1234"
    container_name       = "terraform-state"
    key                  = "dev/terraform.tfstate"  # Dev-specific state file
  }
}
```

**File: `terraform/environments/test/backend.tf`**

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rsg-terraform-state"
    storage_account_name = "sttfstate1234"
    container_name       = "terraform-state"
    key                  = "test/terraform.tfstate"  # Test-specific state file
  }
}
```

**File: `terraform/environments/prod/backend.tf`**

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rsg-terraform-state"
    storage_account_name = "sttfstate1234"
    container_name       = "terraform-state"
    key                  = "prod/terraform.tfstate"  # Prod-specific state file
  }
}
```

**Notice:** The only difference is the `key` parameter. Each environment gets its own state file in the same storage account.

### Create Environment-Specific Variable Files

**File: `terraform/environments/dev/terraform.tfvars`**

```hcl
environment = "dev"
location    = "northeurope"

# Dev uses small VMs
vm_size = "Standard_B2s"

# Dev uses dev-tier services
sql_sku = "Basic"

# Dev tags
tags = {
  Environment = "Development"
  CostCenter  = "IT-Platform"
  ManagedBy   = "Terraform"
}
```

**File: `terraform/environments/test/terraform.tfvars`**

```hcl
environment = "test"
location    = "northeurope"

# Test matches prod scale
vm_size = "Standard_D4s_v5"

# Test uses production-tier services (for realistic testing)
sql_sku = "S3"

tags = {
  Environment = "Test"
  CostCenter  = "IT-Platform"
  ManagedBy   = "Terraform"
}
```

**File: `terraform/environments/prod/terraform.tfvars`**

```hcl
environment = "prod"
location    = "northeurope"

# Prod uses production-grade VMs
vm_size = "Standard_D8s_v5"

# Prod uses production-tier services with HA
sql_sku = "P2"

tags = {
  Environment = "Production"
  CostCenter  = "Business-Operations"
  ManagedBy   = "Terraform"
  Compliance  = "SOC2"
}
```

**Key differences:**
- VM sizes increase from dev → test → prod
- Service tiers increase (Basic → S3 → P2)
- Tags change to reflect environment and cost attribution

## Update Terraform Code for Environment Support

### Global Variables (Shared)

**File: `terraform/variables.tf`**

```hcl
variable "environment" {
  description = "Environment name (dev, test, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "test", "prod"], var.environment)
    error_message = "Environment must be dev, test, or prod."
  }
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "northeurope"
}

variable "vm_size" {
  description = "VM size"
  type        = string
}

variable "sql_sku" {
  description = "SQL Database SKU"
  type        = string
}

variable "tags" {
  description = "Common tags for all resources"
  type        = map(string)
}

# Service principal variables (injected from Key Vault)
variable "subscription_id" {
  type      = string
  sensitive = true
}

variable "spn_client_id" {
  type      = string
  sensitive = true
}

variable "spn_client_secret" {
  type      = string
  sensitive = true
}

variable "spn_tenant_id" {
  type      = string
  sensitive = true
}
```

### Resource Naming with Environment

**File: `terraform/main.tf`**

```hcl
locals {
  # Generate environment-specific resource names
  resource_group_name = "rsg-${var.environment}-001"
  vnet_name          = "vnet-${var.environment}-001"
  storage_name       = "st${var.environment}data${random_integer.suffix.result}"
  
  # Merge global tags with environment-specific tags
  common_tags = merge(
    var.tags,
    {
      ManagedBy   = "Terraform"
      Environment = var.environment
      DeployedAt  = timestamp()
    }
  )
}

resource "random_integer" "suffix" {
  min = 1000
  max = 9999
}

resource "azurerm_resource_group" "main" {
  name     = local.resource_group_name
  location = var.location
  tags     = local.common_tags
}

resource "azurerm_virtual_network" "main" {
  name                = local.vnet_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  address_space       = ["10.${var.environment == "prod" ? 0 : var.environment == "test" ? 1 : 2}.0.0/16"]
  
  tags = local.common_tags
}
```

**What this does:**
- Resource names include environment (e.g., `rsg-dev-001`, `rsg-prod-001`)
- IP ranges differ per environment (prod = 10.0.x.x, test = 10.1.x.x, dev = 10.2.x.x)
- All resources get environment-specific tags

## Create Environment-Specific Build Pipelines

You need separate build pipelines for each environment.

### Clone the Existing Build Pipeline (3 Times)

1. Go to **Pipelines > Pipelines**
2. Find **Terraform Plan (Create Artifact)**
3. Click **...** > **Clone**
4. Rename to: **Terraform Plan - Dev**

Repeat for **Test** and **Prod**.

### Update Each Pipeline's Init Task

Edit **Terraform Plan - Dev** pipeline:

Find the **Terraform Init** task and update the script:

```bash
terraform init \
  -backend-config="access_key=$(sttfstate1234-key1)" \
  -backend-config="key=dev/terraform.tfstate"
```

**Advanced > Working Directory:** `$(System.DefaultWorkingDirectory)/terraform/environments/dev`

**Repeat for other environments:**
- **Test:** `-backend-config="key=test/terraform.tfstate"` and working directory `terraform/environments/test`
- **Prod:** `-backend-config="key=prod/terraform.tfstate"` and working directory `terraform/environments/prod`

### Update Each Pipeline's Plan Task

Edit the **Terraform Plan** task to include the environment-specific `.tfvars`:

```bash
terraform plan \
  -input=false \
  -out=tfplan \
  -var-file="terraform.tfvars" \
  -var="subscription_id=$(subscription-id)" \
  -var="spn_client_id=$(sp-terraform-devops-client-id)" \
  -var="spn_client_secret=$(sp-terraform-devops-client-secret)" \
  -var="spn_tenant_id=$(sp-terraform-devops-tenant-id)"
```

**What changed:** Added `-var-file="terraform.tfvars"` to load environment-specific variables.

### Update Triggers for Each Pipeline

**Dev Pipeline:**
- **CI trigger:** ON
- **Branch filter:** `main`
- **Path filter:** `terraform/environments/dev/**`

**Test Pipeline:**
- **CI trigger:** ON
- **Branch filter:** `main`
- **Path filter:** `terraform/environments/test/**`

**Prod Pipeline:**
- **CI trigger:** ON
- **Branch filter:** `main`
- **Path filter:** `terraform/environments/prod/**`

**What this does:** Only trigger the relevant environment's pipeline when its files change.

## Create Environment-Specific Release Pipelines

### Dev Release Pipeline

Clone your existing release pipeline and rename to: **Deploy Terraform - Dev**

**Changes:**
1. **Artifact source:** `Terraform Plan - Dev`
2. **Stage name:** `Deploy to Development`
3. **Pre-deployment approval:** DISABLED (auto-deploy to dev)
4. **Working directory in tasks:** `terraform/environments/dev`

**Init task script:**
```bash
terraform init \
  -backend-config="access_key=$(sttfstate1234-key1)" \
  -backend-config="key=dev/terraform.tfstate"
```

### Test Release Pipeline

Clone and rename to: **Deploy Terraform - Test**

**Changes:**
1. **Artifact source:** `Terraform Plan - Test`
2. **Stage name:** `Deploy to Test`
3. **Pre-deployment approval:** ENABLED
   - Approvers: Any platform team member
   - Timeout: 7 days
4. **Working directory in tasks:** `terraform/environments/test`

**Init task script:**
```bash
terraform init \
  -backend-config="access_key=$(sttfstate1234-key1)" \
  -backend-config="key=test/terraform.tfstate"
```

### Prod Release Pipeline

Clone and rename to: **Deploy Terraform - Prod**

**Changes:**
1. **Artifact source:** `Terraform Plan - Prod`
2. **Stage name:** `Deploy to Production`
3. **Pre-deployment approval:** ENABLED
   - **First approver:** Infrastructure lead
   - **Second approver:** Security team or CAB representative
   - Timeout: 48 hours (shorter than test, forces timely decisions)
   - **Policy:** Approvers must be different people
4. **Working directory in tasks:** `terraform/environments/prod`

**Init task script:**
```bash
terraform init \
  -backend-config="access_key=$(sttfstate1234-key1)" \
  -backend-config="key=prod/terraform.tfstate"
```

### Add Deployment Gates for Production

Deployment gates add additional automation checks before deployment.

**Configure gates for Prod release:**

1. Edit **Deploy Terraform - Prod** pipeline
2. Click the **lightning bolt with person** on the `Deploy to Production` stage
3. Click **Gates** tab
4. Toggle on: **Gates**

**Add gate: Invoke Azure Function**

If you have an Azure Function that checks:
- Current incident count (from ServiceNow/PagerDuty)
- Ongoing maintenance windows
- Recent failed deployments

**Settings:**
- **Function URL:** Your validation function
- **Evaluation options:**
  - **Time between re-evaluation:** 5 minutes
  - **Timeout after which gates fail:** 30 minutes
  - **Minimum duration gates must succeed:** 5 minutes

**Example gate logic:**
```csharp
// Azure Function: Check if it's safe to deploy
if (activeIncidents > 0) return "FAIL: Active P1 incidents";
if (maintenanceWindow) return "FAIL: Maintenance in progress";
if (recentFailures > 2) return "FAIL: Too many recent failed deployments";
return "PASS: Safe to deploy";
```

**Alternative if you don't have Azure Functions:** Use **Query Work Items** gate to check Azure Boards for blocking issues.

## Production Hardening

### 1. State File Locking

Ensure state file locking is enabled (prevents concurrent modifications).

Azure Blob Storage supports locking by default, but verify:

```powershell
# Check storage account settings
$storageAccount = Get-AzStorageAccount -ResourceGroupName "rsg-terraform-state" -Name "sttfstate1234"
$storageAccount.EnableHttpsTrafficOnly  # Should be True
```

**In Terraform:** Lock happens automatically when you run `terraform plan` or `apply`. You'll see:
```
Acquiring state lock. This may take a few moments...
```

**If someone else has the lock:**
```
Error: Error acquiring the state lock
Lock Info:
  ID:        abc-123-def
  Path:      prod/terraform.tfstate
  Operation: OperationTypeApply
  Who:       john.doe@company.com
  Created:   2025-11-07 14:23:45.123 UTC
```

### 2. State File Backups

Enable blob versioning and soft delete (you should have done this in Part 1, but verify):

```powershell
$ctx = (Get-AzStorageAccount -ResourceGroupName "rsg-terraform-state" -Name "sttfstate1234").Context

# Enable versioning
Enable-AzStorageBlobDeleteRetentionPolicy -Context $ctx -RetentionDays 30

# Enable soft delete
Enable-AzStorageBlobDeleteRetentionPolicy -Context $ctx -RetentionDays 30 -PassThru

# Enable container soft delete
Enable-AzStorageContainerDeleteRetentionPolicy -Context $ctx -RetentionDays 30
```

**Why:** If someone corrupts state or accidentally deletes it, you have 30 days to recover.

### 3. Terraform Version Pinning

**File: `terraform/providers.tf`**

```hcl
terraform {
  required_version = "= 1.5.7"  # Exact version, not >= 1.5.7
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "= 3.80.0"  # Exact version
    }
    random = {
      source  = "hashicorp/random"
      version = "= 3.5.1"
    }
  }
}
```

**Why:** Provider updates can introduce breaking changes. Pin versions and update intentionally during maintenance windows.

**Update process:**
1. Test new provider version in dev
2. If stable, promote to test
3. If no issues, update prod during next maintenance window

### 4. Import Existing Resources (Avoid Drift)

If someone manually created resources in the portal, import them into state:

```bash
# Import existing resource group
terraform import azurerm_resource_group.main /subscriptions/SUB-ID/resourceGroups/rsg-manual-001

# Import existing VM
terraform import azurerm_virtual_machine.main /subscriptions/SUB-ID/resourceGroups/rsg-manual-001/providers/Microsoft.Compute/virtualMachines/vm-manual-001
```

**Better approach:** Use Azure Policy to **prevent** manual resource creation:
- Policy: "Resources must have 'ManagedBy: Terraform' tag"
- Effect: Deny creation if tag is missing
- Exemptions: Emergency service accounts only

### 5. Drift Detection (Daily Scheduled Check)

Create a scheduled pipeline that runs `terraform plan` daily and alerts on drift.

**New pipeline:** `Terraform Drift Detection - Prod`

**Schedule:**
- Trigger: Daily at 6 AM
- Actions: 
  1. Run `terraform plan -detailed-exitcode`
  2. If exit code = 2 (changes detected), send alert email
  3. Post summary to Teams/Slack

**Script:**
```bash
terraform plan -detailed-exitcode -no-color > plan-output.txt
EXIT_CODE=$?

if [ $EXIT_CODE -eq 2 ]; then
  echo "##vso[task.logissue type=warning]Drift detected in production!"
  # Send email or Teams notification
  # Attach plan-output.txt
fi
```

### 6. Production Deployment Windows

Restrict prod deployments to approved maintenance windows.

**Configure release pipeline:**
1. Edit **Deploy Terraform - Prod**
2. Click **Options** tab
3. **Release triggers:**
   - Uncheck: **Continuous deployment**
   - Check: **Scheduled release**
   - **Schedule:** Saturday, 2:00 AM - 6:00 AM

**What this does:** Releases only deploy during the approved window. Outside this window, releases queue but don't start.

**Override for emergencies:** Admins can manually trigger releases outside the window (logged for audit).

## Multi-Stage Promotion Workflow

For the safest deployment process, promote changes through environments:

### Workflow: Dev → Test → Prod

**Week 1:**
1. Merge PR to `main`
2. Dev pipeline runs → auto-deploys to dev
3. Test in dev for 1-2 days
4. Verify functionality

**Week 2:**
5. Create PR to merge `terraform/environments/dev/**` changes to `terraform/environments/test/**`
6. Test pipeline runs → manual approval → deploys to test
7. Run smoke tests in test environment
8. QA team validates

**Week 3:**
9. Create PR to merge test changes to prod
10. Prod pipeline runs → two approvals required → deploys to prod
11. Monitor for 24 hours
12. Incident-free? Mark as stable.

**Key principle:** Never promote from dev directly to prod. Always: dev → test → prod.

## Rollback Strategy

Despite best efforts, sometimes deployments fail. Have a rollback plan.

### Option 1: Roll Forward (Preferred)

Fix the issue and deploy a new release.

**Why preferred:** Maintains audit trail and doesn't rely on state manipulation.

**Process:**
1. Identify issue
2. Create hotfix branch
3. Fix Terraform code
4. Emergency PR → merge
5. Emergency release approval → deploy

### Option 2: Revert PR

If the deployment succeeded but introduced a functional bug:

1. Go to **Repos > Pull requests > Completed**
2. Find the PR that caused the issue
3. Click **Revert**
4. Create new PR with reverted changes
5. Merge → deploy

**Result:** Infrastructure returns to previous state.

### Option 3: Manual State Rollback (Last Resort)

If state is corrupted and you need to restore from backup:

```bash
# Download current state (backup before changing)
az storage blob download \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --name prod/terraform.tfstate \
  --file terraform-current.tfstate

# List previous versions
az storage blob list \
  --account-name sttfstate1234 \
  --container-name terraform-state \
  --prefix prod/terraform.tfstate \
  --include v

# Restore a previous version
az storage blob copy start \
  --account-name sttfstate1234 \
  --destination-container terraform-state \
  --destination-blob prod/terraform.tfstate \
  --source-container terraform-state \
  --source-blob prod/terraform.tfstate?versionId=VERSION-ID

# Run terraform plan to verify
terraform plan
```

**Warning:** Only do this if you understand the implications. Incorrect state restoration can cause resource deletion.

## Monitoring and Reporting

### 1. Deployment Metrics Dashboard

Create a Power BI dashboard tracking:
- **Deployment frequency** (per environment)
- **Success rate** (successful vs. failed deployments)
- **Approval wait time** (time from release creation to approval)
- **Deployment duration** (time from approval to completion)
- **Rollback frequency**

**Data source:** Azure DevOps REST API

### 2. Cost Tracking by Environment

Tag all resources with environment name, then use Azure Cost Management:

```kusto
// KQL query for cost by environment
AzureActivity
| where ResourceProvider == "Microsoft.Resources" and OperationName == "Microsoft.Resources/deployments/write"
| extend Environment = tostring(parse_json(Properties).environment)
| summarize DeploymentCount = count() by Environment, bin(TimeGenerated, 1d)
```

### 3. Audit Log for Approvals

Query Azure DevOps for approval history:

```powershell
# Get all releases for the last 30 days
$releases = az pipelines runs list --pipeline-ids PIPELINE-ID --query "[?finishTime >= '2025-10-01']" | ConvertFrom-Json

foreach ($release in $releases) {
    # Get approval details
    $approvals = az pipelines release approvals list --release-id $release.id | ConvertFrom-Json
    
    # Report
    Write-Host "Release: $($release.name)"
    Write-Host "Approved by: $($approvals.approvedBy.displayName)"
    Write-Host "Approved at: $($approvals.createdOn)"
}
```

## Key Takeaways

1. **Separate state files per environment** - Isolation prevents cascading failures
2. **Environment-specific approval workflows** - Dev auto-deploys, prod requires multiple approvals
3. **Terraform version pinning** - Predictable deployments, no surprise breaking changes
4. **Drift detection** - Catch manual portal changes before they cause issues
5. **Deployment gates and windows** - Production deploys only during safe periods
6. **Promote through environments** - Dev → Test → Prod, never skip stages

You now have an enterprise-grade, multi-environment Terraform CI/CD pipeline.

---

**Next:** [Part 6 - Troubleshooting & Common Production Issues](/blog/terraform-azure-devops-cicd-part6-troubleshooting/)

*All code and pipeline configurations from this series are available in my [GitHub repo](https://github.com/dswann101164).*
