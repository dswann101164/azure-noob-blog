---
title: "Azure Migration Checklist: 8 Critical Questions Before You Migrate"
date: 2025-11-14
modified: 2025-11-29
summary: "Complete Azure migration checklist: 80% of migration failures happen because you didn't ask these 8 questions BEFORE starting. License keys, vendor contacts, firewall rules, certificates - the enterprise migration checklist that actually works."
tags: ["azure", "migration", "operations", "enterprise", "checklist", "cloud-migration", "planning"]
cover: "/static/images/hero/application-migration-checklist.png"
hub: migration
related_posts:
  - cloud-migration-reality-check
  - azure-migrate-enterprise-hybrid
  - azure-migration-roi-wrong
  - azure-hybrid-benefit-complete
---
## The Problem Nobody Talks About


This guide is part of our [Azure Migration hub](/hub/migration/) covering assessment, planning, execution, and post-migration optimization.

You've read Microsoft's migration guides. You've attended the webinars. You've even done the Azure Migrate assessment. Everything looks green.

Then you start the actual migration and discover:
- Nobody knows where the license keys are stored
- The vendor contact left the company 3 years ago
- The firewall rules exist "somewhere in SharePoint"
- The certificate expires in 2 weeks and nobody knows how to renew it

**Sound familiar?**

After managing large-scale enterprise Azure migrations involving thousands of resources across dozens of subscriptions, I've learned this hard truth:

**Migrations don't fail because of technical problems. They fail because of institutional knowledge problems.**

The information you need exists somewhere in someone's head, in an old email, or in a spreadsheet that hasn't been updated since 2019. And you don't discover this until 2 AM during your maintenance window when the application won't start because you don't have the license key.

## The Checklist That Should Have Been In Microsoft's Docs

Here's what I actually use before approving any application migration. This isn't theory - this is what prevents 2 AM emergency calls.

### Question 1: Do you have a copy of the application software installation files?

**Why this matters:** You'd think this is obvious, but I've seen production applications where the installation media is literally on a CD-ROM in someone's desk drawer. Or the installer was downloaded 7 years ago and the vendor's website doesn't have that version anymore.

**What breaks when you don't have it:**
- You can't rebuild the application if the migration fails
- You can't spin up a test environment
- You're stuck on the current version forever (hope you like that security vulnerability)

**Real example:** Had an application where the "installer" was actually a series of manual configuration steps documented in a Word doc. When we migrated, the Word doc referenced screenshots that were broken links. Took 3 days to reverse-engineer what the actual configuration should be.

**The answer you want:** "Yes, and here's the exact path to the installer in our software repository with SHA-256 hash verification."

**The answer you'll probably get:** "I think Bob has it on his laptop?"

---

### Question 2: Do you have a copy of the Software License Key?

**Why this matters:** Because Azure doesn't magically know your on-premises license keys. And when the application starts asking for activation after migration, you better have it.

**What breaks when you don't have it:**
- Application won't start after migration
- Vendor wants to charge you again for a "new installation"
- You discover the license was tied to the old hardware MAC address

**Real example:** Migrated a database application, everything worked perfectly until the 30-day grace period expired. The license key was in an email from 2016. The person who received that email? Left the company 2 years ago. Had to pay $15K for an "emergency license" from the vendor.

**The answer you want:** "Yes, it's in our password vault with the maintenance contract that shows we're paid through 2027."

**The answer you'll probably get:** "It's installed, so it must be somewhere?"

---

### Question 3: Do you have the Vendor's Contact Information?

**Why this matters:** When things go wrong (and they will), you need to contact the vendor. Not the sales guy who cold-called you 5 years ago. The actual support contact who can help.

**What breaks when you don't have it:**
- Can't open a support ticket when migration fails
- Can't verify if Azure is a supported platform
- Can't get a new license key when the old one doesn't work

**Real example:** Application vendor had been acquired twice since we bought the software. The support website redirected to a dead URL. Took 2 weeks to find someone at the new parent company who even knew this product existed.

