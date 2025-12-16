---
title: "The Logic App That Monitors Every Expiring Certificate in Azure (And Accidentally Saved Our Migration)"
date: 2025-12-16
summary: "Production Logic App that monitors app registration certificates and secrets via Microsoft Graph API. Handles pagination for 100+ apps, extracts owner information, sends HTML email alerts. Built for security compliance, caught Azure Migrate appliances expiring before production migration. Complete walkthrough with working code."
tags:
  - Azure
  - Automation
  - Logic Apps
  - Governance
  - Security
  - Microsoft Graph
  - Entra ID
cover: /static/images/hero/logic-app-certificate-monitor.png
hub: automation
related_posts:
  - azure-migrate-certificate-18-month-limit
  - azure-tag-governance-policy
  - four-logic-apps-every-azure-admin-needs
  - azure-debugging-ai-rule
---

# The Logic App That Monitors Every Expiring Certificate in Azure (And Accidentally Saved Our Migration)

## Short Answer

This Logic App monitors all Entra ID app registration certificates and secrets via Microsoft Graph API, sending email alerts 30 days before expiration. It handles paginated responses for enterprises with 100+ applications, extracts owner information for targeted notifications, and formats results as HTML email reports. The solution was built for security compliance but discovered Azure Migrate appliances with expiring certificates that would have deleted 18 months of migration data. The Logic App uses service principal authentication via Key Vault, runs daily at 6 AM, and costs approximately $1-2/month on consumption pricing.

## Why did we build certificate expiration monitoring?

**Original requirement:** Security compliance mandated tracking of all app registration credentials.

**The problem Microsoft doesn't solve:**
- No native Azure Monitor alerts for app registration expiration
- Portal shows expiration dates but doesn't proactively notify
- Enterprises have 100+ app registrations
- Credentials expire with zero warning
- Production services break when certificates expire
- Nobody tracks which app registration belongs to which service

**What we needed:**
- Automated daily scanning
- 30-day early warning
- Owner identification
- Email notifications to responsible teams
- HTML-formatted reports

**What we got:**
- All of the above
- Plus an accidental operational safety net

---

## What the Logic App actually discovered

**Month 3 of operation:** Standard report with 15 expiring credentials.

**Buried in the list:**
```
- Application: AzureMigrate-DC1-Appliance
  Type: Certificate
  Expires: 2026-01-15
  Owner: No Owner
```

**Our reaction:** "What's an Azure Migrate appliance doing in our app registrations?"

**Microsoft's answer:** [Azure Migrate certificates expire after 18 months and delete all your discovery data.](/blog/azure-migrate-certificate-18-month-limit/)

**Without this Logic App:**
- Certificates would have expired silently
- Discovery would have stopped mid-migration
- 18 months of dependency mapping: deleted
- Migration timeline: destroyed
- We'd discover it when authentication failed

**This compliance tool became our migration safety net.**

---

## How the Logic App works (architecture overview)

**Cause:** Microsoft provides no native alerting for app registration certificate expiration in enterprises with 100+ applications.

**Effect:** Certificates expire without warning, breaking production authentication flows and requiring emergency remediation during business hours.

**What to do:** Deploy automated certificate monitoring via Logic App with Microsoft Graph API integration, paginated response handling, and owner-targeted email notifications.

---

**High-level flow:**

1. **Authenticate** - Service principal via Key Vault credentials
2. **Query Graph API** - Get all app registrations with pagination
3. **Check expiration dates** - Both secrets and certificates
4. **Filter results** - 30-day window (configurable)
5. **Extract owners** - From expanded Graph response
6. **Build HTML report** - Formatted table with statistics
7. **Send email** - To team + individual owners
8. **Schedule** - Daily at 6 AM

**What makes this production-grade:**
- Handles pagination (enterprises have 200+ apps)
- Secure credential storage (Key Vault, not hardcoded)
- Owner expansion (targets notifications to responsible teams)
- HTML formatting (readable reports, not raw JSON)
- Error handling (continues if individual apps fail)
- Statistics tracking (processed count, expiring count)

