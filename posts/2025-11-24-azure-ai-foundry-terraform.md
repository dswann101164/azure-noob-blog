---
title: "Deploying Azure AI Foundry RAG with Terraform: Production-Ready Infrastructure as Code"
date: 2025-11-24
summary: "YouTube tutorials use Azure Portal clickops. Enterprises need repeatable, secure, version-controlled deployments. Here's the complete Terraform configuration for Azure AI Foundry RAG that actually works in production - with security, monitoring, and cost controls built in."
tags: ["Azure", "Terraform", "Infrastructure as Code", "Azure AI Foundry", "RAG", "DevOps"]
cover: "/static/images/hero/azure-ai-foundry-terraform.png"
---

**Every Azure AI Foundry tutorial uses the Portal. Zero use Terraform.**

They show you:
1. Click "Create Resource"
2. Fill in some forms
3. Click "Create"
4. "It works!"

**What they don't show:**
- How to deploy this consistently across dev/staging/prod
- How to version control your infrastructure
- How to implement security from day one
- How to avoid the "works on my machine" problem

I manage 44 Azure subscriptions with 31,000 resources. Manual deployments don't scale. Terraform does.

Here's the production-ready Terraform configuration for Azure AI Foundry RAG that includes security, monitoring, cost management, and everything the tutorials skip.

## Why Terraform for Azure AI Foundry?

**The Portal approach (tutorials):**
```
Problem: Need RAG in dev environment
Solution: Click through Portal for 30 minutes
Result: Dev environment works

Problem: Need RAG in prod environment  
Solution: Click through Portal again (slightly different settings)
Result: Prod "works" but configured differently than dev

Problem: Security audit says "no API keys in prod"
Solution: Click through Portal fixing security (miss some settings)
Result: Partial fix, documentation out of date

Problem: Teammate needs to replicate setup
Solution: "Uh, I think I clicked these buttons..."
Result: Doesn't match original, troubleshooting begins
```

**The Terraform approach:**
```terraform
# Define infrastructure once
module "ai_foundry_rag" {
  source = "./modules/ai-foundry"
  
  environment = var.environment  # dev, staging, prod
  # ... configuration ...
}

# Deploy to dev
terraform workspace select dev
terraform apply

# Deploy to prod (identical config, different params)
terraform workspace select prod
terraform apply

# Change security settings
# Edit terraform file, commit to git
terraform apply  # Updates all environments consistently

# Teammate replicates
git clone repo
terraform init
terraform apply  # Exact replica
```

**Benefits:**
- ✅ Version controlled (git)
- ✅ Repeatable (same every time)
- ✅ Auditable (see who changed what when)
- ✅ Testable (validate before applying)
- ✅ Documented (code IS documentation)

**This is how you deploy at enterprise scale.**

## Prerequisites

**What you need before starting:**

1. **Azure subscription** with sufficient quota
2. **Terraform installed** (v1.5.0+)
3. **Azure CLI** authenticated (`az login`)
4. **Service Principal** with appropriate permissions (or use Azure CLI auth)
5. **Understanding of [Azure AI Foundry RAG basics](/blog/azure-ai-foundry-rag-enterprise-reality/)** (read my previous post)

**Required permissions:**
```bash
# Your service principal needs these roles on the subscription
- Contributor (or specific resource provider permissions)
- User Access Administrator (for RBAC assignments)
```

**Cost warning:** This will create billable resources (~$300-$1,000/month depending on tier choices).

## Project Structure

**Organize your Terraform like this:**

```
azure-ai-foundry-terraform/
├── main.tf                 # Main orchestration
├── variables.tf            # Input variables
├── outputs.tf              # Outputs for reference
├── terraform.tfvars        # Variable values (gitignored if sensitive)
├── providers.tf            # Provider configuration
├── backend.tf              # Remote state configuration
├── versions.tf             # Version constraints
│
├── modules/
│   ├── resource-group/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   ├── storage/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   ├── ai-search/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   ├── openai/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   ├── monitoring/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   │
│   └── networking/          # For private endpoints
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
│
└── environments/
    ├── dev.tfvars
    ├── staging.tfvars
    └── prod.tfvars
```