**The answer you want:** 
- Support portal URL
- Account number or customer ID
- Primary and secondary technical contacts
- Support plan tier (24/7 or business hours only)

**The answer you'll probably get:** "Can't we just Google them?"

---

### Question 4: Is the application software still supported by the vendor?

**Why this matters:** If the vendor doesn't support the version you're running, they DEFINITELY won't support it in Azure. And when it breaks, you're on your own.

**What breaks when you don't have it:**
- Vendor refuses to help because "that version is end-of-life"
- No security patches available
- Compliance audit finds unsupported software in production

**Real example:** Migrated an application that was 2 major versions behind. Vendor said "we'll support it in Azure if you upgrade first." Upgrade cost $50K. Migration got delayed 3 months.

**The answer you want:** "Yes, we're on the current major version with active support through [date], and the vendor has confirmed Azure is a supported platform."

**The answer you'll probably get:** "It works, so it must be supported?"

---

### Question 5: Does the software currently have Firewall Rules in place?

**Why this matters:** Because Azure isn't going to magically know what ports your application needs. And Network Security Groups default to blocking everything.

**What breaks when you don't have it:**
- Application can't talk to the database (port blocked)
- Users can't access the application (NSG blocking traffic)
- Backend services can't communicate (forgot about that obscure port 8447)

**Real example:** Migrated a web application. Frontend worked perfectly. Backend batch jobs failed silently because they used port 8443 for API calls and nobody documented it. Took a week to figure out why the nightly jobs weren't running.

**The answer you want:** Complete firewall rule export including:
- Source IPs/ranges
- Destination IPs/ranges  
- Ports and protocols
- Service names (not just numbers)
- Why each rule exists (seriously, document this)

**The answer you'll probably get:** "Let me ask the network team... they don't work here anymore."

---

### Question 6: Does the application deal with PCI data?

**Why this matters:** Because if it touches credit card data, you just signed up for a completely different migration process with compliance requirements, audit trails, and encryption at rest.

**What breaks when you don't have it:**
- Compliance violation discovered mid-migration
- Have to retrofit encryption and access controls
- Audit holds up production deployment

**Real example:** Application "didn't deal with PCI data" according to the application owner. Turns out it logged full credit card numbers in debug mode. Had to redesign the logging, implement encryption, and get a new PCI audit. Added 2 months to migration.

**The answer you want:** "No, this application never touches payment card data, and here's the data flow diagram to prove it."

**The answer that should make you nervous:** "I don't think so?"

---

### Question 7: Does the application currently sit behind a VIP (or load balancer)?

**Why this matters:** Because load balancer configuration isn't in Active Directory, it's not in DNS, and it's probably not documented anywhere. But if you don't recreate it in Azure, your application won't work the same way.

**What breaks when you don't have it:**
- High availability features don't work
- Health checks aren't configured correctly
- Session persistence breaks (RIP your shopping carts)
- SSL offloading configured wrong

**Real example:** Application was behind an F5 load balancer with complex health check logic. Migrated to Azure Application Gateway without understanding the health check was hitting a specific URL that validated database connectivity. Customers got served cached error pages for 2 hours before we figured it out.

**The answer you want:** Complete load balancer export including:
- Virtual IP addresses
- Health check configuration
- Session persistence method
- SSL/TLS settings
- Backend pool members and weights

**The answer you'll probably get:** "It has high availability, so yes?"

---

### Question 8: Does the application have any certificate(s) installed?

**Why this matters:** Because certificates don't migrate automatically, they usually can't be exported without the private key password, and they're probably going to expire during your migration window.

**What breaks when you don't have it:**
- HTTPS doesn't work (browser warnings)
- API authentication fails
- Backend services can't validate each other
- Certificate expires mid-migration and nobody can renew it