---

## Step 1: Create the service principal with Graph API permissions

**Why service principal authentication:**
- Logic Apps run unattended
- Need consistent credentials
- Requires application-level permissions (not user delegation)

**Required Microsoft Graph API permissions:**

| Permission | Type | Purpose |
|-----------|------|---------|
| `Application.Read.All` | Application | Read all app registrations |
| `User.Read.All` | Application | Read user details for owner expansion |

**PowerShell to create the service principal:**

```powershell
# Create app registration
$app = New-AzADApplication -DisplayName "CertificateMonitor-LogicApp"

# Create service principal
$sp = New-AzADServicePrincipal -ApplicationId $app.AppId

# Create client secret (save this - you can't retrieve it later)
$secret = New-AzADAppCredential -ObjectId $app.Id -EndDate (Get-Date).AddYears(2)

Write-Host "Application ID: $($app.AppId)"
Write-Host "Tenant ID: $((Get-AzContext).Tenant.Id)"
Write-Host "Client Secret: $($secret.SecretText)"
```

**Grant admin consent via Azure Portal:**

1. Go to **Entra ID** → **App registrations**
2. Find your `CertificateMonitor-LogicApp`
3. Go to **API permissions**
4. Add **Microsoft Graph** → **Application permissions**:
   - `Application.Read.All`
   - `User.Read.All`
5. Click **Grant admin consent for [your tenant]**

**Critical:** These must be **Application** permissions, not **Delegated** permissions. Logic Apps can't use delegated permissions.

---

## Step 2: Store credentials in Azure Key Vault

**Why Key Vault:**
- Credentials never appear in Logic App definition
- Secrets not logged in execution history
- Centralized credential rotation
- Audit trail for access

**Store three secrets:**

```powershell
# Get your tenant ID
$tenantId = (Get-AzContext).Tenant.Id

# Store the three required values
Set-AzKeyVaultSecret -VaultName "your-keyvault-name" `
    -Name "tenant-id" `
    -SecretValue (ConvertTo-SecureString $tenantId -AsPlainText -Force)

Set-AzKeyVaultSecret -VaultName "your-keyvault-name" `
    -Name "client-id" `
    -SecretValue (ConvertTo-SecureString $app.AppId -AsPlainText -Force)

Set-AzKeyVaultSecret -VaultName "your-keyvault-name" `
    -Name "client-secret" `
    -SecretValue (ConvertTo-SecureString $secret.SecretText -AsPlainText -Force)
```

**Grant Logic App access to Key Vault:**

After creating the Logic App (next step), assign it the **Key Vault Secrets User** role on your Key Vault.

---

## Step 3: The authentication flow (getting the Graph API token)

**Here's what the Logic App does at runtime:**

### **Action 1-3: Retrieve credentials from Key Vault**

```json
{
    "Tenant_ID": {
        "type": "ServiceProvider",
        "inputs": {
            "parameters": {
                "secretName": "tenant-id"
            },
            "serviceProviderConfiguration": {
                "connectionName": "keyVault",
                "operationId": "getSecret"
            }
        }
    }
}
```

**This runs three times:**
- Get tenant ID
- Get client ID  
- Get client secret

**Result:** Three secure variables with credentials.

---

### **Action 4: Request OAuth token from Microsoft identity platform**

```json
{
    "Get_Token": {
        "type": "Http",
        "inputs": {
            "uri": "https://login.microsoftonline.com/@{body('Tenant_ID')?['value']}/oauth2/v2.0/token",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "body": "client_id=@{body('Client_ID')?['value']}&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&client_secret=@{body('Client_Secret')?['value']}&grant_type=client_credentials"
        }
    }
}
```

**What this does:**
- Authenticates to Microsoft identity platform
- Requests token for Graph API scope
- Uses client credentials grant type
- Returns bearer token valid for 1 hour