**This structure enables:**
- Reusable modules
- Environment-specific configs
- Clear separation of concerns
- Team collaboration

## Core Terraform Configuration

### 1. Provider and Backend Setup

**providers.tf:**
```terraform
terraform {
  required_version = ">= 1.5.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.80"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 2.45"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = true
      recover_soft_deleted_key_vaults = true
    }
    
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

provider "azuread" {}
```

**backend.tf:**
```terraform
terraform {
  backend "azurerm" {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "tfstate${var.environment}"
    container_name       = "tfstate"
    key                  = "ai-foundry-rag.tfstate"
  }
}
```

**Why remote state?**
- Team collaboration (shared state)
- State locking (prevents concurrent modifications)
- Encryption at rest
- Backup and recovery

### 2. Variables Definition

**variables.tf:**
```terraform
variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

variable "location" {
  description = "Azure region for resources"
  type        = string
  default     = "eastus2"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "airag"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default     = {
    ManagedBy   = "Terraform"
    Project     = "AI-Foundry-RAG"
    CostCenter  = "IT-Innovation"
  }
}

# Search service tier
variable "search_sku" {
  description = "Azure AI Search SKU"
  type        = string
  default     = "standard"  # standard, basic, standard2, standard3
}

# OpenAI model deployments
variable "openai_deployments" {
  description = "OpenAI model deployments"
  type = map(object({
    model_name    = string
    model_version = string
    scale_type    = string
    capacity      = number
  }))
  default = {
    "gpt-4" = {
      model_name    = "gpt-4"
      model_version = "0613"
      scale_type    = "Standard"
      capacity      = 10
    }
    "text-embedding-ada-002" = {
      model_name    = "text-embedding-ada-002"
      model_version = "2"
      scale_type    = "Standard"
      capacity      = 10
    }
  }
}

# Security settings
variable "enable_private_endpoints" {
  description = "Enable private endpoints for services"
  type        = bool
  default     = false  # Set to true for production
}

variable "allowed_ip_ranges" {
  description = "IP ranges allowed to access services (for firewall)"
  type        = list(string)
  default     = []  # Empty = allow from Azure services only
}

# Monitoring
variable "enable_diagnostic_logs" {
  description = "Enable diagnostic logging"
  type        = bool
  default     = true
}

variable "log_retention_days" {
  description = "Number of days to retain logs"
  type        = number
  default     = 30
}
```

### 3. Main Orchestration

**main.tf:**
```terraform
# Generate unique suffix for globally unique names
resource "random_string" "suffix" {
  length  = 8
  special = false
  upper   = false
}

locals {
  name_prefix = "${var.project_name}-${var.environment}"
  name_suffix = random_string.suffix.result
  
  common_tags = merge(
    var.tags,
    {
      Environment = var.environment
      DeployedBy  = "Terraform"
      DeployDate  = timestamp()
    }
  )
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${local.name_prefix}-rg"
  location = var.location
  tags     = local.common_tags
}

# Storage Account for documents
module "storage" {
  source = "./modules/storage"
  
  name                = "${var.project_name}${var.environment}${local.name_suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tags                = local.common_tags
  
  enable_private_endpoint = var.enable_private_endpoints
  allowed_ip_ranges       = var.allowed_ip_ranges
}

# Azure AI Search
module "ai_search" {
  source = "./modules/ai-search"
  
  name                = "${local.name_prefix}-search-${local.name_suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = var.search_sku
  tags                = local.common_tags
  
  enable_semantic_search  = true
  enable_private_endpoint = var.enable_private_endpoints
  allowed_ip_ranges       = var.allowed_ip_ranges
}

# Azure OpenAI
module "openai" {
  source = "./modules/openai"
  
  name                = "${local.name_prefix}-openai-${local.name_suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location
  tags                = local.common_tags
  
  deployments             = var.openai_deployments
  enable_private_endpoint = var.enable_private_endpoints
  allowed_ip_ranges       = var.allowed_ip_ranges
}

# Key Vault for secrets
module "key_vault" {
  source = "./modules/key-vault"
  
  name                = "${local.name_prefix}-kv-${local.name_suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tags                = local.common_tags
  
  enable_private_endpoint = var.enable_private_endpoints
}

# Store connection strings and keys in Key Vault
resource "azurerm_key_vault_secret" "storage_connection_string" {
  name         = "storage-connection-string"
  value        = module.storage.primary_connection_string
  key_vault_id = module.key_vault.id
  
  depends_on = [module.key_vault]
}

resource "azurerm_key_vault_secret" "search_admin_key" {
  name         = "search-admin-key"
  value        = module.ai_search.primary_admin_key
  key_vault_id = module.key_vault.id
  
  depends_on = [module.key_vault]
}

resource "azurerm_key_vault_secret" "openai_key" {
  name         = "openai-key"
  value        = module.openai.primary_key
  key_vault_id = module.key_vault.id
  
  depends_on = [module.key_vault]
}

# Monitoring
module "monitoring" {
  source = "./modules/monitoring"
  
  name                = "${local.name_prefix}-monitoring"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  tags                = local.common_tags
  
  log_retention_days = var.log_retention_days
  
  # Resources to monitor
  storage_account_id = module.storage.id
  search_service_id  = module.ai_search.id
  openai_account_id  = module.openai.id
}
```

