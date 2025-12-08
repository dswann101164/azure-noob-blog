---
title: "The Missing SOC 2 Guide: Azure Activity Log Setup (Grill Assembly Manual Edition)"
date: 2025-10-27
summary: "Every guide says 'configure diagnostic settings.' Nobody shows you which button to click. Here's the step-by-step tutorial that actually works, written for someone who's never done this before."
tags: ["azure", "SOC2", "Compliance", "Monitoring", "Activity Logs"]
cover: "/static/images/hero/azure-soc2-activity-log.svg"
---

Last week I published [The Azure Audit Gap Nobody Talks About](/blog/azure-audit-gap-nobody-talks-about/). The response was overwhelming: "This is great, but WHERE DO I START?"

Every Azure SOC 2 guide I've found says the same thing: "Configure diagnostic settings for Activity Logs to meet SOC 2 requirements."

Cool. **Which button do I click?**

Nobody tells you. It's like buying a grill from Home Depot and the instructions say "assemble the grill" with no pictures, no step numbers, no "insert bolt D into hole E."

Here's the grill assembly manual version. Follow these steps, and in 30 minutes you'll have SOC 2-compliant Activity Log retention. No guessing. No "figure it out yourself." Just click what I tell you to click.

## What You're Actually Setting Up

**The problem:** Azure keeps Activity Logs for 90 days. SOC 2 requires 12+ months. When your auditor asks "who deleted this storage account in March?" six months later, you have nothing.

**The solution:** Export Activity Logs to two places:
1. **Log Analytics Workspace** - Query logs for 12+ months using KQL
2. **Storage Account** - Archive logs for 7 years (cheap long-term storage)

**Time required:** 30 minutes to set up, 5 minutes to verify