**Response:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJub...",
    "token_type": "Bearer",
    "expires_in": 3599
}
```

---

### **Action 5: Parse the token response**

```json
{
    "Parse_Token": {
        "type": "ParseJson",
        "inputs": {
            "content": "@body('Get_Token')",
            "schema": {
                "type": "object",
                "properties": {
                    "access_token": {
                        "type": "string"
                    }
                }
            }
        }
    }
}
```

**Result:** `body('Parse_Token')?['access_token']` now contains the bearer token for all subsequent Graph API calls.

---

## Step 4: Paginated Graph API queries (handling 100+ apps)

**The problem:** Microsoft Graph returns maximum 100 items per page.

**The Graph API query:**

```
GET https://graph.microsoft.com/v1.0/applications
  ?$select=displayName,appId,passwordCredentials,keyCredentials
  &$expand=owners($select=displayName,userPrincipalName,mail)
  &$top=100
```

**What we're requesting:**
- `displayName` - App name
- `appId` - Application ID (GUID)
- `passwordCredentials` - Client secrets with expiration dates
- `keyCredentials` - Certificates with expiration dates
- `owners` - Expanded user details (name, email)

**The pagination challenge:**

If you have 250 apps:
- First call returns 100 apps + `@odata.nextLink`
- Second call returns 100 apps + `@odata.nextLink`
- Third call returns 50 apps (no `@odata.nextLink`)

**Logic App solution: Until loop with dynamic nextLink**

### **Initialize variables:**

```json
{
    "Init_All_Apps": {
        "type": "InitializeVariable",
        "inputs": {
            "variables": [{
                "name": "allApps",
                "type": "Array",
                "value": []
            }]
        }
    },
    "Init_Next_Link": {
        "type": "InitializeVariable",
        "inputs": {
            "variables": [{
                "name": "nextLink",
                "type": "String",
                "value": "https://graph.microsoft.com/v1.0/applications?$select=displayName,appId,passwordCredentials,keyCredentials&$expand=owners($select=displayName,userPrincipalName,mail)&$top=100"
            }]
        }
    }
}
```

---

### **Until loop: Keep calling until no nextLink**

```json
{
    "Get_All_Apps_Loop": {
        "type": "Until",
        "expression": "@equals(variables('nextLink'), '')",
        "limit": {
            "count": 60,
            "timeout": "PT1H"
        },
        "actions": {
            "Get_Apps_Page": {
                "type": "Http",
                "inputs": {
                    "uri": "@variables('nextLink')",
                    "method": "GET",
                    "headers": {
                        "Authorization": "@concat('Bearer ', body('Parse_Token')?['access_token'])"
                    }
                }
            },
            "Parse_Apps_Page": {
                "type": "ParseJson",
                "inputs": {
                    "content": "@body('Get_Apps_Page')"
                }
            },
            "Merge_Arrays": {
                "type": "SetVariable",
                "inputs": {
                    "name": "allApps",
                    "value": "@union(variables('allApps'), body('Parse_Apps_Page')?['value'])"
                }
            },
            "Update_Next_Link": {
                "type": "SetVariable",
                "inputs": {
                    "name": "nextLink",
                    "value": "@{if(contains(string(body('Get_Apps_Page')), '@odata.nextLink'), body('Get_Apps_Page')['@odata.nextLink'], '')}"
                }
            }
        }
    }
}
```

**How the pagination works:**

1. **First iteration:**
   - Call Graph API with initial URL
   - Parse response
   - Merge 100 apps into `allApps` array
   - Check if response contains `@odata.nextLink`
   - If yes: Set `nextLink` to that URL
   - If no: Set `nextLink` to empty string

2. **Second iteration:**
   - Call Graph API with `@odata.nextLink` URL
   - Parse response
   - Merge next 100 apps into `allApps` array
   - Check for `@odata.nextLink` again

3. **Final iteration:**
   - Call Graph API with last `@odata.nextLink`
   - Parse response with remaining apps
   - No `@odata.nextLink` in response
   - Set `nextLink` to empty string
   - Until loop condition met: exit

**Result:** `allApps` variable contains all 250 apps in a single array.

---

## Step 5: Checking expiration dates (secrets and certificates)

**Now we have all apps. Time to check which credentials are expiring.**

### **Process each app:**

```json
{
    "Process_Each_App": {
        "type": "Foreach",
        "foreach": "@variables('allApps')",
        "actions": {
            "Check_Has_Credentials": {
                "type": "If",
                "expression": {
                    "or": [
                        {
                            "greater": [
                                "@length(item()?['passwordCredentials'])",
                                0
                            ]
                        },
                        {
                            "greater": [
                                "@length(item()?['keyCredentials'])",
                                0
                            ]
                        }
                    ]
                }
            }
        }
    }
}
```

**Logic:**
- Loop through every app
- Check if it has `passwordCredentials` (secrets) or `keyCredentials` (certificates)
- If neither: skip it
- If either: check expiration dates

---

### **Check password (secret) expiration:**

```json
{
    "Check_Password_Expiry": {
        "type": "Foreach",
        "foreach": "@item()?['passwordCredentials']",
        "actions": {
            "Check_If_Expiring_Soon": {
                "type": "If",
                "expression": {
                    "and": [
                        {
                            "less": [
                                "@ticks(item()['endDateTime'])",
                                "@ticks(addDays(utcNow(), 30))"
                            ]
                        },
                        {
                            "greater": [
                                "@ticks(item()['endDateTime'])",
                                "@ticks(utcNow())"
                            ]
                        }
                    ]
                }
            }
        }
    }
}
```

**What this checks:**
- Loop through all secrets for this app
- For each secret:
  - Is `endDateTime` **less than** 30 days from now? (expiring soon)
  - Is `endDateTime` **greater than** now? (not already expired)
- If both true: Add to report

**Why the two conditions:**
- First condition: Catches credentials expiring within 30 days
- Second condition: Excludes already-expired credentials (we want warnings, not archaeology)

**The 30-day window is configurable:**
- Change `addDays(utcNow(), 30)` to `addDays(utcNow(), 60)` for 60-day warning
- Change to `addDays(utcNow(), 7)` for 7-day warning

---

### **Check certificate expiration (same logic):**

```json
{
    "Check_Certificate_Expiry": {
        "type": "Foreach",
        "foreach": "@item()?['keyCredentials']",
        "actions": {
            "Check_Cert_Expiring_Soon": {
                "type": "If",
                "expression": {
                    "and": [
                        {
                            "less": [
                                "@ticks(item()['endDateTime'])",
                                "@ticks(addDays(utcNow(), 30))"
                            ]
                        },
                        {
                            "greater": [
                                "@ticks(item()['endDateTime'])",
                                "@ticks(utcNow())"
                            ]
                        }
                    ]
                }
            }
        }
    }
}
```

**Same logic, different credential type.**

Certificates use `keyCredentials` instead of `passwordCredentials`, but the expiration check is identical.

---

## Step 6: Building the HTML email report

**When a credential is expiring, add it to the HTML table:**

```json
{
    "Add_To_Table": {
        "type": "AppendToStringVariable",
        "inputs": {
            "name": "htmlTable",
            "value": "@concat('<tr><td>', items('Process_Each_App')?['displayName'], '</td><td>', items('Process_Each_App')?['appId'], '</td><td>Secret</td><td>', formatDateTime(item()['endDateTime'], 'yyyy-MM-dd'), '</td><td>', if(greater(length(items('Process_Each_App')?['owners']), 0), items('Process_Each_App')?['owners'][0]?['displayName'], 'No Owner'), '</td><td>', if(greater(length(items('Process_Each_App')?['owners']), 0), coalesce(items('Process_Each_App')?['owners'][0]?['mail'], items('Process_Each_App')?['owners'][0]?['userPrincipalName']), ''), '</td></tr>')"
        }
    }
}
```

**What this builds:**

| App Name | App ID | Type | Expiration Date | Owner Name | Owner Email |
|----------|--------|------|----------------|------------|-------------|
| Production-API | abc123... | Secret | 2026-01-15 | John Smith | john@company.com |
| Azure-Migrate-DC1 | def456... | Certificate | 2026-01-15 | No Owner | |

**The owner logic:**

```javascript
if(greater(length(items('Process_Each_App')?['owners']), 0), 
    items('Process_Each_App')?['owners'][0]?['displayName'], 
    'No Owner')