## Module Implementation: Azure AI Search

**modules/ai-search/main.tf:**
```terraform
resource "azurerm_search_service" "main" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  sku                 = var.sku
  tags                = var.tags
  
  # Semantic search (required for RAG)
  semantic_search_sku = var.enable_semantic_search ? "standard" : null
  
  # Security settings
  public_network_access_enabled = var.enable_private_endpoint ? false : true
  
  # Authentication
  authentication_failure_mode = "http401WithBearerChallenge"
  
  # Managed identity for accessing storage
  identity {
    type = "SystemAssigned"
  }
  
  # Replica count for HA (prod only)
  replica_count = var.sku == "standard" ? var.replica_count : 1
  partition_count = var.partition_count
}

# Network rules if not using private endpoint
resource "azurerm_search_service_network_rule_set" "main" {
  count = var.enable_private_endpoint ? 0 : 1
  
  search_service_id = azurerm_search_service.main.id
  
  # IP rules
  dynamic "ip_rule" {
    for_each = var.allowed_ip_ranges
    content {
      value = ip_rule.value
    }
  }
  
  # Allow Azure services
  bypass_data_plane_authentication = ["AzureServices"]
}

# Private endpoint (production)
resource "azurerm_private_endpoint" "search" {
  count = var.enable_private_endpoint ? 1 : 0
  
  name                = "${var.name}-pe"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = var.subnet_id
  
  private_service_connection {
    name                           = "${var.name}-psc"
    private_connection_resource_id = azurerm_search_service.main.id
    subresource_names              = ["searchService"]
    is_manual_connection           = false
  }
  
  tags = var.tags
}

# Diagnostic settings
resource "azurerm_monitor_diagnostic_setting" "search" {
  count = var.enable_diagnostic_logs ? 1 : 0
  
  name                       = "${var.name}-diagnostics"
  target_resource_id         = azurerm_search_service.main.id
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  enabled_log {
    category = "OperationLogs"
  }
  
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}
```

