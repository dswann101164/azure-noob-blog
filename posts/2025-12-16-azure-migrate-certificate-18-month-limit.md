---
title: "Azure Migrate's 18-Month Data Deletion: The Enterprise Migration Timer Microsoft Calls 'Expected Behavior'"
date: 2025-12-16
summary: "Azure Migrate appliances have an 18-month hard limit before mandatory re-registration that deletes all discovery data. Microsoft documents this as 'expected behavior' in the FAQ but provides no alerts, no data preservation, and no migration path. The certificate expires at 12 months with one 6-month extension available, then forces complete appliance reconfiguration with total data loss at month 18."
tags:
  - Azure
  - Migration
  - Azure Migrate
  - Enterprise Reality
  - Governance
  - Compliance
  - Certificate Management
cover: /static/images/hero/azure-migrate-18-month-timer.png
hub: migration
related_posts:
  - cloud-migration-reality-check
  - azure-migration-roi-wrong
  - azure-arc-ghost-registrations
  - azure-hybrid-benefit-complete
  - azure-cost-optimization-what-actually-works
---

# Azure Migrate's 18-Month Data Deletion: The Enterprise Migration Timer Microsoft Calls 'Expected Behavior'

## Short Answer

Azure Migrate appliance certificates expire after 365 days with a one-time 6-month extension available via PowerShell script, creating an 18-month hard limit before mandatory re-registration. Re-registration requires running a cleanup script that deletes all discovery data, assessment history, and dependency mappings accumulated over 18 months. Microsoft documents this as "expected behavior" in the FAQ section but provides no proactive alerts, no data preservation option, and no migration path. Organizations discover this limitation either through proactive certificate monitoring (rare) or when authentication fails during active migration projects (common), forcing them to restart discovery from zero during critical migration phases.

## Why do Azure Migrate appliances stop working after 18 months?

Our Logic App that monitors certificate expirations flagged something unusual: three Azure Migrate appliances with certificates expiring in 28 days.

I opened a Microsoft support ticket expecting a standard renewal process.

**Support response:**

> "The Entra ID app certificate can be rotated using a PowerShell script. This extends the certificate validity for an additional 6 months. After that, you'll need to re-register the appliance."

**Me:** "Wait. Six months? Not another year? And what's 're-register'?"

**Support:** "Correct. After the 6-month extension, the appliance must be reconfigured. You'll need to run the cleanup script and start discovery over."

**Me:** "Start over? What happens to our 18 months of discovery data?"

**Support:** "The data will be deleted. It's documented behavior."

---

I checked Microsoft's documentation. This **critical limitation** is mentioned exactly **once** - buried in the FAQ section, question 20+ deep, with no warning during appliance deployment.

Here's the timeline Microsoft doesn't explain during deployment:

**Month 0:** Deploy Azure Migrate appliance  
**Months 1-11:** Discovery runs continuously, dependency mapping builds, assessments accumulate  
**Month 12:** Entra ID app certificate expires (365 days)  
**Month 12:** Run `AzureMigrateRotateCertificate.ps1` → **+6 months extension**  
**Month 18:** Certificate expires again → **No more extensions available**  
**Month 18:** Must re-register appliance = **all historical data deleted**

**For enterprise migrations that take 18-24 months, you're guaranteed to lose discovery data mid-project.**

This is part of our [Azure Migration hub](/hub/migration/) covering pre-migration planning, assessment reality checks, and lessons learned from real enterprise migrations at scale.

---

## What exactly happens when you "re-register" an Azure Migrate appliance?

**Cause:** The Entra ID application certificate reaches 18 months (365 days + 6-month extension) with no further renewal options available.

**Effect:** Discovery stops, assessments break, dependency mapping fails, and re-registration forces a complete appliance reconfiguration that deletes 18 months of accumulated migration intelligence.

**What to do:** Deploy certificate expiration monitoring before the 365-day window, run the rotation script at month 12 to gain 6 additional months, and plan for complete appliance redeployment with data loss before month 18.

---

From Microsoft's official documentation ([common-questions-appliance.md](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/migrate/common-questions-appliance.md)):