```

**Translation:**
- If the app has owners (array length > 0)
- Get the first owner's display name
- Otherwise: "No Owner"

**Why this matters:**
- Some apps have no assigned owners
- Logic App handles this gracefully
- Email still sends, shows "No Owner" in table
- Prevents email failures due to null references

---

### **Collect unique owner emails:**

```json
{
    "Add_Owner_To_Array": {
        "type": "AppendToArrayVariable",
        "inputs": {
            "name": "ownersArray",
            "value": {
                "ownerName": "@{if(greater(length(items('Process_Each_App')?['owners']), 0), items('Process_Each_App')?['owners'][0]?['displayName'], 'No Owner')}",
                "ownerEmail": "@{if(greater(length(items('Process_Each_App')?['owners']), 0), coalesce(items('Process_Each_App')?['owners'][0]?['mail'], items('Process_Each_App')?['owners'][0]?['userPrincipalName']), '')}"
            }
        }
    }
}
```

**Purpose:**
- Build array of all owners with expiring credentials
- De-duplicate using `union()` later
- Include owners in email recipients
- Target notifications to responsible parties

---

## Step 7: Send the email with statistics

**Final email action:**

```json
{
    "Send_Email": {
        "type": "ApiConnection",
        "inputs": {
            "host": {
                "connection": {
                    "referenceName": "office365"
                }
            },
            "method": "post",
            "body": {
                "To": "@{if(equals(variables('ownersEmailString'), ''), 'your-team@company.com', concat('your-team@company.com;', variables('ownersEmailString')))}",
                "From": "your-team@company.com",
                "Subject": "App Registration Expiration Report",
                "Body": "@concat('<html><head><style>table{border-collapse:collapse;width:100%;margin-bottom:20px;}th,td{border:1px solid #ccc;padding:8px;text-align:left;}th{background-color:#f0f0f0;font-weight:bold;}h2{color:#d9534f;}.stats{background-color:#f9f9f9;padding:15px;margin:15px 0;border-radius:5px;}</style></head><body><h2>App Registrations Expiring Within 30 Days</h2><div class=\"stats\"><p><strong>Total Apps Processed:</strong> ', variables('processedCount'), '</p><p><strong>Total Apps with Secrets/Certificates:</strong> ', variables('totalApps'), '</p><p><strong>Secrets/Certificates Expiring in Next 30 Days:</strong> ', variables('expiringCount'), '</p></div><table><tr><th>App Name</th><th>App ID</th><th>Type</th><th>Expiration Date</th><th>Owner Name</th><th>Owner Email</th></tr>', if(equals(variables('htmlTable'), ''), '<tr><td colspan=\"6\">No apps expiring in the next 30 days</td></tr>', variables('htmlTable')), '</table></body></html>')",
                "Importance": "High",
                "IsHtml": true
            },
            "path": "/v2/Mail"
        }
    }
}
```

**The email includes:**

**Statistics block:**
```
Total Apps Processed: 247
Total Apps with Secrets/Certificates: 189
Secrets/Certificates Expiring in Next 30 Days: 15
```

**HTML table with:**
- App name
- App ID (GUID)
- Credential type (Secret or Certificate)
- Expiration date (YYYY-MM-DD format)
- Owner name
- Owner email

**Recipients:**
- Your team email (always)
- Plus all owners with expiring credentials (dynamically added)

**Importance:** High (shows as urgent in Outlook)

---

## What this caught in production

**Month 1-2:** Routine compliance reporting
- 3-5 expiring secrets per week
- Teams renewing proactively
- No production incidents

**Month 3:** Azure Migrate discovery

**The alert that changed everything:**

```
Subject: App Registration Expiration Report