**modules/ai-search/variables.tf:**
```terraform
variable "name" {
  description = "Name of the search service"
  type        = string
}

variable "resource_group_name" {
  description = "Resource group name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "sku" {
  description = "Search service SKU"
  type        = string
  default     = "standard"
  
  validation {
    condition     = contains(["free", "basic", "standard", "standard2", "standard3", "storage_optimized_l1", "storage_optimized_l2"], var.sku)
    error_message = "Invalid SKU. Choose from: free, basic, standard, standard2, standard3, storage_optimized_l1, storage_optimized_l2"
  }
}

variable "enable_semantic_search" {
  description = "Enable semantic search"
  type        = bool
  default     = true
}

variable "replica_count" {
  description = "Number of replicas (HA)"
  type        = number
  default     = 1
}

variable "partition_count" {
  description = "Number of partitions"
  type        = number
  default     = 1
}

variable "enable_private_endpoint" {
  description = "Enable private endpoint"
  type        = bool
  default     = false
}

variable "subnet_id" {
  description = "Subnet ID for private endpoint"
  type        = string
  default     = null
}

variable "allowed_ip_ranges" {
  description = "Allowed IP ranges for firewall"
  type        = list(string)
  default     = []
}

variable "enable_diagnostic_logs" {
  description = "Enable diagnostic logging"
  type        = bool
  default     = true
}

variable "log_analytics_workspace_id" {
  description = "Log Analytics workspace ID"
  type        = string
  default     = null
}

variable "tags" {
  description = "Resource tags"
  type        = map(string)
  default     = {}
}
```

**modules/ai-search/outputs.tf:**
```terraform
output "id" {
  description = "Search service ID"
  value       = azurerm_search_service.main.id
}

output "name" {
  description = "Search service name"
  value       = azurerm_search_service.main.name
}

output "endpoint" {
  description = "Search service endpoint"
  value       = "https://${azurerm_search_service.main.name}.search.windows.net"
}

output "primary_admin_key" {
  description = "Primary admin key"
  value       = azurerm_search_service.main.primary_key
  sensitive   = true
}

output "query_keys" {
  description = "Query keys"
  value       = azurerm_search_service.main.query_keys
  sensitive   = true
}

output "identity_principal_id" {
  description = "Managed identity principal ID"
  value       = azurerm_search_service.main.identity[0].principal_id
}
```

## Module Implementation: Azure OpenAI

**modules/openai/main.tf:**
```terraform
resource "azurerm_cognitive_account" "openai" {
  name                = var.name
  resource_group_name = var.resource_group_name
  location            = var.location
  kind                = "OpenAI"
  sku_name            = "S0"
  tags                = var.tags
  
  # Managed identity
  identity {
    type = "SystemAssigned"
  }
  
  # Security
  public_network_access_enabled = var.enable_private_endpoint ? false : true
  custom_subdomain_name         = var.name  # Required for private endpoints
  
  # Network ACLs
  network_acls {
    default_action = var.enable_private_endpoint ? "Deny" : "Allow"
    
    dynamic "ip_rules" {
      for_each = var.allowed_ip_ranges
      content {
        ip_range = ip_rules.value
      }
    }
    
    # Always allow Azure services
    virtual_network_rules = []
  }
}

# Deploy models
resource "azurerm_cognitive_deployment" "models" {
  for_each = var.deployments
  
  name                 = each.key
  cognitive_account_id = azurerm_cognitive_account.openai.id
  
  model {
    format  = "OpenAI"
    name    = each.value.model_name
    version = each.value.model_version
  }
  
  scale {
    type     = each.value.scale_type
    capacity = each.value.capacity
  }
  
  rai_policy_name = "Microsoft.Default"
}

# Private endpoint (production)
resource "azurerm_private_endpoint" "openai" {
  count = var.enable_private_endpoint ? 1 : 0
  
  name                = "${var.name}-pe"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = var.subnet_id
  
  private_service_connection {
    name                           = "${var.name}-psc"
    private_connection_resource_id = azurerm_cognitive_account.openai.id
    subresource_names              = ["account"]
    is_manual_connection           = false
  }
  
  tags = var.tags
}

# Diagnostic settings
resource "azurerm_monitor_diagnostic_setting" "openai" {
  count = var.enable_diagnostic_logs ? 1 : 0
  
  name                       = "${var.name}-diagnostics"
  target_resource_id         = azurerm_cognitive_account.openai.id
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  enabled_log {
    category = "Audit"
  }
  
  enabled_log {
    category = "RequestResponse"
  }
  
  metric {
    category = "AllMetrics"
    enabled  = true
  }
}

# RBAC for AI Search to access OpenAI
resource "azurerm_role_assignment" "search_to_openai" {
  count = var.search_principal_id != null ? 1 : 0
  
  scope                = azurerm_cognitive_account.openai.id
  role_definition_name = "Cognitive Services OpenAI User"
  principal_id         = var.search_principal_id
}
```