**Real example:** Application had 5 certificates installed. Three were expired but the application wasn't using them (tech debt from previous projects). One was from an internal CA that didn't exist anymore. One was valid but nobody had the private key password. Ended up getting new certificates from a public CA and updating all the configuration. Added 2 weeks to the migration.

**Follow-up questions you need to ask:**

**8a. Is the certificate provided by an internal Certificate Authority (CA)?**
- If yes: Contact your internal CA team BEFORE migration
- They need to issue new certificates for the Azure environment
- Verify the CA is still operational (I've seen internal CAs decommissioned)

**8b. Is the certificate provided by a Vendor?**
- If yes: Contact the vendor for Azure-specific certificates
- Some vendors tie certificates to hardware (which won't exist in Azure)
- Get this sorted BEFORE your maintenance window

**8c. Are you able to provide us with a copy of the certificate?**
- You need both the certificate AND the private key
- You need the password for the private key
- You need to know where it's installed (MMC, app config, Java keystore, etc.)

**The answer you want:** "Yes, here's the certificate, private key, password, expiration date, and renewal process documentation."

**The answer you'll probably get:** "It's in IIS somewhere?"

---

## The Ugly Truth About Enterprise Migrations

Here's what Microsoft's migration guides don't tell you:

**The technical migration is the easy part.** Azure Migrate can move VMs. Azure Database Migration Service can move databases. ASR can replicate entire environments.

**The hard part is institutional knowledge.** The information about how things actually work exists in:
- Someone's head (and they're on vacation)
- An email from 2017 (good luck finding it)
- A SharePoint site (that got archived)
- A Word doc (on a file share that doesn't exist anymore)
- "Tribal knowledge" (which means nowhere)

**This checklist isn't about technology. It's about organizational memory.**

## How to Actually Use This Checklist

Don't wait until migration day to ask these questions. Here's the process that works:

### Step 1: Run the checklist 30 days before migration
Send this to the application owner. Make them fill it out. If they put "Don't Know" for anything, that's a red flag.

### Step 2: Verify the answers
Don't just accept "Yes" as an answer. Make them show you:
- The actual installer files
- The actual license key (test it)
- The actual firewall rules (export them)
- The actual certificates (export them with private keys)

### Step 3: Document everything in a runbook
Create a migration runbook that includes:
- Every answer from this checklist
- Screenshots of current configuration
- Export of current settings
- Contact information for vendor support
- Rollback procedures

### Step 4: Test the migration in a dev environment
Don't go straight to production. Use these answers to build a test environment and verify everything works.

## The Template

I've turned this into an Excel template you can actually use. It includes:
- All 8 questions
- Space for additional information
- Answer key (Yes/No/Not Applicable/Don't Know)
- Instructions for application owners

**Download it here:** [Azure Application Migration Checklist Template](/static/downloads/Azure-Application-Migration-Checklist.xlsx)

## What's Missing From This Checklist

This checklist covers the basic technical stuff. But here's what it doesn't cover (and probably should):

- **Database connection strings** (where are they configured?)
- **Service accounts** (what are they, and do they work in Azure AD?)
- **Scheduled tasks** (how do they run, and do they need Windows Task Scheduler?)
- **Integration dependencies** (what other systems does this talk to?)
- **Custom DNS entries** (will they resolve in Azure?)
- **Monitoring configuration** (how do you know if it's working?)

Maybe that's a different blog post.

## The Bottom Line

**Before you migrate anything to Azure, ask these 8 questions.** 

If you get "Don't Know" for more than 2 questions, you're not ready to migrate. Go find the answers first.

If the application owner gets defensive about filling this out, that tells you everything you need to know about how this migration is going to go.

**The information you need exists somewhere.** Find it before your maintenance window, not during it.

Trust me, your future self at 2 AM will thank you.

---

*Got questions about application migrations? Hit me up - I've probably broken it the same way you're about to.*

*Working on your own Azure migration? Want to share your war stories? I'm always looking for real-world examples of what actually breaks in production.*