Applications with certificates expiring within 30 days:
- AzureMigrate-DC1-Appliance (Certificate expires 2026-01-15)
- AzureMigrate-DC2-Appliance (Certificate expires 2026-01-15)
- AzureMigrate-DR-Appliance (Certificate expires 2026-01-18)
```

**Our reaction:** "What are Azure Migrate appliances?"

**Support ticket revealed:** [Certificates expire after 18 months and delete all migration data.](/blog/azure-migrate-certificate-18-month-limit/)

**Without this Logic App:**
- Appliances would have expired silently (no Azure alerts)
- Discovery would have stopped (no warning)
- 18 months of dependency mapping would be deleted (irreversible)
- Migration timeline would be destroyed (unrecoverable)

**This security compliance tool became our migration safety net.**

---

## Cost breakdown (real production numbers)

**Logic App execution:**
- Consumption plan pricing: ~$0.000125 per action
- Daily run with 250 apps: ~300 actions
- Monthly executions: 30 days × 300 actions = 9,000 actions
- Cost: 9,000 × $0.000125 = **$1.13/month**

**Key Vault operations:**
- 3 secrets retrieved per run
- 30 days × 3 secrets = 90 operations/month
- First 10,000 operations free
- Cost: **$0.00/month**

**Office 365 connector:**
- 1 email per day
- Included in Logic App cost
- Cost: **$0.00/month** (no additional charge)

**Total monthly cost: ~$1.13**

**What you're preventing:**
- Production authentication failures: Priceless
- Emergency weekend remediation: $5,000+ in labor
- Azure Migrate data loss: 18 months of work
- Migration delays: Millions in project impact

**ROI:** 4,400% in the first incident alone.

---

## Deployment instructions (step-by-step)

### **1. Create the service principal (covered in Step 1)**

PowerShell from earlier:
```powershell
$app = New-AzADApplication -DisplayName "CertificateMonitor-LogicApp"
$sp = New-AzADServicePrincipal -ApplicationId $app.AppId
$secret = New-AzADAppCredential -ObjectId $app.Id -EndDate (Get-Date).AddYears(2)
```

Grant admin consent for:
- `Application.Read.All`
- `User.Read.All`

---

### **2. Store credentials in Key Vault (covered in Step 2)**

```powershell
Set-AzKeyVaultSecret -VaultName "your-keyvault" -Name "tenant-id" -SecretValue (ConvertTo-SecureString $tenantId -AsPlainText -Force)
Set-AzKeyVaultSecret -VaultName "your-keyvault" -Name "client-id" -SecretValue (ConvertTo-SecureString $app.AppId -AsPlainText -Force)
Set-AzKeyVaultSecret -VaultName "your-keyvault" -Name "client-secret" -SecretValue (ConvertTo-SecureString $secret.SecretText -AsPlainText -Force)
```

---

### **3. Create Logic App and import definition**

**Option A: Azure Portal**
1. Create Resource → Logic App (Consumption)
2. After creation: Logic app code view
3. Paste JSON definition
4. Save

**Option B: Azure CLI**
```bash
az logic workflow create \
  --resource-group your-rg \
  --name CertificateMonitor \
  --definition @certificate-monitor-logic-app.json