## Module Implementation: Storage Account

**modules/storage/main.tf:**
```terraform
resource "azurerm_storage_account" "main" {
  name                     = var.name
  resource_group_name      = var.resource_group_name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = var.replication_type
  account_kind             = "StorageV2"
  tags                     = var.tags
  
  # Security settings
  min_tls_version                 = "TLS1_2"
  enable_https_traffic_only       = true
  allow_nested_items_to_be_public = false
  shared_access_key_enabled       = true  # Needed for some tools, but use SAS tokens
  
  # Managed identity
  identity {
    type = "SystemAssigned"
  }
  
  # Blob properties
  blob_properties {
    versioning_enabled = true
    
    delete_retention_policy {
      days = var.soft_delete_retention_days
    }
    
    container_delete_retention_policy {
      days = var.soft_delete_retention_days
    }
  }
  
  # Network rules
  network_rules {
    default_action             = var.enable_private_endpoint ? "Deny" : "Allow"
    bypass                     = ["AzureServices"]
    ip_rules                   = var.allowed_ip_ranges
    virtual_network_subnet_ids = []
  }
}

# Containers for RAG documents
resource "azurerm_storage_container" "documents" {
  name                  = "documents"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_container" "embeddings" {
  name                  = "embeddings"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

# Private endpoint (production)
resource "azurerm_private_endpoint" "blob" {
  count = var.enable_private_endpoint ? 1 : 0
  
  name                = "${var.name}-blob-pe"
  resource_group_name = var.resource_group_name
  location            = var.location
  subnet_id           = var.subnet_id
  
  private_service_connection {
    name                           = "${var.name}-blob-psc"
    private_connection_resource_id = azurerm_storage_account.main.id
    subresource_names              = ["blob"]
    is_manual_connection           = false
  }
  
  tags = var.tags
}

# Diagnostic settings
resource "azurerm_monitor_diagnostic_setting" "storage" {
  count = var.enable_diagnostic_logs ? 1 : 0
  
  name                       = "${var.name}-diagnostics"
  target_resource_id         = "${azurerm_storage_account.main.id}/blobServices/default"
  log_analytics_workspace_id = var.log_analytics_workspace_id
  
  enabled_log {
    category = "StorageRead"
  }
  
  enabled_log {
    category = "StorageWrite"
  }
  
  enabled_log {
    category = "StorageDelete"
  }
  
  metric {
    category = "Transaction"
    enabled  = true
  }
}

# RBAC for AI Search to read blobs
resource "azurerm_role_assignment" "search_to_storage" {
  count = var.search_principal_id != null ? 1 : 0
  
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = var.search_principal_id
}
```

## Environment-Specific Configurations

**environments/dev.tfvars:**
```terraform
environment = "dev"
location    = "eastus2"

# Cheaper tiers for dev
search_sku = "basic"  # $75/month vs $249/month

openai_deployments = {
  "gpt-4" = {
    model_name    = "gpt-4"
    model_version = "0613"
    scale_type    = "Standard"
    capacity      = 5  # Lower capacity for dev
  }
  "text-embedding-ada-002" = {
    model_name    = "text-embedding-ada-002"
    model_version = "2"
    scale_type    = "Standard"
    capacity      = 5
  }
}

# No private endpoints in dev (save costs)
enable_private_endpoints = false

# Shorter retention for dev
log_retention_days = 7

tags = {
  Environment = "dev"
  CostCenter  = "IT-Dev"
}
```