> **"To use the appliance with a different subscription or project, you would need to reconfigure the existing appliance by running the PowerShell installer script... The script will clean up the existing appliance components and settings to deploy a fresh appliance."**

> **"Also, you cannot reuse an existing project key on a reconfigured appliance."**

**Translation of "clean up the existing appliance components":**

- Discovery history: **Deleted**
- Assessment data: **Deleted**
- Dependency mappings: **Deleted**
- Server metadata: **Deleted**
- Performance baselines: **Deleted**

**Everything.**

And from Microsoft Q&A (Question 1150140), when an admin asked about re-registration:

> **Microsoft Support:** "You can try re-registering the appliance with the new project using another user account via PowerShell script but **it will break all the operations in the old project.**"

They won't say "you lose all your data" in public documentation. They say "break all the operations."

---

## Why doesn't Microsoft warn you about the 18-month limit?

**Where this IS documented:**
- Azure Migrate Appliance FAQ (question buried 20+ deep)
- One line: "default expiry period for the associated AD APP will be one year"
- Another line: "extend its validity for an additional 6 months"

**Where this ISN'T documented:**
- Appliance deployment wizard
- Azure Portal during registration
- Azure Migrate project creation
- Getting Started guides
- Migration planning documentation
- Anywhere with actual visibility

**The notification you get:**
- **None**
- Azure doesn't alert you
- The appliance doesn't warn you
- You discover this when authentication fails

**The proactive monitoring Microsoft provides:**
- **None**
- No Azure Monitor alert option
- No email notifications
- No portal warnings
- No "certificate expires in 30 days" message

**You find out when:**
- Discovery stops working
- Assessments fail to generate
- Migration waves can't start
- Support ticket reveals "working as designed"

---

## How we discovered this before it killed our migration

We deployed a Logic App to monitor expiring certificates across our Azure environment - primarily tracking app registrations and Key Vault certificates for security compliance.

**We weren't looking for Azure Migrate appliances specifically.**

The Logic App flagged them as part of its standard sweep of Entra ID applications with expiring certificates.

**The alert that appeared:**

```
Subject: Certificate Expiration Alert - 15 Applications

Applications with certificates expiring within 30 days:

...
- Application: AzureMigrate-DC1-Appliance
  Type: Service Principal
  Expires: 2026-01-15
  Certificate Thumbprint: A1B2C3D4...

- Application: AzureMigrate-DC2-Appliance  
  Type: Service Principal
  Expires: 2026-01-15
  Certificate Thumbprint: E5F6G7H8...

- Application: AzureMigrate-DR-Appliance
  Type: Service Principal
  Expires: 2026-01-18
  Certificate Thumbprint: I9J0K1L2...
...
```

**Our first reaction:** "What are these? We don't manage applications named 'AzureMigrate'."

**Second reaction:** "Wait. These are our migration appliances."

**Third reaction:** "Why do they have expiring certificates?"

That's when we opened the Microsoft support ticket.

**The Logic App wasn't built for this problem - it just happened to catch it.**

---

## The Logic App that accidentally saved our migration

**Original purpose:**
- Monitor app registration certificates (security compliance requirement)
- Track Key Vault certificate expirations (prevent service outages)
- Alert 30 days before expiration (give teams time to renew)

**What it actually caught:**
- 3 Azure Migrate appliances we'd forgotten about
- Certificate expirations we didn't know existed
- A Microsoft-documented "feature" we'd never read about

**The query:**

```kql
// Query all Entra ID applications with certificates
Resources
| where type == "microsoft.aadiam/servicePrincipals"
| extend certDetails = properties.keyCredentials
| mv-expand certDetails
| extend expiryDate = todatetime(certDetails.endDate)
| where expiryDate < now() + 30d
| project 
    appName = name,
    appId = properties.appId,
    expiryDate,
    thumbprint = tostring(certDetails.customKeyIdentifier),
    daysUntilExpiry = datetime_diff('day', expiryDate, now())
| order by daysUntilExpiry asc
```

**The Logic App workflow:**

1. **Daily trigger** - 6 AM UTC
2. **Query Entra ID** - Find all applications with certificates
3. **Filter expiring certs** - Anything < 30 days
4. **Send consolidated email** - All expiring certificates in one alert
5. **Include remediation links** - Generic "contact app owner" guidance