```

**Download the complete Logic App definition:**
- [Logic App JSON](/static/downloads/certificate-monitor-logic-app.json)
- [Deployment README](/static/downloads/certificate-monitor-README.md)

---

### **4. Configure connections**

After importing, the Logic App will show connection errors. For each:

**Key Vault connection:**
1. Open the **Tenant_ID** action
2. Click "Add new connection"
3. Select your Key Vault
4. Choose authentication: Managed Identity or Service Principal
5. Save

**Office 365 connection:**
1. Open the **Send_Email** action
2. Click "Add new connection"
3. Sign in with Office 365 account that has send-as permissions
4. Authorize
5. Save

---

### **5. Update Key Vault secret names**

If your secret names differ from `tenant-id`, `client-id`, `client-secret`:

1. Open **Tenant_ID** action
2. Update `secretName` parameter
3. Repeat for **Client_ID** and **Client_Secret** actions
4. Save

---

### **6. Update email recipients**

```json
"To": "your-team@company.com;additional@company.com"
```

The Logic App automatically adds owners with expiring credentials to the recipient list.

---

### **7. Test the workflow**

1. Click **Run Trigger** → **Recurrence**
2. Wait 2-3 minutes for execution
3. Check **Runs history** for errors
4. Verify email delivery
5. Review HTML formatting

**First run will likely show:**
- Several expiring credentials (30-day window catches existing issues)
- Apps with "No Owner" (cleanup opportunity)
- Longer execution time (initial Graph API query)

---

## Customization options

### **Change expiration window (30 → 60 days)**

Find this expression (appears twice):
```javascript
@ticks(addDays(utcNow(), 30))
```

Change to:
```javascript
@ticks(addDays(utcNow(), 60))
```

Locations:
- **Check_If_Expiring_Soon** (password check)
- **Check_Cert_Expiring_Soon** (certificate check)

---

### **Change execution schedule**

Default: Daily at 6 AM Eastern

Update the **Recurrence** trigger:
```json
{
    "recurrence": {
        "frequency": "Day",
        "interval": 1,
        "timeZone": "Eastern Standard Time",
        "schedule": {
            "hours": [6],
            "minutes": [0]
        }
    }
}
```

**Options:**
- Weekly: Change `frequency` to `"Week"`, add `"daysOfWeek": ["Monday"]`
- Twice daily: Add second hour: `"hours": [6, 18]`
- Different timezone: Change `timeZone` to valid Windows timezone

---

### **Add Teams notifications instead of email**

Replace the **Send_Email** action with **Post message in a chat or channel**:

```json
{
    "Post_Message": {
        "type": "ApiConnection",
        "inputs": {
            "host": {
                "connection": {
                    "referenceName": "teams"
                }
            },
            "method": "post",
            "body": {
                "recipient": {
                    "channelId": "your-channel-id"
                },
                "messageBody": "<html content here>"
            },
            "path": "/v1.0/teams/conversation/message/post"
        }
    }
}
```

---

### **Filter by app name pattern**

To only check apps matching a pattern (e.g., "Production-*"):

Add filter before **Process_Each_App**:
```json
{
    "Filter_Apps": {
        "type": "Query",
        "inputs": {
            "from": "@variables('allApps')",
            "where": "@startsWith(item()['displayName'], 'Production-')"
        }
    }
}
```

Then change `foreach` to use `@body('Filter_Apps')` instead of `@variables('allApps')`.

---

## Production lessons learned

### **1. Pagination is non-negotiable**

**Without pagination:**
- Logic App only sees first 100 apps
- Remaining 150+ apps invisible
- Credentials expire with zero detection
- False sense of security

**With pagination:**
- All 250+ apps monitored
- Caught Azure Migrate appliances (app #187, #188, #189)
- Complete coverage
- Actually works

---

### **2. Owner expansion requires User.Read.All**

**Without User.Read.All permission:**
- Graph API returns owner object IDs only
- No display names
- No email addresses
- Can't target notifications

**With User.Read.All:**
- Full owner details returned
- Display names in email table
- Email addresses for targeted notifications
- Actually useful

---

### **3. HTML email needs inline CSS**

**Attempted:** Link to external stylesheet

```html
<link rel="stylesheet" href="https://example.com/styles.css">
```

**Result:** Outlook strips external CSS, email looks broken

**Solution:** Inline all styles

```html
<style>
table{border-collapse:collapse;width:100%;}
th,td{border:1px solid #ccc;padding:8px;}
</style>
```

**Result:** Email renders correctly in Outlook, Gmail, mobile clients

---

### **4. Some apps have no owners**

**Reality:** 20-30% of app registrations have zero assigned owners

**Problem:** Logic App crashes if you assume owners exist

**Solution:** Defensive checks everywhere

```javascript
if(greater(length(items('Process_Each_App')?['owners']), 0), 
    items('Process_Each_App')?['owners'][0]?['displayName'], 
    'No Owner')
```

**Bonus:** "No Owner" entries highlight cleanup opportunities

---

### **5. Daily execution is sufficient for 30-day window**

**Considered:** Hourly execution for faster detection

**Reality:** Certificate expiration is a slow-moving problem
- 30-day warning window
- Renewals take days (procurement, approvals, coordination)
- Daily check catches everything
- Saves 720 Logic App executions/month

**Cost savings:** $0.09/month (not much, but multiplied by 100 Logic Apps = real money)

---

## Related use cases (beyond app registrations)

**This same pattern works for:**

### **1. Key Vault certificate expiration**

**Graph API query:**
```
GET https://management.azure.com/subscriptions/{sub}/providers/Microsoft.KeyVault/vaults?api-version=2023-02-01
```

Then for each vault:
```
GET https://{vault-name}.vault.azure.net/certificates?api-version=7.4
```

**Same Logic App structure:**
- Pagination handling
- Expiration date checking
- Email reporting

---

### **2. Azure reservation expiration**

**Query Azure Resource Graph:**
```kql
ReservationRecommendations
| where expiryDate < datetime_add('day', 30, now())
| project reservationId, name, expiryDate, costSavings
```

**Email teams 30 days before:**
- Reservation expiring
- Cost savings at risk
- Renewal recommendation

---

### **3. Managed identity credential rotation**

**Check managed identities:**
```
GET https://graph.microsoft.com/v1.0/servicePrincipals
  ?$filter=servicePrincipalType eq 'ManagedIdentity'
  &$select=appId,displayName,passwordCredentials
```

**Same expiration logic:**
- 30-day window
- Email alerts
- Proactive rotation

---

### **4. Service principal cleanup audit**

**Find unused service principals:**
```
GET https://graph.microsoft.com/v1.0/servicePrincipals
  ?$select=appId,displayName,signInActivity
```

**Filter by last sign-in:**
- No activity in 90 days
- Flag for review
- Cleanup candidates

---

## What Microsoft should provide (but doesn't)

**Azure Monitor should natively alert on:**
- App registration certificate expiration (30/60/90 days)
- Key Vault certificate expiration
- Service principal last sign-in
- Managed identity credential age

**Azure Portal should show:**
- Dashboard of expiring credentials
- Proactive email notifications
- Automated renewal workflows
- Owner assignment enforcement

**Instead, Microsoft provides:**
- Graph API endpoints
- Expiration date fields
- Manual checking via Portal
- "Build it yourself" expectation

**This Logic App fills the gap.**

---

## Download the complete solution

**Full Logic App definition (JSON):**
- Service principal authentication via Key Vault
- Paginated Graph API handling for 100+ apps
- Expiration checking for secrets and certificates
- Owner extraction and email targeting
- HTML report formatting with statistics
- Daily execution schedule

[Download Logic App JSON](/static/downloads/certificate-monitor-logic-app.json)

**Deployment guide (README):**
- Complete setup instructions
- Graph API permissions
- Key Vault configuration
- Connection setup
- Customization options
- Troubleshooting guide

[Download README](/static/downloads/certificate-monitor-README.md)

**Prerequisites:**
- Azure subscription
- Entra ID admin access (for granting Graph API permissions)
- Key Vault (or create new)
- Office 365 mailbox with send-as permissions

**Deployment time:** 30-45 minutes

**Monthly cost:** $1-2 (Consumption Logic App)

---

## The bigger pattern: Microsoft provides tools, not operations

**Same pattern across Azure:**

**Azure Migrate:** Provides discovery, hides 18-month certificate timer  
**Azure Arc:** Provides hybrid management, [creates 64% ghost registrations](/blog/azure-arc-ghost-registrations/)  
**Azure Monitor Workbooks:** Provides dashboards, [abandons them after 2 years](/blog/modernizing-azure-workbooks/)  
**App Registrations:** Provides authentication, doesn't monitor expiration

**Microsoft's position:**
- "Here's the API"
- "Here's the data"
- "Build your own monitoring"
- "This is cloud maturity"

**The operational reality:**
- Deploy the service: 1 hour
- Build monitoring: 8 hours
- Document procedures: 4 hours
- Maintain runbooks: Ongoing

**Total overhead:** ~15 hours per service × 50 services = 750 hours

**This is why senior Azure admins write blogs.**