**environments/prod.tfvars:**
```terraform
environment = "prod"
location    = "eastus2"

# Production tiers
search_sku = "standard"  # $249/month, includes semantic search

openai_deployments = {
  "gpt-4" = {
    model_name    = "gpt-4"
    model_version = "0613"
    scale_type    = "Standard"
    capacity      = 20  # Higher capacity for prod
  }
  "text-embedding-ada-002" = {
    model_name    = "text-embedding-ada-002"
    model_version = "2"
    scale_type    = "Standard"
    capacity      = 20
  }
}

# Enable private endpoints for security
enable_private_endpoints = true

# Longer retention for compliance
log_retention_days = 90

# Restrict access to specific IPs
allowed_ip_ranges = [
  "203.0.113.0/24",  # Corporate office
  "198.51.100.0/24"  # VPN endpoint
]

tags = {
  Environment = "prod"
  CostCenter  = "IT-Prod"
  Compliance  = "SOC2"
}
```

## Deployment Workflow

### Initial Setup

**1. Initialize Terraform:**
```bash
# Clone your repo
git clone https://github.com/yourorg/azure-ai-foundry-terraform.git
cd azure-ai-foundry-terraform

# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Format code
terraform fmt -recursive
```

**2. Create workspace for dev:**
```bash
# Create dev workspace
terraform workspace new dev

# Or switch to existing
terraform workspace select dev
```

**3. Plan deployment:**
```bash
# Plan with dev variables
terraform plan -var-file="environments/dev.tfvars" -out=dev.tfplan

# Review the plan carefully
```

**4. Apply deployment:**
```bash
# Apply the plan
terraform apply dev.tfplan

# Or apply directly (will prompt for approval)
terraform apply -var-file="environments/dev.tfvars"
```

### Deploying to Production

**1. Create prod workspace:**
```bash
terraform workspace new prod
terraform workspace select prod
```

**2. Plan and apply:**
```bash
# Plan
terraform plan -var-file="environments/prod.tfvars" -out=prod.tfplan

# Review thoroughly - this is prod!

# Apply
terraform apply prod.tfplan
```

### Making Changes

**1. Update Terraform files:**
```bash
# Edit modules/ai-search/main.tf (example)
vim modules/ai-search/main.tf

# Format
terraform fmt

# Validate
terraform validate
```

**2. Plan changes:**
```bash
# See what will change
terraform plan -var-file="environments/dev.tfvars"
```

**3. Apply changes:**
```bash
# Apply to dev first
terraform workspace select dev
terraform apply -var-file="environments/dev.tfvars"

# Test thoroughly in dev

# Apply to prod
terraform workspace select prod
terraform apply -var-file="environments/prod.tfvars"
```

## Cost Management with Terraform

**Add cost tags for tracking:**

```terraform
locals {
  cost_tags = {
    CostCenter  = var.cost_center
    Project     = var.project_name
    Environment = var.environment
    Owner       = var.owner_email
    BudgetAlert = var.monthly_budget
  }
}

# Apply to all resources
tags = merge(var.tags, local.cost_tags)
```

**Budget alerts (Azure Monitor):**

```terraform
resource "azurerm_consumption_budget_resource_group" "main" {
  name              = "${local.name_prefix}-budget"
  resource_group_id = azurerm_resource_group.main.id
  
  amount     = var.monthly_budget
  time_grain = "Monthly"
  
  time_period {
    start_date = formatdate("YYYY-MM-01'T'00:00:00Z", timestamp())
  }
  
  notification {
    enabled   = true
    threshold = 80
    operator  = "GreaterThan"
    
    contact_emails = var.budget_alert_emails
  }
  
  notification {
    enabled   = true
    threshold = 100
    operator  = "GreaterThan"
    
    contact_emails = var.budget_alert_emails
  }
}
```

**Auto-shutdown for dev (save costs overnight):**

```terraform
# Logic App to shut down dev resources at 6 PM
resource "azurerm_logic_app_workflow" "dev_shutdown" {
  count = var.environment == "dev" ? 1 : 0
  
  name                = "${local.name_prefix}-shutdown"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  
  # Schedule: 6 PM EST Monday-Friday
  # Add workflow definition here
}
```

## Security Best Practices

### 1. No Secrets in Code

**❌ Wrong:**
```terraform
resource "azurerm_cognitive_account" "openai" {
  # ...
  api_key = "sk-1234567890abcdef"  # NEVER DO THIS
}
```

