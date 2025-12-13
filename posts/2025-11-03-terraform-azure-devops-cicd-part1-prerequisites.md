---
title: "Terraform + Azure DevOps CI/CD: Part 1 - Prerequisites & Architecture"
date: 2025-11-03
summary: "Enterprise-grade Infrastructure as Code with pull request approvals, Key Vault secrets, and zero manual portal changes. This is the exact setup I use in production - GUI pipelines, not YAML."
tags: ["azure", "Terraform", "devops", "CICD", "IaC", "Azure DevOps"]
cover: "static/images/hero/terraform-devops-part1.png"
hub: governance
---
This is the **exact** Terraform + Azure DevOps CI/CD setup I use in production at a financial services company. Not a proof-of-concept - this is battle-tested infrastructure that deploys real Azure resources every day.


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

**What makes this different:**
- **GUI pipelines, not YAML** - Full visual control, easier troubleshooting
- **Two approval gates** - Pull request review + release approval before deployment
- **Zero secrets in code** - Everything in Key Vault, injected at runtime
- **Plan file consistency** - What reviewers approve is exactly what deploys
- **No manual portal changes** - Everything through Git, everything reviewed

This is a 4-part series. Part 1 covers the architecture and one-time prerequisites.

## Why This Setup Exists

Most Terraform tutorials show you how to run `terraform apply` from your laptop. Great for learning. Useless for production.

In the real world, you need:
1. **Approval workflows** - Nobody deploys infrastructure without review
2. **Secret management** - Service principals, storage keys, never in Git
3. **Consistency** - Deployment matches what was approved, not latest Git commit
4. **Auditability** - Who approved what, when, and why
5. **Team collaboration** - Multiple people, no laptop dependencies

This setup delivers all of that using Azure DevOps classic pipelines (GUI-based, not YAML).

## The Full Workflow (End-to-End)

Here's what happens when you want to deploy infrastructure:

### Step 1: Create Feature Branch
```bash
git checkout -b add-resource-group
```

You CANNOT commit directly to `main`. Branch policies enforce this.

### Step 2: Write Terraform Code
```hcl
# demo.tf
resource "azurerm_resource_group" "test" {
  name     = "rsg-demo-001"
  location = "northeurope"
  
  provider = azurerm.connectivity
}
```

### Step 3: Push Branch + Create Pull Request
```bash
git add terraform/demo.tf
git commit -m "Add demo resource group"
git push origin add-resource-group
```

Azure DevOps automatically:
- Runs `terraform validate`
- Runs `terraform plan` (no output file)
- Shows plan results in PR comments
- Requires your review before merge

### Step 4: Review Pull Request
You (or your teammate) review:
- The code changes (files tab)
- The plan output (what will deploy)
- Status checks (must pass)

If good, approve and complete the PR.

### Step 5: Automatic Build Pipeline
When PR merges to `main`:
- `terraform plan` runs again
- Plan output saved to `.tfplan` file
- File archived + published as artifact

### Step 6: Release Approval Gate
Release pipeline waits for your approval:
- You review the artifact contents
- You approve deployment (or defer to change window)
- Only then does `terraform apply` run

### Step 7: Deployment
```
terraform apply -auto-approve -input=false tfplan
```

Resource group deploys. You never touched the Azure portal.

## Architecture Overview

### Components

**Azure Resources (One-Time Setup):**
1. **Storage Account** - Terraform remote state backend
2. **Key Vault** - Secrets (storage keys, service principal credentials)
3. **Service Principal** - Azure DevOps identity for deployments

**Azure DevOps (One-Time Setup):**
1. **Service Connection** - Links DevOps to Azure via service principal
2. **Variable Group** - Links DevOps to Key Vault secrets
3. **Git Repository** - Stores Terraform code

**Azure DevOps Pipelines:**
1. **Terraform Status Check** (Build) - Runs on PR creation (validate + plan, no artifact)
2. **Terraform Plan** (Build) - Runs on merge to main (plan + artifact)
3. **Terraform Apply** (Release) - Runs after approval (applies artifact)

**Branch Policies:**
- Require pull request reviews
- Automatically trigger status check pipeline
- Block direct commits to `main`

### Why Three Pipelines?

**Status Check Pipeline:**
- Triggers: Pull request created/updated
- Purpose: Fast feedback - is the code valid? What will it do?
- Output: Plan displayed in PR, no artifact

**Plan Pipeline:**
- Triggers: Code merged to `main` branch
- Purpose: Create deployment artifact from approved code
- Output: `.tfplan` file archived as artifact

**Apply Pipeline (Release):**
- Triggers: New artifact from Plan pipeline
- Purpose: Deploy approved infrastructure
- Output: Resources in Azure

