---
title: "SOC 2 Audit Prep Part 2: Azure AD Audit Log Retention Setup (Step-by-Step)"
date: 2025-10-27
summary: "The grill assembly manual for capturing Azure AD audit logs - app registrations, consent grants, sign-ins, and role assignments. Every click, every command, every verification. Part 2 of fixing the 90-day audit gap."
tags: ["azure", "Compliance", "Auditing", "Azure AD", "Entra ID", "Security", "SOC 2"]
cover: "/static/images/hero/azure-ad-audit-logs.svg"
hub: governance
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
---
## What This Is


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

This is Part 2 of fixing the Azure audit gap. **[Part 1 covered Activity Logs](/blog/2025-10-27-soc2-activity-log-step-by-step/)** (ARM resources like VMs and storage accounts). This post covers **Azure AD Audit Logs** (identity layer: app registrations, consent grants, sign-ins, role assignments).

Same format: every click, every command, every field. Grill assembly manual level detail.

**What you'll configure:**
- Azure AD diagnostic settings export
- Five separate log categories (AuditLogs, SignInLogs, etc.)
- Long-term retention in Log Analytics Workspace
- Archive to Storage Account
- Verification queries to prove it's working
- App registration tracking (external spreadsheet)

**Time required:** 45-60 minutes

**Cost:** $50-200/month (depending on user count and sign-in volume)

## Who This Is For

You need this if:

- You get Tenable alerts about "unused app registrations"
- Security asks "who granted admin consent to this app?"
- Auditors want to see sign-in activity from 6 months ago
- You can't answer "who created this app registration?"
- You're preparing for SOC 2, HIPAA, PCI-DSS, or similar audits
- Your Azure AD logs only go back 30 days (the default)

**Critical context:** Azure AD logs are SEPARATE from Activity Logs. You're not done after Part 1. You need both.

## Prerequisites

Before you start:

1. **Azure AD Premium P1 or P2 license** (REQUIRED)
   - Check: Azure Portal → Azure Active Directory → Licenses
   - If you see "Free" tier → You can't export Azure AD logs
   - You need at least one P1 license to unlock diagnostic settings

2. **Log Analytics Workspace** (from Part 1)
   - If you completed Part 1, reuse the same workspace
   - If you're starting here, create one first (instructions below)

3. **Permissions Required:**
   - Global Administrator OR
   - Security Administrator + Log Analytics Contributor

4. **Storage Account** (optional but recommended)
   - For long-term archive (7 years)
   - Can reuse from Part 1

**License check:**
```powershell
# Check your Azure AD license tier
Connect-AzureAD
Get-AzureADSubscribedSku | Select-Object SkuPartNumber, ConsumedUnits

# Look for:
# - AAD_PREMIUM or AAD_PREMIUM_P1 → You're good
# - AAD_PREMIUM2 → Even better
# - AAD_BASIC or AAD_FREE → Can't export Azure AD logs
```

**If you don't have Azure AD Premium:** Stop here. Talk to procurement. You CANNOT export Azure AD diagnostic logs without it. This is a hard requirement.

## The Five Log Categories (What You're Capturing)

Azure AD has five separate log types. Here's what each one captures and why you need it:

### 1. AuditLogs - The "Who Did What" Log

**What it captures:**
- App registration creation/deletion/modification
- Service principal changes
- User/group creation and updates
- Admin role assignments
- Directory settings changes
- Policy modifications

**Why you need it:**
- Answers "who created this app registration?"
- Tracks admin role grants
- Documents consent grants
- Shows configuration changes

**Example audit question:** "Who added John Doe to Global Administrator role?"

### 2. SignInLogs - User Authentication Events

**What it captures:**
- Interactive user sign-ins (username/password)
- Failed login attempts
- Multi-factor authentication events
- Conditional Access policy evaluations
- Device compliance checks

**Why you need it:**
- Tracks user access patterns
- Identifies brute force attempts
- Validates MFA enforcement
- Documents access from specific locations/devices

**Example audit question:** "Show me all sign-ins from Russia in the last 90 days"

### 3. NonInteractiveUserSignInLogs - Background Authentication

**What it captures:**
- Token refresh events (user not typing password)
- Background authentication for apps
- Delegated permission flows
- Modern auth token exchanges

**Why you need it:**
- Tracks how apps use delegated permissions
- Shows background access patterns
- Identifies token-based access

**Example audit question:** "Is this user's token still being used after offboarding?"

### 4. ServicePrincipalSignInLogs - App Registration Usage

**What it captures:**
- Service principal authentication (client credentials flow)
- App registration sign-ins
- Managed identity authentication
- Application access to Azure resources

**Why you need it:**
- **THIS IS THE BIG ONE FOR APP REGISTRATIONS**
- Answers "is this app registration actually being used?"
- Tracks which resources an app accesses
- Documents app behavior

**Example audit question:** "Has this app registration been used in the last 90 days?"

### 5. ManagedIdentitySignInLogs - System Identities

**What it captures:**
- Managed identity authentication events
- System-assigned identity access
- User-assigned identity access

**Why you need it:**
- Tracks managed identity usage
- Documents zero-credential access patterns
- Validates least privilege enforcement

**Example audit question:** "What resources does this managed identity access?"

**The reality:** You need ALL FIVE. Don't pick and choose. Enable all of them.

## Step 1: Create Log Analytics Workspace (If You Don't Have One)

If you completed Part 1, **skip this section** and reuse your existing workspace.

If you're starting here:

### Portal Method

**1. Navigate to Log Analytics Workspaces**

- Azure Portal → Search bar → Type "Log Analytics workspaces"
- Click **Log Analytics workspaces** (the service, not a specific workspace)

**2. Click "+ Create"**

Top left corner. Blue button. Click it.

**3. Fill in the basics:**

| Field | What To Enter | Why |
|-------|---------------|-----|
| **Subscription** | Your production subscription | Where the workspace will be billed |
| **Resource Group** | `governance-rg` or `security-rg` | Logical grouping for audit resources |
| **Name** | `audit-logs-workspace` | Clear naming convention |
| **Region** | Same as your resources | Reduces egress costs |

**4. Click "Review + create"**

Skip the Tags tab unless you have required tags.

**5. Click "Create"**

Wait 2-3 minutes for deployment.

**6. Write down the Workspace ID**

After deployment:
- Click "Go to resource"
- Left menu → **Properties**
- Copy the **Resource ID** (long path starting with `/subscriptions/...`)
- Save it. You'll need it in the next step.

### PowerShell Method (Faster)

```powershell
# Set variables
$resourceGroup = "governance-rg"
$workspaceName = "audit-logs-workspace"
$location = "eastus"  # Change to your region
$retentionDays = 730  # 2 years

# Create resource group if it doesn't exist
New-AzResourceGroup -Name $resourceGroup -Location $location -Force

# Create workspace
$workspace = New-AzOperationalInsightsWorkspace `
    -ResourceGroupName $resourceGroup `
    -Name $workspaceName `
    -Location $location `
    -RetentionInDays $retentionDays `
    -Sku "PerGB2018"

