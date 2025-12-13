---
title: "If You Can't Code Your Architecture, You're Not an Architect"
date: 2025-10-14
summary: "Deploy one VM to learn the variables. Deploy three VMs to learn you're wasting time. Code your fourth deployment or admit you're just clicking buttons for a living."
tags: ["azure", "Architecture", "Terraform", "IaC", "Career"]
cover: "static/images/hero/code-architecture.svg"
hub: governance
---
# If You Can't Code Your Architecture, You're Not an Architect


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

**Here's the uncomfortable truth:** Azure architects who can't code their infrastructure are slow, inconsistent, and undocumented. They're expensive button-clickers making PowerPoint diagrams that drift from reality the moment they're published.

If you can't draw your architecture, code it, and deploy it - you're not an architect. You're a solutions consultant charging architect rates.

## The Rule of Three Deployments

### Deploy ONE: You're Learning

Your first VM deployment through the Azure Portal is **education**. You're discovering what variables matter:

- What region makes sense?
- What VM size handles the workload?
- Standard SSD or Premium?
- What subnet in what VNet?
- What tags does FinOps require?
- What naming convention are we using?
- What resource group structure makes sense?

**This takes 20-30 minutes of clicking through wizards, reading tooltips, and making decisions.**

This is fine. This is how you learn what Azure actually asks for. You're discovering the parameters that matter for your environment.

### Deploy THREE: You're Wasting Time

By the third manual deployment, you're doing this:

1. Navigate to Virtual Machines
2. Click Create
3. Select same subscription (why is this even a question?)
4. Type resource group name (same as last two times)
5. Type VM name (incrementing the number)
6. Select same region
7. Select same availability zone
8. Select same VM size
9. Click through networking (same VNet, different subnet)
10. Set same tags (copy/paste from last time)
11. Click Review + Create
12. Wait 8 minutes
13. **Realize you forgot to add one tag**
14. Go back and add it manually
15. Hope you remembered it on the first two VMs

**You just spent 60 minutes deploying three VMs that differ only by name and IP address.**

And here's the thing that kills me: **You're going to do this again next week.**

### The Breaking Point

If you're deploying your fourth VM manually through the portal, you've failed as an architect.

You're not "being thorough." You're not "understanding Azure better." You're burning billable hours on work a script could do in parallel while you get coffee.

**Manual deployments after the third one are technical debt you're creating in real-time.**

## Code Deploys Faster (And You Know It)

Let's do the math on deploying three VMs:

**Manual through portal:**
- VM 1: 20 minutes (learning the options)
- VM 2: 18 minutes (muscle memory kicking in)
- VM 3: 22 minutes (forgot a setting, went back)
- **Total: 60 minutes, serial deployment**
- **Consistency: Three VMs with small differences you won't find for 6 months**

**Code with Terraform:**
- Write main.tf: 15 minutes (capturing those variables you just learned)
- `terraform plan`: 2 minutes (catch mistakes before deployment)
- `terraform apply`: 8 minutes (deploys all three in parallel)
- **Total: 25 minutes for first run**
- **Subsequent deployments: 10 minutes**
- **Consistency: Identical VMs, enforced by code**

### But Here's the Real Killer

You need to deploy 10 more VMs next sprint for the dev environment.

**Manual:** 10 VMs × 20 minutes = 200 minutes (3.3 hours)  
**Code:** Change a count variable, `terraform apply` (10 minutes)

You need to rebuild the environment after a subscription migration.

**Manual:** Start clicking, hope your Visio diagram is current  
**Code:** `terraform apply` in the new subscription (15 minutes)

You need to prove compliance wants to know your VM configurations.

**Manual:** "Let me log into the portal and check..."  
**Code:** "Here's the git repo, line 47 shows disk encryption settings"

## Your Code IS Your Documentation

When you capture your architecture in Terraform, you're not doing "extra work." You're documenting decisions you already made.

**That Terraform file documents:**
- What variables matter (region, size, tags)
- What your naming convention is
- What your network topology looks like
- What security settings you chose
- What your disaster recovery approach is