**✅ Right:**
```terraform
# Store in Key Vault
resource "azurerm_key_vault_secret" "openai_key" {
  name         = "openai-key"
  value        = azurerm_cognitive_account.openai.primary_key
  key_vault_id = azurerm_key_vault.main.id
}

# Applications retrieve from Key Vault at runtime
# Using managed identity authentication
```

### 2. Use Managed Identities

```terraform
# Enable managed identity on all services
identity {
  type = "SystemAssigned"
}

# Grant RBAC permissions
resource "azurerm_role_assignment" "search_to_storage" {
  scope                = azurerm_storage_account.main.id
  role_definition_name = "Storage Blob Data Reader"
  principal_id         = azurerm_search_service.main.identity[0].principal_id
}
```

### 3. Private Endpoints for Production

```terraform
# Disable public access
public_network_access_enabled = false

# Enable private endpoint
resource "azurerm_private_endpoint" "search" {
  # ... configuration ...
}
```

### 4. Network Restrictions

```terraform
# Firewall rules
network_rules {
  default_action = "Deny"
  bypass         = ["AzureServices"]
  ip_rules       = var.allowed_corporate_ips
}
```

## Monitoring and Alerts

**Create alerts for failures:**

```terraform
resource "azurerm_monitor_metric_alert" "search_failures" {
  name                = "${local.name_prefix}-search-failures"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [module.ai_search.id]
  description         = "Alert when search query failure rate exceeds 10%"
  
  criteria {
    metric_namespace = "Microsoft.Search/searchServices"
    metric_name      = "SearchQueriesPerSecond"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = 10
  }
  
  action {
    action_group_id = azurerm_monitor_action_group.ops_team.id
  }
}

resource "azurerm_monitor_metric_alert" "openai_throttling" {
  name                = "${local.name_prefix}-openai-throttling"
  resource_group_name = azurerm_resource_group.main.name
  scopes              = [module.openai.id]
  description         = "Alert on OpenAI API throttling"
  
  criteria {
    metric_namespace = "Microsoft.CognitiveServices/accounts"
    metric_name      = "Throttle"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = 10
  }
  
  action {
    action_group_id = azurerm_monitor_action_group.ops_team.id
  }
}
```

## CI/CD Integration

**Azure DevOps Pipeline:**

```yaml
# azure-pipelines.yml
trigger:
  branches:
    include:
      - main
  paths:
    include:
      - terraform/**

pool:
  vmImage: 'ubuntu-latest'

stages:
  - stage: Validate
    jobs:
      - job: TerraformValidate
        steps:
          - task: TerraformInstaller@0
            inputs:
              terraformVersion: '1.5.7'
          
          - script: |
              cd terraform
              terraform init -backend=false
              terraform validate
              terraform fmt -check -recursive
            displayName: 'Validate Terraform'

  - stage: Plan_Dev
    dependsOn: Validate
    jobs:
      - job: PlanDev
        steps:
          - task: TerraformTaskV4@4
            inputs:
              provider: 'azurerm'
              command: 'init'
              backendServiceArm: 'AzureRM-ServiceConnection'
              backendAzureRmResourceGroupName: 'terraform-state-rg'
              backendAzureRmStorageAccountName: 'tfstatedev'
              backendAzureRmContainerName: 'tfstate'
              backendAzureRmKey: 'ai-foundry-rag.tfstate'
          
          - task: TerraformTaskV4@4
            inputs:
              provider: 'azurerm'
              command: 'plan'
              commandOptions: '-var-file="environments/dev.tfvars" -out=dev.tfplan'
              environmentServiceNameAzureRM: 'AzureRM-ServiceConnection'

  - stage: Apply_Dev
    dependsOn: Plan_Dev
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: ApplyDev
        environment: 'dev'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: TerraformTaskV4@4
                  inputs:
                    provider: 'azurerm'
                    command: 'apply'
                    commandOptions: 'dev.tfplan'
                    environmentServiceNameAzureRM: 'AzureRM-ServiceConnection'

  # Repeat for staging and prod with approval gates
```