# Show workspace ID (save this)
Write-Host "Workspace ID: $($workspace.ResourceId)" -ForegroundColor Green

# Show workspace key (for API access if needed)
$workspaceKey = Get-AzOperationalInsightsWorkspaceSharedKey `
    -ResourceGroupName $resourceGroup `
    -Name $workspaceName

Write-Host "Workspace Key: $($workspaceKey.PrimarySharedKey)" -ForegroundColor Yellow
```

**Verification:**

```powershell
# Verify workspace exists and is active
Get-AzOperationalInsightsWorkspace `
    -ResourceGroupName $resourceGroup `
    -Name $workspaceName | 
    Select-Object Name, Location, Sku, RetentionInDays, ProvisioningState

# Expected output:
# Name                   : audit-logs-workspace
# Location               : eastus
# Sku                    : PerGB2018
# RetentionInDays        : 730
# ProvisioningState      : Succeeded
```

## Step 2: Configure Azure AD Diagnostic Settings

This is where we export Azure AD logs to the workspace.

### Portal Method

**1. Navigate to Azure Active Directory**

- Azure Portal → Search bar → Type "Azure Active Directory"
- Click **Azure Active Directory** (NOT "Azure AD users" or other sub-services)

**2. Find Diagnostic Settings**

- Left menu → **Monitoring** section
- Click **Diagnostic settings**

**What you see:**
- A list of diagnostic settings (probably empty)
- A note: "Requires Azure AD Premium P1 or P2"
- If you see "This feature requires premium licenses" → Stop. You don't have the right license.

**3. Click "+ Add diagnostic setting"**

Top of the page.

**4. Name your setting:**

| Field | What To Enter |
|-------|---------------|
| **Diagnostic setting name** | `export-azuread-to-law` |

Clear naming. You'll see this in automation scripts later.

**5. Select ALL FIVE log categories:**

Check these boxes:

- ☑ **AuditLogs**
- ☑ **SignInLogs**
- ☑ **NonInteractiveUserSignInLogs**
- ☑ **ServicePrincipalSignInLogs**
- ☑ **ManagedIdentitySignInLogs**

**Why all five?** Because you don't know which log will answer tomorrow's audit question. Enable them all.

**6. Select destination:**

Under "Destination details":

- ☑ **Send to Log Analytics workspace**

**Workspace selection:**
- Subscription: (should auto-select your current subscription)
- Log Analytics workspace: Select `audit-logs-workspace`

**7. (Optional) Add Storage Account for long-term archive:**

If you want 7-year retention:

- ☑ **Archive to a storage account**
- Storage account: Select your audit storage account
- Retention (days): **2555** (7 years)

**8. Click "Save"**

Top of the page.

**Wait 5-10 minutes.** Logs don't appear instantly. Azure needs to start the export pipeline.

### PowerShell Method (Recommended for Automation)

This requires Microsoft Graph PowerShell module:

```powershell
# Install Microsoft Graph module (if not already installed)
Install-Module Microsoft.Graph -Scope CurrentUser -Force

# Connect with required permissions
Connect-MgGraph -Scopes "AuditLog.Read.All","Directory.Read.All"

# Set variables
$workspaceResourceId = "/subscriptions/YOUR-SUB-ID/resourceGroups/governance-rg/providers/Microsoft.OperationalInsights/workspaces/audit-logs-workspace"

# Get current tenant ID
$tenantId = (Get-MgContext).TenantId

# Define diagnostic setting
$diagnosticSetting = @{
    name = "export-azuread-to-law"
    workspaceId = $workspaceResourceId
    logs = @(
        @{ category = "AuditLogs"; enabled = $true }
        @{ category = "SignInLogs"; enabled = $true }
        @{ category = "NonInteractiveUserSignInLogs"; enabled = $true }
        @{ category = "ServicePrincipalSignInLogs"; enabled = $true }
        @{ category = "ManagedIdentitySignInLogs"; enabled = $true }
    )
}

# Apply diagnostic setting
# Note: This uses REST API because there's no direct PowerShell cmdlet yet
$uri = "https://graph.microsoft.com/beta/auditLogs/directoryAudits/diagnosticSettings"

Invoke-MgGraphRequest -Method POST -Uri $uri -Body ($diagnosticSetting | ConvertTo-Json -Depth 10)

Write-Host "Azure AD diagnostic settings configured successfully!" -ForegroundColor Green
```

**If you get "Insufficient privileges":**

```powershell
# You need Global Administrator or Security Administrator role
# Check your role:
Get-MgUserMemberOf -UserId (Get-MgContext).Account | 
    Select-Object AdditionalProperties

# If you don't have the right role, ask someone who does to run this script
```

### Azure CLI Method (Alternative)

```bash
# Login
az login

# Get workspace ID
workspaceId=$(az monitor log-analytics workspace show \
    --resource-group governance-rg \
    --workspace-name audit-logs-workspace \
    --query id -o tsv)

# Note: Azure CLI doesn't fully support Azure AD diagnostic settings yet
# Use Portal or PowerShell for now
# This is a known limitation as of October 2025
```


---

## CRITICAL: Verify Your Configuration (Before Testing Queries)

**The problem your screenshot revealed:** The diagnostic settings list view shows a setting exists, but doesn't prove what categories are enabled.

### Step 2a: Verify Categories Are Actually Enabled

**Don't trust the list view.** You need to click "Edit setting" to see the actual configuration.

**Portal verification (DO THIS NOW):**

1. Navigate to your diagnostic settings:
   - **For Activity Logs:** Monitor → Activity Log → Diagnostic settings
   - **For Azure AD:** Azure Active Directory → Diagnostic settings

2. You'll see your diagnostic setting in a table (like "soc2-activity-logs" or "export-azuread-to-law")

3. **Click on the setting name** (not Edit, just click the name to open it)

4. **Scroll to the Logs section** and verify checkboxes:

**For Activity Logs - ALL 8 must be checked:**
```
☑ Administrative
☑ Security
☑ ServiceHealth
☑ Alert
☑ Recommendation
☑ Policy
☑ Autoscale
☑ ResourceHealth
```

**For Azure AD - ALL 5 must be checked:**
```
☑ AuditLogs
☑ SignInLogs
☑ NonInteractiveUserSignInLogs
☑ ServicePrincipalSignInLogs
☑ ManagedIdentitySignInLogs
```

5. **Verify destination** shows your Log Analytics workspace

6. **Take a screenshot of this screen** - This is what auditors want, not the list view

**If any boxes are unchecked:**
- Click "Edit"
- Check the missing boxes
- Click "Save"
- Wait 15 minutes
- Recheck

### PowerShell Verification (Proves Configuration)

This exports exactly what's configured - run this and save the output:

**For Activity Logs:**
```powershell
# Get subscription diagnostic settings
$subscriptionId = (Get-AzContext).Subscription.Id
$diagnosticSettings = Get-AzDiagnosticSetting -ResourceId "/subscriptions/$subscriptionId"