**Why this worked:**

Azure Migrate appliances register themselves as Entra ID applications during deployment. The certificate rotation problem exists at the Entra ID layer, not the appliance layer.

Our security compliance Logic App didn't care **what** the application was for - it just flagged **any** certificate expiring soon.

**The irony:**

- We built this for security compliance
- It accidentally caught an operational problem
- Microsoft should provide this monitoring
- But they don't
- So our compliance tool became our migration safety net

---

**Without this Logic App, we would have discovered the expiration when:**
- Discovery stopped working mid-migration
- Assessment reports failed during wave planning
- Migration validation broke during execution
- Support ticket revealed "working as designed, should have read the FAQ"

---

## What's the actual certificate rotation process?

Microsoft provides a PowerShell script for the 6-month extension. Here's what you run:

**Step 1: Open elevated PowerShell on the appliance VM**

```powershell
cd C:\'Program Files'\'Microsoft Azure Appliance Configuration Manager'\Scripts\PowerShell\AzureMigrateCertificateRotation
```

**Step 2: Run the rotation script**

```powershell
.\AzureMigrateRotateCertificate.ps1
```

**What the script does:**
1. Fetches Key Vault name and certificate details from appliance config
2. Generates new public/private key pair in Key Vault
3. Imports new certificate to appliance in PFX format
4. Deletes old certificate from Entra ID app
5. Attaches new certificate to Entra ID app
6. Updates appliance configuration files
7. Restarts Azure Migrate agents

**Duration:** 5-10 minutes  
**Downtime:** Discovery pauses during agent restart  
**Result:** +6 months of validity  

**Critical limitation:** This can only be run **once**. After the 6-month extension, no further rotation is possible.

---

## What happens at month 18 when the extension expires?

**Option 1: Re-register the appliance (lose all data)**

```powershell
# Run on appliance VM
cd C:\'Program Files'\'Microsoft Azure Appliance Configuration Manager'\Scripts
.\AzureMigrateInstaller.ps1 -Scenario VMware
```

**This script:**
- Deletes all appliance configuration
- Removes discovery data
- Clears assessment cache
- Resets dependency mappings
- Requires new project key from Azure Portal

**Result:** Clean appliance, zero historical data.

**Option 2: Deploy a new appliance (start over)**

- Download new OVA/VHD template
- Deploy to different VM
- Register with new project key
- Re-run complete discovery
- Rebuild assessment baselines

**Result:** Same as Option 1, but with a fresh VM.

**Option 3: Accept the data loss and continue**

- Wait for certificate to expire
- Discovery fails
- Fix it reactively
- Lose 18 months of dependency insights

**Result:** Same outcome, worse timing.

---

## Why this is a disaster for enterprise migrations

**Typical enterprise Azure migration timeline:**

**Months 1-3:** Discovery and initial assessment  
**Months 4-6:** Dependency mapping and application grouping  
**Months 7-9:** Migration wave planning and piloting  
**Months 10-12:** Wave 1 migration execution  
**Months 13-15:** Wave 2-3 execution  
**Months 16-18:** Final wave execution and optimization  
**Months 19-24:** Post-migration validation and decommissioning

**Azure Migrate appliance lifecycle:**

**Months 1-11:** Discovery accumulates  
**Month 12:** Certificate expires → Run rotation script (+6 months)  
**Months 13-17:** Continue discovery  
**Month 18:** Certificate expires → **Mandatory data deletion**  
**Months 19-24:** **Start discovery over during final migration phases**

**The problem:**

Your migration waves are based on dependency maps built over 18 months. You've identified:
- Application groups
- Database dependencies  
- Network flow patterns
- Authentication dependencies
- Shared services

**At month 18, you lose:**
- All dependency data
- Historical performance baselines
- Assessment trending
- Migration wave validation data

**And you're forced to:**
- Restart discovery from zero
- Wait 30 days for new dependency maps
- Re-validate application groups
- Potentially miss hidden dependencies
- Risk migration failures

---

## The bigger pattern: Enterprise Azure requires operational tooling Microsoft doesn't provide

This is the same pattern we've documented across Azure operations:

**Azure Migrate:** Provides discovery, hides the 18-month self-destruct timer  
**Azure Arc:** Provides hybrid management, [creates 64% ghost registrations](/blog/azure-arc-ghost-registrations/)  
**Azure Monitor Workbooks:** Provides dashboards, [abandons them after 2 years](/blog/modernizing-azure-workbooks/)  
**Azure Cost Management:** Provides cost data, [can't handle application-level allocation](/blog/azure-cost-optimization-what-actually-works/)

Microsoft builds the service. You build the operational monitoring. They call it "cloud maturity." We call it "filling the gaps."

**The operational reality:**

- Deploy Azure Migrate appliance: **45 minutes**
- Read documentation to discover 18-month limit: **Never, it's not in the deployment docs**
- Build certificate monitoring Logic App: **4 hours**
- Document rotation procedures: **2 hours**
- Plan for 18-month redeployment: **8 hours**
- Total operational overhead: **~15 hours**

**What Microsoft should provide:**

- Automatic certificate renewal (like every other Azure service)
- Portal alerts 90 days before expiration
- Data export before re-registration
- Migration path from old to new appliance
- Or just remove the 18-month limit entirely

---

## What you should do before deploying Azure Migrate

**Pre-deployment checklist:**

1. ✅ **Document deployment date** - The 18-month clock starts immediately
2. ✅ **Set calendar reminders:**
   - Day 300: Certificate expires in 65 days
   - Day 330: Certificate expires in 35 days (rotation time)
   - Day 350: Certificate expires in 15 days (escalate if not rotated)
   - Month 17: Plan for appliance replacement
3. ✅ **Deploy certificate monitoring** - Logic App or Azure Monitor
4. ✅ **Document rotation procedures** - PowerShell script location, required permissions
5. ✅ **Plan for 18-month replacement** - Budget, timeline, communication
6. ✅ **Test rotation in lab** - Don't learn the process in production
7. ✅ **Export assessment data quarterly** - Manual backup since Azure won't preserve it

**Operational procedures:**

**Month 12 - Certificate Rotation**
- Schedule maintenance window (10 minutes)
- Run `AzureMigrateRotateCertificate.ps1`
- Verify discovery resumes
- Document completion

**Month 17 - Replacement Planning**
- Deploy new appliance
- Run parallel discovery for 30 days
- Validate dependency parity
- Plan cutover

**Month 18 - Cutover**
- Switch production workflows to new appliance
- Export final data from old appliance
- Decommission old appliance
- Update documentation

---

## What should Microsoft change?

**Minimum viable fix:**

- Portal alerts 90/60/30 days before expiration
- Email notifications to project owners
- Warning banner in Azure Migrate dashboard

**Better fix:**

- Automatic certificate renewal (every other Azure service does this)
- Extend rotation to 12 months instead of 6 months
- Allow multiple rotations instead of one-time extension

**Actual fix:**

- Remove the 18-month limit entirely
- Provide appliance-to-appliance migration
- Preserve discovery data during re-registration
- Make this work like enterprise software should

**What we actually get:**

- FAQ documentation
- "Expected behavior" support responses
- Admins building their own monitoring
- Another operational gap to fill

---

## The documentation Microsoft should have provided but didn't

From [Azure Migrate Appliance FAQ](https://learn.microsoft.com/en-us/azure/migrate/common-questions-appliance):

> **"For a newly created Migrate appliance, the default expiry period for the associated AD APP (Entra Application) will be one year. To extend the validity of the Azure AD app, follow these steps..."**

**What it should say:**

> **WARNING: Azure Migrate appliances have an 18-month operational lifespan before mandatory data deletion.**
> 
> The Entra ID application certificate expires after 365 days. You can extend once for 6 additional months using a PowerShell script. After 18 months total, the appliance must be re-registered, which deletes all discovery data, assessment history, and dependency mappings.
> 
> **For enterprise migrations longer than 18 months:**
> - Plan appliance replacement before month 17
> - Deploy certificate monitoring immediately
> - Export assessment data quarterly
> - Budget for parallel discovery during cutover
> 
> **Microsoft does not provide:**
> - Proactive expiration alerts
> - Automatic certificate renewal
> - Data preservation during re-registration
> - Appliance-to-appliance migration tools