**What you need:**
- Azure account with Owner or Contributor permissions on a subscription
- 30 minutes of your time
- Coffee (you'll wait 15 minutes for logs to sync)

**Cost:** $7-15/month for small environments, $60-170/month for medium, $730-950/month for enterprise

Let's do this.

---

## Part 1: Create Log Analytics Workspace (10 minutes)

This is where you'll run KQL queries to answer audit questions like "who did what when?"

### Step 1: Open Azure Portal and Search

1. Go to **portal.azure.com** in your browser
2. Sign in with your Azure account
3. Look at the **search bar at the very top** - it says "Search resources, services, and docs (G+/)"
4. Click in that search bar
5. Type: `log analytics workspaces`
6. Click **"Log Analytics workspaces"** in the dropdown results (has a database icon)

**You should see:** A page titled "Log Analytics workspaces" with a list of existing workspaces (might be empty if this is your first one)

**If you see an error:** Check if you're signed in to the correct subscription. Click your profile icon (top right) to verify.

---

### Step 2: Create New Workspace

1. Look at the top-left of the page
2. Click the **"+ Create"** button (blue button with a plus sign)

**You should see:** A new page opens titled "Create Log Analytics workspace" with tabs at the top: Basics, Tags, Review + create

---

### Step 3: Fill in the Basics Tab

You're on the **"Basics"** tab. Fill in these fields:

**Subscription:**
- Click the dropdown
- Select your subscription (if you only have one, it's already selected)
- **Write this down on paper:** _________________ (you'll need it in Part 3)

**Resource Group:**
- Click the dropdown
- Do you see a resource group for governance/compliance stuff? Use that.
- If not (or you're starting fresh):
  - Click **"Create new"** below the dropdown
  - A popup appears
  - Type exactly: `soc2-compliance-rg`
  - Click **"OK"**
- **Write this down:** _________________

**Name:**
- Type: `soc2-audit-logs`
- **If Azure says "Name not available"** (red error):
  - Add random numbers: `soc2-audit-logs-847`
  - Keep trying different numbers until you get a green checkmark
- **Write this name down:** _________________ (critical - you need this in Part 3)

**Region:**
- Click the dropdown
- Pick any region (I use "East US" but it doesn't really matter)
- **Write this down:** _________________

**Pricing tier:**
- Leave as **"Pay-as-you-go"** (this is correct, don't change it)

**You should see:** All fields filled in, no red error messages

---

### Step 4: Set Retention Period

This is critical for SOC 2 compliance.

1. Click the **"Pricing tier"** tab at the top (next to "Basics")
2. You should see a section labeled **"Data retention"**
3. Look for a slider or input box
4. **Set it to 365 days** (drag slider right, or type `365` in the box)

**Why 365 days?** SOC 2 requires minimum 12 months. This is the cheapest option that meets compliance. Going higher (730 days = 2 years) costs more but gives you safety margin.

**You should see:** "365" displayed clearly

---

### Step 5: Skip Tags, Create the Workspace

1. Click **"Review + create"** button at the bottom left (skip the Tags tab - you can add tags later)
2. **Wait 5 seconds** - Azure validates your settings
3. **You should see:** Green checkmark with "Validation passed"
4. **If you see a red X:** Read the error message. Most common issues:
   - Name already taken → Go back to Step 3, pick different name
   - No permissions → Contact your Azure admin, you need Owner or Contributor role
5. Click the **"Create"** button at the bottom left
6. **Wait 1-2 minutes** - You'll see a blue "Deployment in progress" spinner

**You should see:** Green checkmark saying "Your deployment is complete"

---

### Step 6: Verify It Worked

1. Click the **"Go to resource"** button (it appears after deployment completes)
2. You're now looking at your workspace dashboard

**You should see:**
- Page title at the top shows your workspace name (like "soc2-audit-logs")
- Green "Succeeded" status
- Information like Resource group, Subscription ID, Location

**Write down these three things:**
- Workspace name: _________________
- Resource group: s_________________ (should be soc2-compliance-rg)
- Subscription: _________________ (should match what you picked earlier)

**Checkpoint:** You now have a Log Analytics Workspace. This is where Activity Logs will be stored for 365 days and where you'll run queries. ✓

---

## Part 2: Create Storage Account (10 minutes)

This is your cheap long-term archive for 7-year retention. Costs pennies compared to Log Analytics.

### Step 7: Search for Storage Accounts

1. Click the **search bar** at the very top of the page
2. Type: `storage accounts`
3. Click **"Storage accounts"** in the dropdown (has a box/container icon)

**You should see:** "Storage accounts" page with a list of storage accounts (might be empty)

---

### Step 8: Create New Storage Account

1. Look at the top-left
2. Click **"+ Create"** button (blue button with plus sign)

**You should see:** "Create a storage account" form with multiple tabs

---

### Step 9: Fill in Basics

You're on the "Basics" tab. Fill these in:

**Subscription:**
- Select the **same subscription** you used in Part 1

**Resource group:**
- Click dropdown
- Select **"soc2-compliance-rg"** (the one you created or used in Part 1)

**Storage account name:**
- Type: `soc2archive` + today's date
- Example: `soc2archive20251027`
- **Rules:** Must be lowercase, 3-24 characters, numbers and letters only, no spaces, no dashes, no underscores
- **If "Name not available":** Try `soc2logs20251027` or add your initials
- **Write this name down:** _________________

**Region:**
- Select **the same region** you used for the workspace in Part 1 (probably "East US")

**Performance:**
- Leave as **"Standard"** (should be pre-selected)
- Don't change to Premium (costs 10x more, unnecessary for logs)

**Redundancy:**
- Click the dropdown
- Select **"Locally-redundant storage (LRS)"**
- Why? Cheapest option ($0.02/GB/month). You don't need geo-redundancy for archived logs.

**You should see:** All fields filled, no red errors

---

### Step 10: Create the Storage Account

1. Click **"Review"** button at the bottom left (skip Advanced, Networking, Data protection, Encryption, Tags tabs)
2. Wait 5 seconds for validation
3. **You should see:** "Validation passed" with green checkmark
4. Click **"Create"** button at the bottom left
5. **Wait 2 minutes** - Deployment runs

**You should see:** "Your deployment is complete" with green checkmark

6. Click **"Go to resource"** button

**You should see:** Storage account overview page with your storage account name at the top

**Write down:**
- Storage account name: _________________ (like soc2archive20251027)
- Resource group: soc2-compliance-rg
- Location: (should match workspace region)

**Checkpoint:** You now have a Storage Account for 7-year log archive. ✓

---

## Part 3: Export Activity Logs (10 minutes)

Now you connect the dots: tell Azure to send Activity Logs to both places you just created.

### Step 11: Open Activity Log Settings

1. Click the **search bar** at the very top of the page
2. Type: `activity log`
3. Click **"Activity Log"** in the dropdown (has a clock icon)

**You should see:** A page showing recent Azure activities - a table with columns like "Time," "Resource," "Operation," "Status"

4. Look at the **left sidebar** (dark blue vertical area on the left side of the page)
5. Scroll down about halfway
6. Find and click **"Export Activity Logs"**

**You should see:** Page titled "Diagnostic settings" at the top

**What you might see:**
- Empty page saying "No diagnostic settings defined yet" (this is fine - you're setting it up now)
- OR existing settings in a table (like "AzureKeyVault" - ignore these, you're adding a new one)

---

### Step 12: Create New Diagnostic Setting

1. Look at the top of the page
2. Click **"+ Add diagnostic setting"** button (blue button near the top)

**You should see:** A form opens on the right side with lots of checkboxes, dropdowns, and options

---

### Step 13: Name Your Setting

Look at the very top of the form. You'll see **"Diagnostic setting name"** field.

Type exactly: `soc2-activity-logs`

**Why this name?** When your auditor asks "show me your Activity Log exports," you can instantly point to "soc2-activity-logs" in the list. Makes your life easier during audits.

---

### Step 14: Select ALL Log Categories

This is critical. Don't skip any boxes.

Scroll down to the **"Logs"** section. You'll see a list of categories with checkboxes.

**Check EVERY SINGLE BOX (all 8):**

- ☑ **Administrative**
- ☑ **Security**
- ☑ **ServiceHealth**
- ☑ **Alert**
- ☑ **Recommendation**
- ☑ **Policy**
- ☑ **Autoscale**
- ☑ **ResourceHealth**

**Why all 8?** Here's what each one gives you:
- **Administrative:** Who created/deleted/modified resources (critical for SOC 2 CC6.1)
- **Security:** Security alerts, policy violations
- **ServiceHealth:** Azure outages that might have affected your resources
- **Alert:** Monitoring alerts that fired
- **Recommendation:** Azure Advisor recommendations
- **Policy:** Azure Policy violations (governance failures)
- **Autoscale:** Autoscaling events (capacity changes)
- **ResourceHealth:** Resource health status changes

SOC 2 auditors ask random questions like:
- "Show me when this resource failed" (ResourceHealth)
- "Who changed this security setting?" (Administrative + Security)
- "What alerts fired during this incident?" (Alert)
- "Were there any policy violations?" (Policy)

If you only check some boxes, you'll miss data you need later during the audit.

**Double-check:** All 8 boxes should have checkmarks. Scroll through the list to verify.

---

### Step 15: Configure Log Analytics Destination

Scroll down to the **"Destination details"** section.

**First destination: Log Analytics (for queries)**

1. Find and **check the box** next to **"Send to Log Analytics workspace"**
2. Two new dropdowns appear below it:

**Subscription dropdown:**
- Click it
- Select your subscription (same one you've been using)
- Should match what you wrote down in Step 3

**Log Analytics workspace dropdown:**
- Click it
- Select **"soc2-audit-logs"** (the workspace you created in Part 1)
- **If you don't see it:** Something went wrong in Part 1. Go back to Step 6, verify the workspace exists.

**You should see:** Both dropdowns filled in, no red errors

---

### Step 16: Configure Storage Account Destination

Still in the **"Destination details"** section, right below where you just were.

**Second destination: Storage Account (for 7-year archive)**

1. Find and **check the box** next to **"Archive to a storage account"**
2. Three new fields appear:

**Subscription dropdown:**
- Click it
- Select your subscription (same as before)

**Storage account dropdown:**
- Click it
- Select your storage account: **"soc2archive20251027"** (or whatever you named it in Part 2)
- **If you don't see it:** Go back to Step 12, verify the storage account exists

**Retention (days) field:**
- Click in the box
- Delete any existing number
- Type: `2555`
- **Why 2555?** That's 7 years (7 × 365 = 2,555 days). SOC 2 often wants this. SOX requires it. Better to have it and not need it than vice versa.

**You should see:** All three fields filled in correctly

**Visual check:** You should now have TWO checked destinations:
- ☑ Send to Log Analytics workspace (with workspace selected)
- ☑ Archive to a storage account (with storage account selected and 2555 days)

---

### Step 17: Save It

1. **Look at the very top** of the form (might need to scroll up)
2. Find the **"Save"** button (top-left area, near the X button)
3. Click **"Save"**
4. **Wait 10 seconds** - Azure is saving your configuration

**You should see:**
- Green notification in the top-right saying "Successfully saved diagnostic setting 'soc2-activity-logs'"
- The form closes
- You're back at the "Diagnostic settings" page
- You should now see "soc2-activity-logs" in the table

**If you see a red error instead:**

Most common issues:
- **"Insufficient permissions"** → You need Owner or Contributor role on the subscription. Contact your Azure admin.
- **"Storage account not found"** → Go back to Step 16, double-check you selected the correct storage account
- **"Workspace not found"** → Go back to Step 15, verify the workspace name

**Checkpoint:** Activity Logs are now being exported to both Log Analytics (365 days) and Storage (7 years). ✓

---


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

## Part 4: Verify It's Working (Critical - Don't Skip)

This is how you know it actually worked. I've seen people skip this step and discover 6 months later during an audit that logs weren't being exported.

### Step 18: Wait 15 Minutes (Seriously)

Set a timer. Go grab coffee. Check your email. Walk around the block.

Azure needs 15-30 minutes to start sending Activity Log data to Log Analytics. First sync is always slow.

**Do not skip the wait.** If you check immediately, you'll see no results and panic unnecessarily.

---

### Step 19: Open Log Analytics Query Editor

After your 15-minute coffee break:

1. Click the **search bar** at the top of the portal
2. Type: `log analytics workspaces`
3. Click **"Log Analytics workspaces"**
4. Find and click your workspace: **"soc2-audit-logs"**

**You should see:** Your workspace overview page

5. Look at the **left sidebar**
6. Find and click **"Logs"** (about halfway down, has a chart/graph icon)

**If a tutorial popup appears:**
- It says "Get Started with Log Analytics" or similar
- Click **"Get Started"** button
- Then immediately click the **X** in the top-right to close it
- You don't need the tutorial right now

**You should see:** A query window with:
- A large white text box (this is where you type queries)
- A blinking cursor in the box
- A blue "Run" button above the box
- A list of tables on the left (you might see "AzureActivity" in the list)

---

### Step 20: Run Your First Test Query

This query checks if Activity Logs are arriving.

1. **Click in the query window** (the white text box)
2. **Delete any existing text** if there is any
3. **Type this exactly** (or copy/paste):

```kql
AzureActivity
| take 10
```

**What this does:** Gets 10 recent Activity Log entries. Simple test to see if data is flowing.

4. Press **Shift + Enter** on your keyboard (or click the blue **"Run"** button)
5. **Wait 5-10 seconds** - Query is running

**YOU SHOULD SEE:**

A table appears below the query window with:
- 10 rows of data
- Columns like "TimeGenerated," "Caller," "OperationName," "ResourceId," "ActivityStatusValue"
- TimeGenerated dates should be recent (within the last few hours)
- Caller shows email addresses or service principals
- OperationName shows things like "MICROSOFT.RESOURCES/SUBSCRIPTIONS/RESOURCEGROUPS/WRITE"

**If you see this:** ✅ **SUCCESS! Your Activity Logs are flowing correctly.**

**IF YOU SEE "No results found" or empty table:**

Don't panic. Try these steps in order:

1. **Check the time range** - Look above the query window. You might see "Time range: Last 24 hours" or similar. Change it to "Last 7 days" and run again.

2. **Wait another 15 minutes** - First sync can take 30-45 minutes total. Set another timer. Check again.

3. **Generate some activity** - Create a test resource group:
   - Search for "resource groups"
   - Click "+ Create"
   - Fill in: Name = "test-soc2", Region = East US
   - Click "Review + create" then "Create"
   - Wait 5 minutes
   - Run the query again

4. **Still nothing after 60 minutes total?** Something's wrong. Go back to Part 3:
   - Step 14: Verify ALL 8 boxes are checked (especially "Administrative")
   - Step 15: Verify correct workspace selected
   - Step 17: Verify you saw the green "Successfully saved" message

---

### Step 21: Check Retention (Proves Logs Are Staying)

This query shows how many days of logs you have.

In the query window, **delete the previous query** and type this:

```kql
AzureActivity
| summarize 
    OldestLog = min(TimeGenerated),
    NewestLog = max(TimeGenerated),
    DaysCovered = datetime_diff('day', max(TimeGenerated), min(TimeGenerated))
```

Press **Shift + Enter** to run it.

**YOU SHOULD SEE:**

A table with 1 row showing:
- **OldestLog:** Earliest Activity Log you have (probably today or yesterday)
- **NewestLog:** Most recent Activity Log (probably a few minutes ago)
- **DaysCovered:** 0 or 1 (since you just set this up)

**This is normal.** You just configured this. You don't have 365 days of logs yet.

**IMPORTANT - Mark Your Calendar:**

- **In 7 days:** Run this query again. DaysCovered should be ~7.
- **In 30 days:** Run it again. DaysCovered should be ~30.
- **In 90 days:** Run it again. DaysCovered should be ~90.
- **In 365 days:** Run it again. DaysCovered should be ~365.

**When DaysCovered hits 365, you're officially SOC 2 compliant for Activity Log retention.** ✓

Save this query somewhere (OneNote, wiki, Confluence) so you can run it quarterly.

---

### Step 22: Test a Real Audit Query

Let's make sure you can actually answer audit questions.

Try this query that finds resource deletions (common audit question):

```kql
AzureActivity
| where TimeGenerated >= ago(7d)
| where OperationName contains "DELETE"
| where ActivityStatusValue == "Success"
| project TimeGenerated, Caller, ResourceId, ResourceGroup, OperationName
| order by TimeGenerated desc
```

**What this does:** Shows all successful resource deletions in the last 7 days, who did it, and what they deleted.

**YOU SHOULD SEE:**

Either:
- **A table with rows** (if anyone deleted resources recently) - Shows when, who, and what was deleted
- **OR "No results found"** (if nobody deleted anything) - This is fine, means no deletions

**If you see results:** Great! You can now answer the audit question "Show me all resource deletions in Q3 2025."

**Save this query** - You'll use it during audits.

---

## What You Can Do Now

You just set up SOC 2-compliant Activity Log retention. Here's what this enables:

### Audit Question 1: "Who created storage account 'proddata001' on September 15, 2025?"

```kql
AzureActivity
| where TimeGenerated between (datetime(2025-09-15) .. datetime(2025-09-16))
| where ResourceId contains "proddata001"
| where OperationName contains "CREATE" or OperationName contains "WRITE"
| where ActivityStatusValue == "Success"
| project TimeGenerated, Caller, OperationName, ResourceId
```

**Answer:** The Caller column shows who did it. TimeGenerated shows exactly when.

---

### Audit Question 2: "Show me all resource deletions in the last 90 days"

```kql
AzureActivity
| where TimeGenerated >= ago(90d)
| where OperationName contains "DELETE"
| where ActivityStatusValue == "Success"
| project TimeGenerated, Caller, ResourceId, ResourceGroup
| order by TimeGenerated desc
```

**Answer:** Every row is a deletion. Export to Excel for the auditor.

---

### Audit Question 3: "What changes did john.doe@company.com make last month?"

```kql
AzureActivity
| where Caller contains "john.doe@company.com"
| where TimeGenerated >= ago(30d)
| project TimeGenerated, ResourceGroup, ResourceId, OperationName, ActivityStatusValue
| order by TimeGenerated desc
```

**Answer:** Complete audit trail of everything this user did.

---

### Audit Question 4: "Were there any policy violations in Q2 2025?"

```kql
AzureActivity
| where TimeGenerated between (datetime(2025-04-01) .. datetime(2025-06-30))
| where CategoryValue == "Policy"
| where ActivityStatusValue == "Failure"
| project TimeGenerated, Caller, OperationName, Properties
| order by TimeGenerated desc
```

**Answer:** Every policy failure, who triggered it, when.

---

## Cost Breakdown

**What this setup actually costs:**

### Small Environment (1-3 subscriptions)
- **Log Analytics:** ~$2-10/month
  - First 5GB/month is free
  - After that: $2.76/GB ingested + $0.12/GB/month retention
  - Small environments generate 1-3GB/month of Activity Logs
- **Storage Account:** ~$2-5/month
  - Cool tier: $0.01/GB/month
  - 7 years of logs ≈ 200-500GB total = $2-5/month
- **Total: $4-15/month**

### Medium Environment (10-20 subscriptions)
- **Log Analytics:** ~$50-150/month
  - 20-50GB/month ingested
- **Storage Account:** ~$10-20/month
  - 1-2TB archived
- **Total: $60-170/month**

### Enterprise (40+ subscriptions, like mine)
- **Log Analytics:** ~$700-900/month
  - 250-300GB/month ingested
  - Multiple environments, lots of activity
- **Storage Account:** ~$30-50/month
  - 3-5TB archived over 7 years
- **Total: $730-950/month**

**ROI Check:**
- One failed SOC 2 audit finding: $50,000-$500,000 in remediation costs + penalties
- One security breach investigation without logs: $100,000+ in forensics consulting
- This solution: $48-11,400/year

No-brainer.

---

## Common Mistakes to Avoid

### Mistake 1: Only Checking "Administrative" in Step 14

**Why it's wrong:** You'll miss Security logs, Policy violations, and other categories auditors ask for.

**Fix:** Check all 8 boxes. Every single one matters.

---

### Mistake 2: Skipping Part 4 (Verification)

**Why it's wrong:** You won't know if it's working until the audit, when it's too late to fix.

**Fix:** Actually run the test queries. Verify you see results. Check again in 7 days, 30 days, 90 days.

---

### Mistake 3: Setting Retention to 30 or 90 Days

**Why it's wrong:** SOC 2 requires 12+ months minimum. Setting 90 days means you fail compliance.

**Fix:** Set Log Analytics retention to 365 days (Step 4). Set Storage retention to 2,555 days (Step 16).

---

### Mistake 4: Not Documenting What You Did

**Why it's wrong:** When your coworker asks "where are our Activity Logs?" in 6 months, nobody remembers.

**Fix:** Create a one-page doc:
- Workspace name: soc2-audit-logs
- Storage account: soc2archive20251027
- Retention: 365 days (LAW), 7 years (Storage)
- Configured by: [your name]
- Date: [today's date]
- Purpose: SOC 2 CC6.1, CC6.7 compliance

Save it in SharePoint, Confluence, or your internal wiki.

---

### Mistake 5: Thinking This Covers Azure AD

**Why it's wrong:** This guide covers Activity Logs (ARM resources like VMs, storage, networks). Azure AD logs (users, app registrations, sign-ins) are a completely separate system.

**Fix:** You still need to configure Azure AD diagnostic settings separately. That's a different guide (coming next week).

---

## What's Next

You just set up **Activity Logs** (ARM resources - VMs, storage accounts, networks).

**You're 50% done with SOC 2 logging compliance.**

The other 50% is **Azure AD Audit Logs** (identity layer):
- User sign-ins
- App registration creation
- Admin consent grants
- Role assignments
- Password resets

That's a separate system with different configuration. I'll cover that in next week's post.

For now, you're compliant with:
- **SOC 2 CC6.1** (Logical Access Controls) - You can prove who accessed what
- **SOC 2 CC6.7** (System Monitoring) - You have 12+ months of monitoring data

---

## Quick Reference Card

Copy this, print it, stick it on your desk:

**Activity Log Setup - Quick Facts**

- **Workspace:** soc2-audit-logs (365 days)
- **Storage:** soc2archive[date] (7 years)
- **Diagnostic Setting:** soc2-activity-logs
- **All 8 categories:** ✓ checked
- **Test Query:** `AzureActivity | take 10`
- **Retention Check:** Run quarterly (check DaysCovered)
- **Cost:** $4-15/month (small), $60-170/month (medium), $730-950/month (enterprise)
- **Compliant with:** SOC 2 CC6.1, CC6.7

---

## The Real Takeaway

This is the guide nobody wrote. Every SOC 2 Azure article says "configure diagnostic settings." None show you how.

Now you know. Every button, every dropdown, every checkbox, every KQL query you need.

Next time your auditor asks "show me who deleted this resource in March," you'll have an answer in 30 seconds instead of panic-calling your Azure admin.

That's the difference between passing and failing the audit.

**Questions? Stuck on a step? Email me at contact@azure-noob.com or drop a comment below.**

And if you found this useful, share it with your compliance team. They'll thank you when audit season rolls around.