**Your Visio diagram lies.** It was accurate the day you drew it. It drifted from reality the moment someone manually added a NIC through the portal.

**Your code can't lie.** It's either deployed or it isn't. It either matches production or your `terraform plan` shows the drift.

### Code as Recipe

Can you rebuild your environment from your code?

- Can you deploy to a new region for DR?
- Can you spin up a test environment that matches production?
- Can you prove to auditors what's actually deployed?
- Can you onboard a new architect without spending a week explaining how things work?

If the answer is no, you don't have architecture. You have **tribal knowledge and hope**.

## The Languages You'll Touch (And That's Fine)

"But I'm not a developer!"

Neither am I. But I write:

- **Terraform** - Infrastructure as Code
- **PowerShell** - Automation and Azure PowerShell cmdlets
- **Python** - Scripts and Azure SDK
- **JSON** - ARM templates, Policy definitions
- **KQL** - Resource Graph queries, Log Analytics
- **YAML** - Azure DevOps pipelines
- **Bash** - Because half your Azure VMs run Linux

**And I'm mediocre at ALL of them.**

You're not becoming a developer. You're becoming **good enough to:**
- Read existing code
- Modify it for your needs
- Debug when it breaks
- Google the syntax you forgot
- Ask ChatGPT to explain the part you don't understand

**That's the bar.** Not mastery. Competence.

## The Test

Here's how you know if you're actually an architect:

**Can you delete your entire environment and rebuild it from code in under an hour?**

If yes: You're an architect. Your code is your documentation. Your architecture is reproducible.

If no: You're a very expensive button-clicker with nice diagrams that will be wrong by next quarter.

## What This Means for Your Career

**Junior architects** who can code their infrastructure are more valuable than senior architects who can't.

**Speed matters.** When your company is doing a subscription consolidation with 44 subscriptions and 21 AD domains (yes, that's a real project I'm working on), manual deployments are a non-starter.

**Consistency matters.** When FinOps wants to know why 200 VMs don't have the Environment tag, "we deployed them manually" is not an acceptable answer.

**Documentation matters.** When your VP asks "how do we failover to our DR region," pointing at Terraform code that deploys to either region is an answer. Pointing at a Visio diagram from 2023 is not.

## The Harsh Reality

If you've been an Azure architect for more than a year and you still can't deploy infrastructure with code, you're not growing. You're stagnating.

**You're being out-competed by:**
- Junior admins learning Terraform on YouTube
- Platform engineering teams that ship code
- Cloud-native companies that never click through portals
- AI assistants that can write Terraform better than you can click

**You're becoming obsolete.** Not because you're not smart. Because you're refusing to learn the tools that make architecture scalable.

## Start Tomorrow

You don't need to be an expert. You need to start.

**Tomorrow morning:**

1. Deploy ONE resource manually (learn the variables)
2. Write Terraform that captures those variables
3. Deploy that same resource with code
4. Delete both
5. Deploy it again with code (faster this time)

**That's it.** You're now an architect who codes.

**Next week:**

1. Deploy three resources
2. See the pattern
3. Parameterize it
4. Push to git
5. You now have documented, reproducible architecture

**Next month:**

1. Rebuild a full environment from code
2. Someone asks "how is this configured?"
3. You send them a link to the git repo
4. You're now the architect everyone wants on their project

## The Bottom Line

**Manual deployment ONE time** = Learning the variables  
**Manual deployment THREE times** = Recognizing the pattern  
**Manual deployment FOUR times** = Architectural malpractice

If you can't code your Azure architecture, you're not an architect.

You're just slow, inconsistent, and undocumented.

---

*Want to see this in action? Check out the [Azure IPAM Tool](https://github.com/dswann5/azure-ipam) - 1,000+ private endpoints managed in code, not spreadsheets.*

*Working on a 44-subscription consolidation? You NEED code. Read about [IP Address Management for Cloud Mergers](/blog/azure-ipam-tool).*