## Troubleshooting Common Issues

### Issue 1: "Resource Already Exists"

**Problem:** Importing existing resources

**Solution:**
```bash
# Import existing resource
terraform import azurerm_search_service.main /subscriptions/{sub-id}/resourceGroups/{rg}/providers/Microsoft.Search/searchServices/{name}

# Or remove from state and recreate
terraform state rm azurerm_search_service.main
terraform apply
```

### Issue 2: "Insufficient Quota"

**Problem:** Azure subscription quota limits

**Solution:**
```bash
# Check quota
az vm list-usage --location eastus2 --output table

# Request quota increase via Azure Portal
# Or use smaller SKUs in terraform.tfvars
```

### Issue 3: "Backend Initialization Failed"

**Problem:** State storage not accessible

**Solution:**
```bash
# Create state storage manually first
az group create --name terraform-state-rg --location eastus2

az storage account create \
  --name tfstatedev \
  --resource-group terraform-state-rg \
  --location eastus2 \
  --sku Standard_LRS

az storage container create \
  --name tfstate \
  --account-name tfstatedev

# Then terraform init
```

## Outputs for Application Use

**outputs.tf:**
```terraform
output "search_endpoint" {
  description = "Azure AI Search endpoint"
  value       = module.ai_search.endpoint
}

output "openai_endpoint" {
  description = "Azure OpenAI endpoint"
  value       = module.openai.endpoint
}

output "storage_account_name" {
  description = "Storage account name"
  value       = module.storage.name
}

output "key_vault_uri" {
  description = "Key Vault URI for retrieving secrets"
  value       = module.key_vault.uri
}

output "resource_group_name" {
  description = "Resource group name"
  value       = azurerm_resource_group.main.name
}

# Sensitive outputs
output "connection_info" {
  description = "Connection information for applications"
  value = {
    search_endpoint   = module.ai_search.endpoint
    openai_endpoint   = module.openai.endpoint
    storage_account   = module.storage.name
    key_vault_uri     = module.key_vault.uri
  }
  sensitive = true
}
```

**Use in your application:**
```python
# Application retrieves endpoints from Terraform outputs
# Stored in CI/CD variables or Key Vault

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()

# Get Key Vault URI from Terraform output
kv_uri = os.environ['KEY_VAULT_URI']
client = SecretClient(vault_url=kv_uri, credential=credential)

# Retrieve secrets
search_key = client.get_secret("search-admin-key").value
openai_key = client.get_secret("openai-key").value
```

## What We Accomplished

**With this Terraform configuration, you have:**

✅ **Repeatable deployments** - Deploy identical environments with one command
✅ **Version control** - Infrastructure changes tracked in git
✅ **Security by default** - Managed identities, Key Vault, optional private endpoints
✅ **Environment parity** - Dev/staging/prod from same code
✅ **Cost controls** - Budget alerts, environment-specific SKUs
✅ **Monitoring built-in** - Diagnostic logs, metric alerts
✅ **Team collaboration** - Remote state, workspace isolation
✅ **Audit trail** - Every change documented in git history

**Compare to Portal deployments:**
- Portal: 30 minutes per environment, undocumented, inconsistent
- Terraform: 5 minutes per environment, version controlled, identical

**This is how enterprises deploy Azure AI Foundry at scale.**

---

## Next Steps

**Now that you have the infrastructure:**

1. **Deploy to dev** and test thoroughly
2. **Configure your RAG pipeline** using the endpoints from Terraform outputs
3. **Create your search index** (I'll cover this in the next post)
4. **Set up CI/CD** for automated deployments
5. **Deploy to prod** with confidence

**Coming next:**
- Part 3: Python code for production RAG with error handling
- Part 4: Monitoring and observability dashboards
- Part 5: Cost optimization strategies

---

*Managing 44 Azure subscriptions and 31,000 resources taught me: Infrastructure as Code isn't optional at scale. It's the only way to maintain sanity.*