# Show what's actually configured
foreach ($setting in $diagnosticSettings) {
    Write-Host "`n=== Diagnostic Setting: $($setting.Name) ===" -ForegroundColor Cyan
    
    Write-Host "`nEnabled Categories:" -ForegroundColor Yellow
    foreach ($log in $setting.Logs) {
        $status = if ($log.Enabled) { "✓" } else { "✗" }
        $color = if ($log.Enabled) { "Green" } else { "Red" }
        Write-Host "  $status $($log.Category)" -ForegroundColor $color
    }
    
    if ($setting.WorkspaceId) {
        Write-Host "`n✓ Sending to Log Analytics" -ForegroundColor Green
    }
}
```

**For Azure AD:**
```powershell
# Check Azure AD diagnostic settings
Connect-MgGraph -Scopes "AuditLog.Read.All"
$uri = "https://graph.microsoft.com/beta/auditLogs/directoryAudits/diagnosticSettings"
$settings = Invoke-MgGraphRequest -Method GET -Uri $uri

# Show configured categories
$settings.value | ForEach-Object {
    Write-Host "`n=== $($_.name) ===" -ForegroundColor Cyan
    $_.logs | ForEach-Object {
        $status = if ($_.enabled) { "✓" } else { "✗" }
        Write-Host "  $status $($_.category)" -ForegroundColor $(if ($_.enabled) { "Green" } else { "Red" })
    }
}
```

**Save this output** - It's proof of configuration for auditors.

**What you should see:**
- ALL categories show ✓ (green checkmark)
- Workspace ID displayed
- If any show ✗ (red X), go back and fix the configuration

**Export for compliance documentation:**
```powershell
# Create timestamped proof
$timestamp = Get-Date -Format "yyyy-MM-dd-HHmm"
$diagnosticSettings | ConvertTo-Json -Depth 10 | 
    Out-File "diagnostic-settings-proof-$timestamp.json"

Write-Host "`nConfiguration proof saved: diagnostic-settings-proof-$timestamp.json" -ForegroundColor Green
```

**This file proves:**
1. What you configured
2. When you verified it  
3. Which categories are enabled
4. Where logs are going

**Save these monthly** - Creates audit trail showing continuous compliance.

---

## Step 3: Verify Logs Are Flowing

Wait 10-15 minutes after configuration, then verify.

### Portal Verification

**1. Navigate to Log Analytics Workspace**

- Azure Portal → Search for your workspace name
- Click on `audit-logs-workspace`

**2. Open Logs blade**

- Left menu → **Logs**
- Close the "Queries" popup (X in top right)

**3. Run verification queries:**

#### Query 1: Check for AuditLogs

```kusto
AuditLogs
| where TimeGenerated > ago(1h)
| take 10
| project TimeGenerated, OperationName, Identity, Result
```

**Expected result:** 10 rows of audit events (user actions, admin changes, etc.)

**If you see "Table not found" or zero rows:**
- Wait another 10 minutes
- Check diagnostic settings are saved (Portal → Azure AD → Diagnostic settings)
- Verify you have Azure AD Premium P1/P2

#### Query 2: Check for SignInLogs

```kusto
SignInLogs
| where TimeGenerated > ago(1h)
| take 10
| project TimeGenerated, UserPrincipalName, AppDisplayName, IPAddress, ResultType
```

**Expected result:** User sign-in events from the last hour

**If zero rows:**
- Wait longer (sign-ins might be sparse in dev environments)
- Try `ago(24h)` instead of `ago(1h)`

#### Query 3: Check for Service Principal Activity

```kusto
AADServicePrincipalSignInLogs
| where TimeGenerated > ago(1h)
| take 10
| project TimeGenerated, AppId, ServicePrincipalName, ResourceDisplayName
```

**Expected result:** App registration sign-in events

**If zero rows:**
- This is normal if no apps are currently authenticating
- Try `ago(7d)` for a wider window
- Not all environments have high app activity

#### Query 4: Verify All Log Types Exist

```kusto
// Check which log types are present
search *
| where TimeGenerated > ago(24h)
| where $table startswith "AAD" or $table == "AuditLogs" or $table contains "SignIn"
| summarize 
    RowCount = count(),
    FirstSeen = min(TimeGenerated),
    LastSeen = max(TimeGenerated)
    by $table
| order by RowCount desc
```

**Expected output:**

| Table Name | RowCount | FirstSeen | LastSeen |
|------------|----------|-----------|----------|
| SignInLogs | 4,523 | 2025-10-27 08:00:00 | 2025-10-27 09:30:00 |
| AuditLogs | 342 | 2025-10-27 08:15:00 | 2025-10-27 09:25:00 |
| AADServicePrincipalSignInLogs | 156 | 2025-10-27 08:30:00 | 2025-10-27 09:20:00 |
| AADNonInteractiveUserSignInLogs | 89 | 2025-10-27 08:45:00 | 2025-10-27 09:15:00 |
| AADManagedIdentitySignInLogs | 12 | 2025-10-27 09:00:00 | 2025-10-27 09:10:00 |

**If you see fewer than 5 tables:**
- Check which log categories you enabled in diagnostic settings
- Wait longer (some logs are infrequent)
- Verify you selected all five checkboxes in Step 2

### PowerShell Verification

```powershell
# Install Az.OperationalInsights if needed
Install-Module Az.OperationalInsights -Scope CurrentUser -Force

# Connect
Connect-AzAccount

# Run query to check for logs
$resourceGroup = "governance-rg"
$workspaceName = "audit-logs-workspace"

$query = @"
search *
| where TimeGenerated > ago(24h)
| where `$table startswith "AAD" or `$table == "AuditLogs" or `$table contains "SignIn"
| summarize RowCount = count() by `$table
"@

$result = Invoke-AzOperationalInsightsQuery `
    -WorkspaceId (Get-AzOperationalInsightsWorkspace `
        -ResourceGroupName $resourceGroup `
        -Name $workspaceName).CustomerId `
    -Query $query

$result.Results | Format-Table

# Should show multiple log types with row counts
```

## Step 4: Build Your Azure AD Query Library

These are the queries auditors WILL ask for. Build them now.

### Query 1: Who Created This App Registration?

```kusto
// Find app registration creation events
AuditLogs
| where OperationName == "Add application"
| where Result == "success"
| extend 
    AppName = tostring(TargetResources[0].displayName),
    AppId = tostring(TargetResources[0].id),
    CreatedBy = tostring(InitiatedBy.user.userPrincipalName),
    CreatedByObjectId = tostring(InitiatedBy.user.id)