**Why not one pipeline?** Separation of concerns. Status checks need to be fast (no approval gates). Apply needs to be controlled (approval gates). Plan creates the bridge between them.

## Prerequisites: What You Need to Set Up Manually

These are **one-time manual steps**. Do them once, use them forever.

### 1. Azure Storage Account (Remote State Backend)

Terraform state files CANNOT live in Git. Ever. Use Azure Blob Storage.

**Why:**
- State files contain secrets (connection strings, keys, sensitive data)
- Multiple users need shared state (concurrency control)
- Automatic locking prevents conflicts

**Setup:**
```powershell
# Variables
$resourceGroup = "rsg-terraform-state"
$storageAccount = "sttfstate$(Get-Random -Maximum 9999)"
$location = "northeurope"
$containerName = "terraform-state"

# Create resource group
New-AzResourceGroup -Name $resourceGroup -Location $location

# Create storage account (LRS = sufficient, enable versioning)
$storageParams = @{
    ResourceGroupName = $resourceGroup
    Name = $storageAccount
    Location = $location
    SkuName = "Standard_LRS"
    Kind = "StorageV2"
    MinimumTlsVersion = "TLS1_2"
    AllowBlobPublicAccess = $false
    EnableHttpsTrafficOnly = $true
}
New-AzStorageAccount @storageParams

# Enable blob versioning (so you can roll back state if needed)
$ctx = (Get-AzStorageAccount -ResourceGroupName $resourceGroup -Name $storageAccount).Context
Enable-AzStorageBlobDeleteRetentionPolicy -Context $ctx -RetentionDays 7
Enable-AzStorageBlobInventoryPolicy -Context $ctx

# Create container
New-AzStorageContainer -Name $containerName -Context $ctx -Permission Off

# SAVE THESE VALUES - YOU'LL NEED THEM
Write-Host "Storage Account Name: $storageAccount"
Write-Host "Container Name: $containerName"
Write-Host "Resource Group: $resourceGroup"

# Get access keys (we'll store these in Key Vault next)
$keys = Get-AzStorageAccountKey -ResourceGroupName $resourceGroup -Name $storageAccount
Write-Host "Key1: $($keys[0].Value)"  # SAVE THIS
Write-Host "Key2: $($keys[1].Value)"  # SAVE THIS
```

**Important Settings:**
- **Soft delete enabled (7 days)** - Recover corrupted state files
- **Versioning enabled** - Roll back to previous state versions
- **TLS 1.2 minimum** - Security baseline
- **No public blob access** - Private storage only

### 2. Azure Key Vault (Secret Storage)

Never put secrets in Git. Never put secrets in Azure DevOps variables. Use Key Vault.

**What Goes in Key Vault:**
- Storage account access keys (key1, key2)
- Service principal client ID
- Service principal client secret
- Service principal tenant ID
- Service principal object ID (optional, useful for role assignments)

**Setup:**
```powershell
# Variables
$keyVaultName = "kv-tfstate-$(Get-Random -Maximum 9999)"
$resourceGroup = "rsg-terraform-state"  # Same RG as storage
$location = "northeurope"

# Create Key Vault
$kvParams = @{
    Name = $keyVaultName
    ResourceGroupName = $resourceGroup
    Location = $location
    Sku = "Standard"
    EnablePurgeProtection = $true
    EnableSoftDelete = $true
    SoftDeleteRetentionInDays = 90
}
New-AzKeyVault @kvParams

# SAVE THIS VALUE
Write-Host "Key Vault Name: $keyVaultName"
```

**Key Vault Secrets to Add (Do This After Creating Service Principal):**

We'll add these in the next step, but here's the naming convention:
- `{storage-account-name}-key1`
- `{storage-account-name}-key2`
- `{service-principal-name}-client-id`
- `{service-principal-name}-client-secret`
- `{service-principal-name}-tenant-id`
- `{service-principal-name}-object-id`

Example:
```powershell
# After you have the storage account key
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name "sttfstate1234-key1" -SecretValue (ConvertTo-SecureString "YOUR-KEY-HERE" -AsPlainText -Force)
```

### 3. Service Principal (Azure DevOps Identity)

Azure DevOps needs a service principal to authenticate to Azure and deploy resources.

**Why Service Principal (Not Managed Identity):**
- Azure DevOps hosted agents don't support managed identities yet
- Service principals work across subscriptions
- Explicit credential rotation policy