| project 
    TimeGenerated,
    CreatedBy,
    AppName,
    AppId,
    CorrelationId
| order by TimeGenerated desc
```

**Use case:** Security flags an app registration. You need to know who created it.

**Save this query as:** `App Registration Creation History`

### Query 2: Who Granted Admin Consent?

```kusto
// Track admin consent grants to apps
AuditLogs
| where OperationName == "Consent to application"
| where Result == "success"
| extend 
    AppName = tostring(TargetResources[0].displayName),
    ConsentedBy = tostring(InitiatedBy.user.userPrincipalName),
    ConsentType = tostring(TargetResources[0].modifiedProperties[0].newValue),
    Permissions = tostring(TargetResources[0].modifiedProperties)
| project 
    TimeGenerated,
    ConsentedBy,
    AppName,
    ConsentType,
    Permissions,
    CorrelationId
| order by TimeGenerated desc
```

**Use case:** "Who approved Graph API permissions for this app?"

**Save as:** `Admin Consent Grants`

### Query 3: Is This App Registration Being Used?

```kusto
// Check service principal sign-in activity
let appId = "YOUR-APP-ID-GUID";  // Replace with actual App ID
AADServicePrincipalSignInLogs
| where AppId == appId
| where TimeGenerated >= ago(90d)
| summarize 
    SignInCount = count(),
    FirstSignIn = min(TimeGenerated),
    LastSignIn = max(TimeGenerated),
    UniqueResources = dcount(ResourceDisplayName),
    Resources = make_set(ResourceDisplayName)
    by AppDisplayName, AppId
| extend DaysSinceLastUse = datetime_diff('day', now(), LastSignIn)
| project 
    AppDisplayName,
    AppId,
    SignInCount,
    FirstSignIn,
    LastSignIn,
    DaysSinceLastUse,
    UniqueResources,
    Resources
```

**Use case:** Tenable alert "unused app registration" - verify if it's actually unused.

**Save as:** `App Registration Usage Check`

**Pro tip:** Run this for ALL app registrations monthly. Automate it. Find the truly unused ones.

### Query 4: Failed Sign-In Attempts (Brute Force Detection)

```kusto
// Find repeated failed sign-in attempts
SignInLogs
| where TimeGenerated >= ago(24h)
| where ResultType != 0  // 0 = success, anything else = failure
| summarize 
    FailedAttempts = count(),
    FirstAttempt = min(TimeGenerated),
    LastAttempt = max(TimeGenerated),
    UniqueIPs = dcount(IPAddress),
    IPList = make_set(IPAddress),
    ErrorCodes = make_set(ResultType)
    by UserPrincipalName, AppDisplayName
| where FailedAttempts > 10  // Threshold for investigation
| order by FailedAttempts desc
```

**Use case:** Security incident response - identify brute force attempts.

**Save as:** `Brute Force Detection - Failed Logins`

### Query 5: New Admin Role Assignments

```kusto
// Track who was granted admin roles
AuditLogs
| where OperationName == "Add member to role"
| where Result == "success"
| extend 
    RoleName = tostring(TargetResources[0].displayName),
    UserAdded = tostring(TargetResources[1].userPrincipalName),
    AddedBy = tostring(InitiatedBy.user.userPrincipalName)
| project 
    TimeGenerated,
    AddedBy,
    UserAdded,
    RoleName,
    CorrelationId
| order by TimeGenerated desc
```

**Use case:** Quarterly access review - "who has Global Administrator?"

**Save as:** `Admin Role Grants`

### Query 6: Sign-Ins from Specific Country

```kusto
// Find sign-ins from specific location (adjust for your compliance needs)
SignInLogs
| where TimeGenerated >= ago(90d)
| where LocationDetails.countryOrRegion == "RU"  // Russia, adjust as needed
| where ResultType == 0  // Successful sign-ins only
| project 
    TimeGenerated,
    UserPrincipalName,
    AppDisplayName,
    IPAddress,
    LocationDetails.city,
    LocationDetails.countryOrRegion,
    DeviceDetail.operatingSystem
| order by TimeGenerated desc
```

**Use case:** Compliance review - "show me all successful sign-ins from [restricted country]"

**Save as:** `Sign-Ins from [Country]`

### Query 7: Conditional Access Policy Changes

```kusto
// Track changes to Conditional Access policies
AuditLogs
| where Category == "Policy"
| where OperationName contains "conditional access policy"
| extend 
    PolicyName = tostring(TargetResources[0].displayName),
    Action = OperationName,
    ChangedBy = tostring(InitiatedBy.user.userPrincipalName),
    Changes = tostring(TargetResources[0].modifiedProperties)
| project 
    TimeGenerated,
    ChangedBy,
    PolicyName,
    Action,
    Changes
| order by TimeGenerated desc
```

**Use case:** "Who changed the MFA policy last week?"

**Save as:** `Conditional Access Policy Changes`

### Query 8: Service Principal Secret/Certificate Additions

```kusto
// Track when secrets or certificates are added to app registrations
AuditLogs
| where OperationName in ("Add service principal credentials", "Update application – Certificates and secrets management")
| where Result == "success"
| extend 
    AppName = tostring(TargetResources[0].displayName),
    AddedBy = tostring(InitiatedBy.user.userPrincipalName),
    CredentialType = tostring(TargetResources[0].modifiedProperties[0].displayName)
| project 
    TimeGenerated,
    AddedBy,
    AppName,
    CredentialType,
    CorrelationId
| order by TimeGenerated desc
```

**Use case:** Security review - "who added credentials to this app this month?"

**Save as:** `App Registration Credential Additions`

## Step 5: App Registration External Tracking

App registrations **cannot be tagged** because they're Azure AD objects, not ARM resources.

You need external tracking. Here's how.

### Option 1: Spreadsheet (Quick Start)

Create this in Excel/Google Sheets:

| App Name | App ID | Object ID | Created By | Created Date | Purpose | Owner Email | Status | Last Reviewed | Notes |
|----------|--------|-----------|------------|--------------|---------|-------------|--------|---------------|-------|
| MyApp-Prod | guid | guid | john.doe | 2024-03-15 | Production API | jane.smith@company.com | Active | 2025-10-01 | Accesses Graph API |
| TestApp-042 | guid | guid | old.employee | 2023-08-22 | Testing | unknown@company.com | Review | 2025-10-01 | No usage in 90 days |
| DevTool | guid | guid | current.user | 2025-01-10 | Local dev | current.user@company.com | Active | 2025-10-15 | Personal use |

**Required columns:**
- App Name (from Azure AD)
- App ID (GUID)
- Created By (from audit logs or Azure AD)
- Owner Email (current owner contact)
- Status (Active / Review / Decommission)
- Last Reviewed (date)

**Update cadence:**
- New app created → Add row immediately
- Monthly → Run export script (below) and cross-check
- Quarterly → Full review with security team
- Tenable alert → Check this sheet first

### Option 2: Automated Export Script

Run this monthly to keep your spreadsheet current:

```powershell
# Export all app registrations to CSV
Connect-AzureAD

# Get all applications
$apps = Get-AzureADApplication -All $true

# Build detailed report
$report = @()
foreach ($app in $apps) {
    # Get owners
    $owners = Get-AzureADApplicationOwner -ObjectId $app.ObjectId -All $true
    $ownerEmails = $owners.UserPrincipalName -join "; "
    
    # Get credentials (secrets and certificates)
    $secrets = $app.PasswordCredentials
    $certs = $app.KeyCredentials
    
    # Check for expiring credentials
    $expiringSecrets = $secrets | Where-Object { $_.EndDate -lt (Get-Date).AddDays(60) }
    
    $report += [PSCustomObject]@{
        DisplayName = $app.DisplayName
        AppId = $app.AppId
        ObjectId = $app.ObjectId
        CreatedDateTime = $app.CreatedDateTime
        Owners = $ownerEmails
        OwnerCount = $owners.Count
        SecretCount = $secrets.Count
        CertCount = $certs.Count
        ExpiringSecretsIn60Days = $expiringSecrets.Count
        SignInAudience = $app.SignInAudience
        PublisherDomain = $app.PublisherDomain
        ReplyUrls = ($app.ReplyUrls -join "; ")
    }
}

# Export to CSV with timestamp
$timestamp = Get-Date -Format "yyyy-MM-dd"
$outputFile = "app-registrations-inventory-$timestamp.csv"
$report | Export-Csv -Path $outputFile -NoTypeInformation

Write-Host "Exported $($report.Count) app registrations to: $outputFile" -ForegroundColor Green

# Show apps without owners (RED FLAG)
$noOwners = $report | Where-Object { $_.OwnerCount -eq 0 }
if ($noOwners) {
    Write-Host "`nWARNING: $($noOwners.Count) apps have NO OWNERS:" -ForegroundColor Red
    $noOwners | Select-Object DisplayName, AppId, CreatedDateTime | Format-Table
}

# Show apps with expiring secrets
$expiring = $report | Where-Object { $_.ExpiringSecretsIn60Days -gt 0 }
if ($expiring) {
    Write-Host "`nATTENTION: $($expiring.Count) apps have secrets expiring in 60 days:" -ForegroundColor Yellow
    $expiring | Select-Object DisplayName, AppId, ExpiringSecretsIn60Days | Format-Table
}
```

**Run this:**
- Monthly (1st of the month)
- Before quarterly access reviews
- After Tenable scan reports
- When security asks "what apps do we have?"

**Compare reports:**
```powershell
# Compare this month vs last month to find NEW apps
$thisMonth = Import-Csv "app-registrations-inventory-2025-10-01.csv"
$lastMonth = Import-Csv "app-registrations-inventory-2025-09-01.csv"

$newApps = $thisMonth | Where-Object { $_.AppId -notin $lastMonth.AppId }
Write-Host "New apps created this month: $($newApps.Count)"
$newApps | Select-Object DisplayName, AppId, CreatedDateTime, Owners | Format-Table
```

### Option 3: CMDB Integration (Enterprise)

If you have ServiceNow, Jira, or Azure DevOps:

**Create CI Type: "Azure App Registration"**

Fields:
- Name (String)
- App ID (String/GUID)
- Object ID (String/GUID)
- Owner (Reference to User)
- Created By (String)
- Created Date (Date)
- Purpose (Text)
- Status (Choice: Active/Review/Decommission)
- Last Sign-In (Date) - updated from KQL query
- API Permissions (Text)

**Automated sync:**
```powershell
# Pseudo-code for CMDB sync
$apps = Get-AzureADApplication -All $true
foreach ($app in $apps) {
    # Check if exists in CMDB
    $cmdbRecord = Get-CMDBRecord -Type "AzureAppRegistration" -AppId $app.AppId
    
    if ($cmdbRecord) {
        # Update existing record
        Update-CMDBRecord -Id $cmdbRecord.Id -Data @{
            LastVerified = Get-Date
            OwnerCount = (Get-AzureADApplicationOwner -ObjectId $app.ObjectId).Count
        }
    } else {
        # Create new record
        New-CMDBRecord -Type "AzureAppRegistration" -Data @{
            Name = $app.DisplayName
            AppId = $app.AppId
            ObjectId = $app.ObjectId
            CreatedDate = $app.CreatedDateTime
            Status = "Review"  # New apps default to review status
        }
    }
}
```

Run weekly via Azure Automation Runbook.

## Step 6: Storage Account Archive (7-Year Retention)

Log Analytics retention (730 days max) costs ~$0.12/GB/month. Storage costs ~$0.01/GB/month.

For 7-year compliance: export to storage.

### Create Storage Account (If Needed)

```powershell
# Set variables
$resourceGroup = "governance-rg"
$storageAccountName = "auditarchive$(Get-Random)"  # Must be globally unique
$location = "eastus"

# Create storage account
New-AzStorageAccount `
    -ResourceGroupName $resourceGroup `
    -Name $storageAccountName `
    -Location $location `
    -SkuName Standard_LRS `
    -Kind StorageV2 `
    -AccessTier Cool `
    -MinimumTlsVersion TLS1_2

Write-Host "Storage account created: $storageAccountName" -ForegroundColor Green

# Enable soft delete (protection against accidental deletion)
$storageAccount = Get-AzStorageAccount `
    -ResourceGroupName $resourceGroup `
    -Name $storageAccountName

$ctx = $storageAccount.Context
Enable-AzStorageBlobDeleteRetentionPolicy -Context $ctx -RetentionDays 30

Write-Host "Soft delete enabled (30-day retention)" -ForegroundColor Green
```

### Add Storage to Diagnostic Settings

**Portal method:**
1. Azure Portal → Azure Active Directory → Diagnostic settings
2. Click on your existing diagnostic setting (`export-azuread-to-law`)
3. Add destination:
   - ☑ **Archive to a storage account**
   - Select your storage account
   - Retention (days): **2555** (7 years)
4. Click "Save"

**PowerShell method:**