**Setup:**
```powershell
# Create service principal
$spName = "sp-terraform-devops"
$sp = New-AzADServicePrincipal -DisplayName $spName -Role "Owner" -Scope "/subscriptions/YOUR-SUBSCRIPTION-ID"

# SAVE THESE VALUES IMMEDIATELY - SECRET ONLY SHOWS ONCE
Write-Host "Application (Client) ID: $($sp.AppId)"
Write-Host "Tenant ID: $((Get-AzContext).Tenant.Id)"
Write-Host "Object ID: $($sp.Id)"
Write-Host "Client Secret: $($sp.PasswordCredentials.SecretText)"  # SAVE THIS NOW
```

**Permissions:**
- **Owner** on subscription (or management group if multi-subscription)
- Why Owner? Terraform needs to assign Azure roles (Contributor isn't enough)

**Alternative (More Secure):**
If your org restricts Owner, use **Contributor + User Access Administrator**:
```powershell
# Assign Contributor
New-AzRoleAssignment -ObjectId $sp.Id -RoleDefinitionName "Contributor" -Scope "/subscriptions/YOUR-SUB-ID"

# Assign User Access Administrator (for role assignments)
New-AzRoleAssignment -ObjectId $sp.Id -RoleDefinitionName "User Access Administrator" -Scope "/subscriptions/YOUR-SUB-ID"
```

### 4. Add Secrets to Key Vault

Now that you have storage keys and service principal credentials, store them:

```powershell
$keyVaultName = "kv-tfstate-1234"  # Your Key Vault name

# Storage account secrets
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name "sttfstate1234-key1" -SecretValue (ConvertTo-SecureString "STORAGE-KEY-1" -AsPlainText -Force)
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name "sttfstate1234-key2" -SecretValue (ConvertTo-SecureString "STORAGE-KEY-2" -AsPlainText -Force)

# Service principal secrets
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name "sp-terraform-devops-client-id" -SecretValue (ConvertTo-SecureString "CLIENT-ID-GUID" -AsPlainText -Force)
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name "sp-terraform-devops-client-secret" -SecretValue (ConvertTo-SecureString "SECRET-VALUE" -AsPlainText -Force)
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name "sp-terraform-devops-tenant-id" -SecretValue (ConvertTo-SecureString "TENANT-ID-GUID" -AsPlainText -Force)
Set-AzKeyVaultSecret -VaultName $keyVaultName -Name "sp-terraform-devops-object-id" -SecretValue (ConvertTo-SecureString "OBJECT-ID-GUID" -AsPlainText -Force)

# Optional: Set expiration on the client secret to match your rotation policy
$secretName = "sp-terraform-devops-client-secret"
$expirationDate = (Get-Date).AddYears(1)  # 1 year from now
Update-AzKeyVaultSecret -VaultName $keyVaultName -Name $secretName -Expires $expirationDate
```

**Pro Tip:** Use consistent naming. I use `{resource-name}-{secret-type}` so it's obvious what each secret is for.

### 5. Grant Service Principal Access to Key Vault

The service principal needs to READ secrets from Key Vault (so Azure DevOps can retrieve them at runtime).

```powershell
$keyVaultName = "kv-tfstate-1234"
$spObjectId = "YOUR-SP-OBJECT-ID"  # From step 3

# Grant Get and List permissions on secrets
Set-AzKeyVaultAccessPolicy -VaultName $keyVaultName -ObjectId $spObjectId -PermissionsToSecrets Get,List

# Verify
Get-AzKeyVaultAccessPolicy -VaultName $keyVaultName
```

**Why only Get and List?** Principle of least privilege. The service principal doesn't need to create, update, or delete secrets.

## Azure DevOps Setup

### 1. Create Azure DevOps Project

If you don't have one:
1. Go to `dev.azure.com`
2. Create organization (free for up to 5 users)
3. Create new project
4. Initialize Git repo with `.gitignore` for Terraform

**Important:** When initializing the repo, select **Terraform** from the .gitignore template dropdown. This prevents accidentally committing `.tfstate`, `.tfvars`, and `.tfplan` files.

### 2. Create Service Connection

This links Azure DevOps to your Azure subscription using the service principal.

**Steps:**
1. Go to **Project Settings** (bottom-left gear icon)
2. Click **Service connections** (under Pipelines)
3. Click **New service connection**
4. Select **Azure Resource Manager**
5. Select **Service principal (manual)**

**Fill in the form:**
- **Subscription ID:** Your Azure subscription ID
- **Subscription Name:** Friendly name
- **Service Principal ID:** The **Application (Client) ID** from step 3
- **Service Principal Key:** The **Client Secret** from step 3 (you saved it, right?)
- **Tenant ID:** Your Azure AD tenant ID
- **Service connection name:** `terraform-azure-connection` (use this exact name, or update pipeline YAML later)

**Grant Access:**
- Check the box: **Grant access permission to all pipelines**

Click **Verify** to test the connection. If it fails, double-check your service principal credentials.

### 3. Create Variable Group (Linked to Key Vault)

This is where the magic happens - Azure DevOps can dynamically pull secrets from Key Vault at pipeline runtime.

**Steps:**
1. Go to **Pipelines > Library**
2. Click **+ Variable group**
3. Name it: `terraform-keyvault-secrets` (or match your Key Vault name for clarity)
4. Toggle on: **Link secrets from an Azure key vault as variables**
5. Select your service connection: `terraform-azure-connection`
6. Select your Key Vault: `kv-tfstate-1234`
7. Click **+ Add** and select ALL the secrets you created:
   - `sttfstate1234-key1`
   - `sttfstate1234-key2`
   - `sp-terraform-devops-client-id`
   - `sp-terraform-devops-client-secret`
   - `sp-terraform-devops-tenant-id`
   - `sp-terraform-devops-object-id`

**Grant Access:**
- Check: **Allow access to all pipelines**

Click **Save**.

**What This Does:**
- At pipeline runtime, Azure DevOps authenticates to Key Vault using the service principal
- It retrieves the secret VALUES (but they're masked in logs)
- Pipeline tasks can reference these as variables: `$(sttfstate1234-key1)`

**Security Note:** The secret values are NEVER displayed in logs. Azure DevOps automatically masks them.

## Terraform Configuration Files

Before we build pipelines, we need Terraform configuration files in the Git repo.

### 1. Create `/terraform` Folder

All Terraform code lives here. Keep it separate from pipeline YAML (if you later decide to add YAML).

```
repo/
├── terraform/
│   ├── providers.tf
│   ├── backend.tf
│   ├── variables.tf
│   └── main.tf (your actual resources)
├── .gitignore
└── README.md
```

### 2. `providers.tf`

```hcl
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80.0"  # Use latest stable
    }
  }
}

provider "azurerm" {
  features {}
  
  subscription_id = var.subscription_id
  client_id       = var.spn_client_id
  client_secret   = var.spn_client_secret
  tenant_id       = var.spn_tenant_id
}

# Optional: Multiple subscription support
provider "azurerm" {
  alias = "connectivity"
  features {}
  
  subscription_id = "YOUR-CONNECTIVITY-SUB-ID"
  client_id       = var.spn_client_id
  client_secret   = var.spn_client_secret
  tenant_id       = var.spn_tenant_id
}
```

**Why Variables Here?** We're NOT hardcoding credentials. Azure DevOps will inject these at runtime from Key Vault.

### 3. `backend.tf`

```hcl
terraform {
  backend "azurerm" {
    resource_group_name  = "rsg-terraform-state"
    storage_account_name = "sttfstate1234"  # YOUR storage account name
    container_name       = "terraform-state"
    key                  = "terraform.tfstate"
    # access_key is intentionally missing - injected at runtime
  }
}
```

**Why No Access Key?** We'll pass it via environment variable in the pipeline:
```bash
export ARM_ACCESS_KEY="$(sttfstate1234-key1)"
terraform init
```

This keeps the key out of Git forever.

### 4. `variables.tf`

```hcl
variable "subscription_id" {
  description = "Azure subscription ID"
  type        = string
}

variable "spn_client_id" {
  description = "Service principal client ID"
  type        = string
  sensitive   = true
}

variable "spn_client_secret" {
  description = "Service principal client secret"
  type        = string
  sensitive   = true
}

variable "spn_tenant_id" {
  description = "Azure AD tenant ID"
  type        = string
  sensitive   = true
}
```

**The `sensitive` Flag:** Prevents Terraform from logging these values in plan output.

### 5. Commit to Git

```bash
git add terraform/
git commit -m "Add Terraform configuration files"
git push origin main
```

## What's Next?

Part 2 covers:
- Creating the **Terraform Status Check** pipeline (runs on PRs)
- Creating the **Terraform Plan** pipeline (runs on merge)
- Configuring task steps (init, validate, plan, archive artifact)
- Linking variable groups to pipelines

## Key Takeaways

1. **One-time manual setup** - Storage account, Key Vault, service principal
2. **Secrets in Key Vault only** - Never in Git, never in DevOps variables
3. **Service connection bridges Azure DevOps to Azure** - Uses service principal
4. **Variable groups pull secrets at runtime** - Dynamic, secure, auditable
5. **Three pipelines serve different purposes** - Status check, plan, apply

This foundation enables secure, auditable, team-friendly infrastructure deployments. No more cowboy `terraform apply` from laptops.

---

**Next:** [Part 2 - Build Pipelines (Status Check & Terraform Plan)](/blog/terraform-azure-devops-cicd-part2-build-pipelines/)

*All code and pipeline configurations from this series are available in my [GitHub repo](https://github.com/dswann101164).*