```powershell
# Get storage account resource ID
$storageId = (Get-AzStorageAccount `
    -ResourceGroupName $resourceGroup `
    -Name $storageAccountName).Id

# Update diagnostic settings to include storage
# Note: This updates the existing diagnostic setting
# Run the same diagnostic setting creation command from Step 2
# but add storage configuration:

$diagnosticSetting = @{
    name = "export-azuread-to-law"
    workspaceId = $workspaceResourceId
    storageAccountId = $storageId
    logRetentionDays = 2555  # 7 years
    logs = @(
        @{ category = "AuditLogs"; enabled = $true; retentionPolicy = @{ enabled = $true; days = 2555 } }
        @{ category = "SignInLogs"; enabled = $true; retentionPolicy = @{ enabled = $true; days = 2555 } }
        @{ category = "NonInteractiveUserSignInLogs"; enabled = $true; retentionPolicy = @{ enabled = $true; days = 2555 } }
        @{ category = "ServicePrincipalSignInLogs"; enabled = $true; retentionPolicy = @{ enabled = $true; days = 2555 } }
        @{ category = "ManagedIdentitySignInLogs"; enabled = $true; retentionPolicy = @{ enabled = $true; days = 2555 } }
    )
}

# Apply via REST API (same as Step 2 but with storage added)
```

### Verify Storage Archive

After 24 hours, check that logs are appearing in storage:

```powershell
# List containers in storage account
$ctx = (Get-AzStorageAccount `
    -ResourceGroupName $resourceGroup `
    -Name $storageAccountName).Context

Get-AzStorageContainer -Context $ctx | Select-Object Name

# Expected containers:
# insights-logs-auditlogs
# insights-logs-signin
# insights-logs-noninteractiveusersignin
# insights-logs-serviceprincipalsignin
# insights-logs-managedidentitysignin
```

**Browse logs:**
```powershell
# List blobs in a specific container
$containerName = "insights-logs-auditlogs"
Get-AzStorageBlob -Container $containerName -Context $ctx | 
    Select-Object Name, LastModified, Length | 
    Sort-Object LastModified -Descending | 
    Select-Object -First 10
```

**Log structure:**
```
/insights-logs-auditlogs/
  resourceId=/TENANTS/YOUR-TENANT-ID/y=2025/m=10/d=27/h=14/m=00/
    PT1H.json
```

**Immutability (optional but recommended):**

```powershell
# Enable legal hold (prevents deletion)
Set-AzRmStorageContainerImmutabilityPolicy `
    -ResourceGroupName $resourceGroup `
    -StorageAccountName $storageAccountName `
    -ContainerName $containerName `
    -ImmutabilityPeriod 2555  # 7 years in days

Write-Host "Immutability policy set - logs cannot be deleted for 7 years" -ForegroundColor Green
```

## Cost Breakdown

Let's talk money. Here's what this actually costs.

### Small Environment (100-500 users)

**Assumptions:**
- 100 users
- 500 sign-ins/day
- 50 audit events/day
- Minimal app registration activity

**Monthly costs:**

| Component | Volume | Cost |
|-----------|--------|------|
| **Log Analytics ingestion** | ~2 GB/month | $5.00 |
| **Log Analytics retention** (730 days) | 2 GB × 24 months | $5.76 |
| **Storage Account** (Cool tier) | 50 GB (7 years accumulated) | $0.50 |
| **Azure AD Premium P1** (per user) | 100 users × $6/user | $600.00 |
| **Total (excluding Azure AD licenses)** | | **$11.26** |
| **Total (including Azure AD licenses)** | | **$611.26** |

**Reality check:** The Azure AD Premium license is the big cost. The logging infrastructure itself is cheap.

### Medium Environment (500-2,000 users)

**Assumptions:**
- 1,000 users
- 5,000 sign-ins/day
- 200 audit events/day
- Moderate app activity

**Monthly costs:**

| Component | Volume | Cost |
|-----------|--------|------|
| **Log Analytics ingestion** | ~15 GB/month | $37.50 |
| **Log Analytics retention** (730 days) | 15 GB × 24 months | $43.20 |
| **Storage Account** | 360 GB (7 years) | $3.60 |
| **Azure AD Premium P1** | 1,000 users × $6/user | $6,000.00 |
| **Total (excluding Azure AD licenses)** | | **$84.30** |
| **Total (including Azure AD licenses)** | | **$6,084.30** |

### Enterprise Environment (5,000+ users)

**Assumptions:**
- 10,000 users
- 50,000 sign-ins/day
- 1,000 audit events/day
- Heavy app/automation activity

**Monthly costs:**

| Component | Volume | Cost |
|-----------|--------|------|
| **Log Analytics ingestion** | ~100 GB/month | $250.00 |
| **Log Analytics retention** (730 days) | 100 GB × 24 months | $288.00 |
| **Storage Account** | 2.4 TB (7 years) | $24.00 |
| **Azure AD Premium P1** | 10,000 users × $6/user | $60,000.00 |
| **Total (excluding Azure AD licenses)** | | **$562.00** |
| **Total (including Azure AD licenses)** | | **$60,562.00** |

### Cost Optimization Tips

**1. Reduce Log Analytics retention:**
```powershell
# Set to 90 days instead of 730 days
Set-AzOperationalInsightsWorkspace `
    -ResourceGroupName $resourceGroup `
    -Name $workspaceName `
    -RetentionInDays 90

# Savings: ~75% on retention costs
# Trade-off: Less query-able history (rely more on storage archive)
```

**2. Filter sign-in logs:**

You can exclude specific sign-in types from export:

- NonInteractiveUserSignInLogs can be disabled if you only care about interactive logins
- ManagedIdentitySignInLogs can be disabled if you don't use managed identities heavily

**Trade-off:** Less complete audit trail. Only do this if you're confident you don't need certain log types.

**3. Use commitment tiers:**

If you're ingesting 100+ GB/month:

```powershell
# Set commitment tier (100 GB/day minimum)
Set-AzOperationalInsightsWorkspace `
    -ResourceGroupName $resourceGroup `
    -Name $workspaceName `
    -Sku CapacityReservation `
    -CapacityReservationLevel 100

# Pricing: $196/day ($5,880/month) for 100 GB/day
# vs. $250/month on Pay-As-You-Go
# Savings kick in above ~78 GB/month
```

**4. Storage lifecycle management:**

```powershell
# Automatically move old blobs to Archive tier after 365 days
$rule = Add-AzStorageAccountManagementPolicyAction `
    -BaseBlobAction TierToArchive `
    -DaysAfterModificationGreaterThan 365

Add-AzStorageAccountManagementPolicyRule `
    -ResourceGroupName $resourceGroup `
    -AccountName $storageAccountName `
    -Rules $rule

# Archive tier: $0.002/GB/month (vs. Cool tier $0.01/GB/month)
# Savings: 80% on old logs you rarely access
```

## Troubleshooting Common Issues

### Issue 1: "Table not found" in Log Analytics

**Symptoms:**
- Query returns "Table 'AuditLogs' not found"
- Or: "Table 'SignInLogs' not found"

**Causes:**
1. Diagnostic settings not configured correctly
2. Not enough time has passed (logs take 10-30 minutes to appear)
3. No activity to log (empty tenant, dev environment)
4. Azure AD Premium not properly licensed

**Fix:**

```powershell
# Check diagnostic settings exist
Connect-MgGraph -Scopes "AuditLog.Read.All"
$uri = "https://graph.microsoft.com/beta/auditLogs/directoryAudits/diagnosticSettings"
Invoke-MgGraphRequest -Method GET -Uri $uri | ConvertTo-Json -Depth 10

# Should show your diagnostic setting with all log categories enabled
```

**If no diagnostic settings found:**
- Go back to Step 2 and reconfigure
- Verify you have Azure AD Premium P1/P2

**If diagnostic settings exist but no logs:**
- Wait 30 minutes
- Generate some activity (sign in, create a test app registration)
- Query again

### Issue 2: SignInLogs Present, But AuditLogs Missing

**Symptoms:**
- `SignInLogs` table exists and has data
- `AuditLogs` table missing or empty

**Cause:** Not all log categories were selected in diagnostic settings

**Fix:**

1. Portal → Azure AD → Diagnostic settings
2. Click on your diagnostic setting
3. Verify ALL FIVE categories are checked:
   - ☑ AuditLogs
   - ☑ SignInLogs  
   - ☑ NonInteractiveUserSignInLogs
   - ☑ ServicePrincipalSignInLogs
   - ☑ ManagedIdentitySignInLogs
4. Click "Save"
5. Wait 15 minutes

### Issue 3: High Costs (Unexpected Log Analytics Bill)

**Symptoms:**
- Log Analytics ingestion costs higher than expected
- SignInLogs consuming most of the data volume

**Causes:**
- High sign-in volume (common with automation/service accounts)
- NonInteractiveUserSignInLogs capturing every token refresh
- No retention policy optimization

**Fix:**

**Check ingestion volume:**
```kusto
// See which log types consume most data
Usage
| where TimeGenerated > ago(30d)
| where IsBillable == true
| summarize DataVolume_GB = sum(Quantity) / 1000 by DataType
| order by DataVolume_GB desc
```

**Expected output:**

| DataType | DataVolume_GB |
|----------|---------------|
| SignInLogs | 45.2 |
| AADNonInteractiveUserSignInLogs | 23.1 |
| AuditLogs | 8.5 |
| AADServicePrincipalSignInLogs | 3.2 |

**If SignInLogs > 80% of total:**
- This is normal for high-user environments
- Consider filtering or sampling (advanced topic, ask security first)

**If you're over budget:**
1. Reduce retention from 730 days to 90 days
2. Rely on storage account for long-term archive
3. Disable NonInteractiveUserSignInLogs (if security approves)

### Issue 4: Can't Find Specific App Registration in Logs

**Symptoms:**
- Query for app registration creation returns no results
- You know the app exists, but can't find the audit trail

**Causes:**
1. App created before diagnostic settings were configured
2. Audit log retention expired (30 days default)
3. Search query incorrect (app name vs. app ID)

**Fix:**

```kusto
// Search by app name (partial match)
AuditLogs
| where OperationName == "Add application"
| extend AppName = tostring(TargetResources[0].displayName)
| where AppName contains "MyApp"  // Replace with partial name
| project TimeGenerated, AppName, InitiatedBy
```

**If still no results:**
- The app was created before logs were exported
- Check Azure AD → App registrations → [Your App] → Properties → Created date
- If created date is older than your log retention, you won't find the audit event

**Workaround:**
- Document app registration details NOW (use the export script from Step 5)
- Going forward, you'll have the audit trail

### Issue 5: Storage Account Access Denied

**Symptoms:**
- Can't browse blobs in storage account
- "AuthorizationPermissionMismatch" error

**Cause:** Missing RBAC role on storage account

**Fix:**

```powershell
# Grant yourself Storage Blob Data Reader role
$storageAccount = Get-AzStorageAccount `
    -ResourceGroupName $resourceGroup `
    -Name $storageAccountName

$userId = (Get-AzADUser -SignedIn).Id

New-AzRoleAssignment `
    -ObjectId $userId `
    -RoleDefinitionName "Storage Blob Data Reader" `
    -Scope $storageAccount.Id

Write-Host "Role assigned - wait 5 minutes for permission propagation" -ForegroundColor Green
```

## Quarterly Testing Checklist

Test your setup every quarter. This catches issues before audits.

### Q4 2025 Azure AD Audit Drill

**Test Date:** October 27, 2025  
**Tester:** [Your Name]

#### Test 1: Log Retention Verification

```kusto
// Verify logs exist from 90+ days ago
AuditLogs
| summarize 
    OldestLog = min(TimeGenerated),
    NewestLog = max(TimeGenerated),
    DaysCovered = datetime_diff('day', max(TimeGenerated), min(TimeGenerated))
```

- [ ] AuditLogs retention: _____ days (expected: 90+)
- [ ] SignInLogs retention: _____ days (expected: 90+)
- [ ] Storage account has logs older than 90 days: ☐ Yes ☐ No

**Pass/Fail:** _____

#### Test 2: Query Execution

- [ ] Run Query 1 (Who created app registration): Works? ☐ Yes ☐ No
- [ ] Run Query 2 (Admin consent grants): Works? ☐ Yes ☐ No
- [ ] Run Query 3 (App usage check): Pick random app, verify results
- [ ] Run Query 5 (Admin role assignments): Shows recent changes

**Pass/Fail:** _____

#### Test 3: App Registration Inventory

- [ ] Open tracking spreadsheet/CMDB
- [ ] Last updated date: ___________
- [ ] Spot check 5 random apps: Owners match Azure AD? ☐ Yes ☐ No
- [ ] New apps created this quarter: _____ (compare to last export)

**Pass/Fail:** _____

#### Test 4: Storage Archive Verification

```powershell
# Check storage containers exist and have recent data
$containers = Get-AzStorageContainer -Context $ctx
$containers | ForEach-Object {
    $latest = Get-AzStorageBlob -Container $_.Name -Context $ctx | 
        Sort-Object LastModified -Descending | 
        Select-Object -First 1
    [PSCustomObject]@{
        Container = $_.Name
        LatestBlob = $latest.Name
        LastModified = $latest.LastModified
    }
}
```

- [ ] All 5 log containers present: ☐ Yes ☐ No
- [ ] Latest blob timestamp is within 24 hours: ☐ Yes ☐ No
- [ ] Total storage size: _____ GB (expected: increasing monthly)

**Pass/Fail:** _____

#### Test 5: Access & Documentation

- [ ] Compliance team has Log Analytics access: ☐ Yes ☐ No
- [ ] Storage account access restricted (RBAC verified): ☐ Yes ☐ No
- [ ] Query library documentation up to date: ☐ Yes ☐ No
- [ ] App registration inventory accessible: ☐ Yes ☐ No

**Pass/Fail:** _____

### Issues Found

[List any issues discovered during drill]

### Action Items

- [ ] Fix issue #1: _______________
- [ ] Update documentation: _______________
- [ ] Retest failed items in 30 days

**Next Drill:** January 27, 2026

## Real-World Audit Scenarios

Here's what this looks like when auditors actually ask questions:

### Scenario 1: SOX Quarterly Access Review

**Auditor request:**  
*"Provide a list of all users granted Global Administrator role in Q3 2025, including who granted the role and when."*

**Your response time:** 5 minutes

**Query:**
```kusto
AuditLogs
| where TimeGenerated between(datetime(2025-07-01) .. datetime(2025-09-30))
| where OperationName == "Add member to role"
| where Result == "success"
| extend 
    RoleName = tostring(TargetResources[0].displayName),
    UserAdded = tostring(TargetResources[1].userPrincipalName),
    AddedBy = tostring(InitiatedBy.user.userPrincipalName)
| where RoleName contains "Global Administrator"
| project 
    Date = format_datetime(TimeGenerated, 'yyyy-MM-dd'),
    AddedBy,
    UserAdded,
    RoleName
| order by TimeGenerated asc
```

**Export to Excel:**
```powershell
$results | Export-Csv -Path "Q3-2025-Global-Admin-Grants.csv" -NoTypeInformation
```

**Auditor reaction:** ✅ Satisfied. Documentation clear. Closed finding.

### Scenario 2: Security Incident - Compromised Account

**Security team request:**  
*"User john.doe@company.com's credentials were compromised. Show all sign-in activity for the last 90 days, including IP addresses and locations."*

**Your response time:** 10 minutes

**Query:**
```kusto
SignInLogs
| where UserPrincipalName == "john.doe@company.com"
| where TimeGenerated >= ago(90d)
| project 
    TimeGenerated,
    ResultType,
    ResultDescription,
    IPAddress,
    City = LocationDetails.city,
    State = LocationDetails.state,
    Country = LocationDetails.countryOrRegion,
    AppDisplayName,
    DeviceOS = DeviceDetail.operatingSystem,
    Browser = DeviceDetail.browser
| order by TimeGenerated desc
```

**Export and analysis:**
```powershell
# Export to CSV
$signIns | Export-Csv -Path "incident-john-doe-signins.csv" -NoTypeInformation

# Identify suspicious patterns
$signIns | Group-Object IPAddress | 
    Sort-Object Count -Descending | 
    Select-Object Name, Count, @{N='Countries';E={($_.Group.Country | Select-Object -Unique) -join ', '}}
```

**Security team reaction:** ✅ Full visibility. Identified compromise window. Remediation plan confirmed.

### Scenario 3: Tenable Scanner Alert

**Alert:**  
*"50 app registrations detected with client secrets expiring in 30 days. Identify owner and usage."*

**Your response time:** 30 minutes (bulk analysis)

**Step 1: Get list of expiring apps from Tenable export**

**Step 2: Check each app's usage:**
```kusto
// Run for each app ID from Tenable report
let appIds = dynamic(["app-id-1", "app-id-2", "app-id-3"]);  // Up to 50
AADServicePrincipalSignInLogs
| where AppId in (appIds)
| where TimeGenerated >= ago(90d)
| summarize 
    SignInCount = count(),
    LastUsed = max(TimeGenerated),
    Resources = make_set(ResourceDisplayName)
    by AppId, AppDisplayName
| extend DaysSinceLastUse = datetime_diff('day', now(), LastUsed)
| order by SignInCount desc
```

**Step 3: Cross-reference with tracking spreadsheet:**
```powershell
# Load spreadsheet
$inventory = Import-Csv "app-registrations-inventory-2025-10-01.csv"

# Match Tenable alerts to inventory
$tenableApps = Import-Csv "tenable-expiring-secrets-2025-10-27.csv"
$analysis = $tenableApps | ForEach-Object {
    $appId = $_.AppId
    $inventoryRecord = $inventory | Where-Object { $_.AppId -eq $appId }
    [PSCustomObject]@{
        AppName = $_.AppName
        AppId = $appId
        ExpirationDate = $_.SecretExpiration
        LastUsed = $kqlResults[$appId].LastUsed
        Owner = $inventoryRecord.Owners
        Status = if ($kqlResults[$appId].SignInCount -eq 0) { "UNUSED - SAFE TO DELETE" } else { "IN USE - RENEW SECRET" }
    }
}

$analysis | Export-Csv -Path "tenable-app-analysis-2025-10-27.csv" -NoTypeInformation
```

**Security team reaction:** ✅ Clear action plan. Unused apps identified for deletion. Active apps flagged for renewal.

## Integration with Part 1 (Activity Logs)

You've now configured both systems:

**Part 1 (Activity Logs):**
- ARM resources (VMs, storage, networks, etc.)
- Who created/deleted/modified resources
- Resource-level operations

**Part 2 (Azure AD Logs):**
- Identity layer (users, apps, roles, consent)
- Who authenticated and from where
- App registration lifecycle

**Together, you have:**
- Complete audit trail across Azure
- 7-year retention compliance
- Query-able history for investigations
- External tracking for untaggable resources

**The workflow:**

1. **Daily:** Logs automatically export to Log Analytics + Storage
2. **Weekly:** Run app registration export script
3. **Monthly:** Review new apps, check usage, update inventory
4. **Quarterly:** Run audit drill, verify retention, test queries
5. **Annually:** Present to auditors with confidence

## Next Steps

You're done with the technical setup. Now:

### Immediate Actions (This Week)

1. ✅ Verify logs are flowing (Step 3 queries)
2. ✅ Save query library to workspace
3. ✅ Export app registrations to spreadsheet
4. ✅ Document your architecture (one-page reference)

### Short Term (This Month)

1. Run first monthly export of app registrations
2. Cross-check with Tenable alerts
3. Identify and flag apps without owners
4. Schedule first quarterly audit drill

### Ongoing (Every Quarter)

1. Run audit drill (testing checklist above)
2. Review app registration inventory
3. Update query library based on actual audit requests
4. Verify retention is working (storage + Log Analytics)

## The Takeaway

Azure AD logs are **separate** from Activity Logs. You need both.

**Part 1 (Activity Logs):** Covers ARM resources  
**Part 2 (Azure AD Logs):** Covers identity layer

**The cost:** $50-200/month (excluding Azure AD Premium licenses)

**The ROI:** When security asks "who created this app registration 6 months ago?" - you have the answer in 30 seconds instead of 30 hours.

**The reality:** Most organizations only monitor Activity Logs and completely miss app registrations, consent grants, and sign-in patterns. Don't be most organizations.

---

**Questions?** Email me or drop a comment. I've implemented this at scale (10,000+ users, SOX compliance) and I'm happy to help troubleshoot.

**Found this useful?** Share it with your security team. They'll thank you during the next audit cycle.

**Up next:** Part 3 will cover automated alerting on high-risk Azure AD events (unusual sign-ins, new admin roles, consent grants to suspicious apps). Stay tuned.
