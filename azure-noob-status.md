# Azure Noob Blog - Weekly Status

**Date:** October 27, 2025  
**Blog Age:** 12 weeks (launched September 7, 2025)  
**Publishing Pace:** 3+ posts/week consistently maintained  
**Total Posts:** 32 published

---

## Current State

### What's Working
- **Velocity:** Shipping 3+ posts/week consistently, exceeding original 2/week target
- **Content Quality:** Real operational problems from Synovus work with full working code
- **Major Series Completed:** Three-part audit compliance series addressing critical SOC 2 gap
  - Problem statement: "The Azure Audit Gap Nobody Talks About"
  - Part 1: Azure Activity Log compliance (8,000+ words, complete setup guide)
  - Part 2: Azure AD audit logs (8,000+ words, comprehensive guide)
  - Pattern: "Grill assembly manual" format - every click, field, verification step documented
- **Proven Formula:** Multiple successful patterns:
  - Attribution to original creators (Billy York workbooks example)
  - Before/after technical comparisons
  - Full code examples with explanations (15+ scripts per post)
  - GitHub repos with working implementations
  - Honest documentation of lessons learned
- **Lead Generation:** 
  - Email capture live on KQL Cheat Sheet post (high-value evergreen content)
  - 2 subscribers with 8.7% conversion rate (strong signal)
  - Early organic growth: 5 clicks from Google Search Console in 28 days
- **Analytics Deployed:** Site now has tracking infrastructure in place
- **Content Pipeline:** Original 8-post pipeline completed, now drawing from ongoing work experience

### Content Strategy (Validated)
Primary driver: Document real work experience at Synovus while solving problems
- Not chasing traffic targets or monetization timelines
- Building portable intellectual property
- Long-term interest in remote consulting and potential SaaS products
- Organic growth approach - blog climbs when it climbs

---

## Content Inventory

### Published (32 Posts)

**Audit & Compliance Series (3)**
1. The Azure Audit Gap Nobody Talks About - Why 90-day logs won't survive 7-year audit
2. Azure SOC 2 Activity Log Compliance - Complete step-by-step setup guide (Part 1)
3. Azure AD Audit Logs for SOC 2 - Comprehensive implementation guide (Part 2)

**FinOps & Cost Management (5)**
1. Azure Cost Reporting for Boardroom - Turning receipts into stories
2. Azure Cost Management is Confusing - Taming Azure billing
3. Cost Reports Don't Match Business Reality - Shared infrastructure problem
4. Azure Resource Tags Guide - Order, capitalization, spelling
5. IT Roles & Responsibilities Matrix - CAF-aligned RACI

**KQL & Data Queries (6+)**
1. Azure VM Inventory with KQL - Complete Resource Graph query
2. KQL Cheat Sheet - Complete guide with email capture
3. The KQL Problem Nobody Warns You About - One language across five different systems
4. Azure Update Manager Reality Check - 77% of VMs unsupported
5. [Additional KQL posts from the 32 total]

**Technical/Operations (10+)**
1. Azure VM Automation Dependency Hell - Chocolatey vs winget
2. Why Most Azure Migrations Fail - Institutional knowledge problem
3. Modernizing Azure Workbooks - Enhanced Billy York's workbook (50→200+ services)
4. The 3 Hour Rule - When to stop debugging and open Microsoft support ticket
5. Microsoft Docs vs Reality - Documentation gaps in enterprise scenarios
6. Chris Bowman Dashboard - Workbook repair and enhancement
7. [Additional operational posts including migration experience]

**Career & Strategy (2+)**
1. Certification Strategy - Not renewing Azure certs, investing in AI-102 instead
2. AI Tool Usage Analysis - 30-day production testing data
3. [Additional career positioning content]

*Note: 32 posts published over 12 weeks. Complete inventory available at azure-noob.com/blog*

---

## Active Content Topics

### Migration Experience Posts (Ready to Write)
From 44 subscriptions + 21 AD domains consolidation project:

1. **IP Address Management for Azure Subscription Consolidation**
   - What nobody tells you about cloud mergers
   - Can't clone NICs, private endpoints consume unpredictable IP space
   - No IP reservation for firewall rules
   
2. **Enterprise Azure Migration Reality**
   - What 21 AD domains and dual ExpressRoute taught me
   - DNS split-brain challenges
   - "Just click the button" isn't real - dual environments for 12-18 months
   
3. **Leadership Wants Cloud Migration ROI**
   - Why that's the wrong question
   - ROI calculation misses soft costs (no VAR meetings, no hardware refresh, faster provisioning, better stability)
   
4. **Azure Resource Graph Is Your Cloud CMDB**
   - Why leadership doesn't know it yet
   - Self-maintaining CMDB that actually works
   
5. **Your CMDB Is Wrong**
   - How cloud migration fixes it
   - First accurate inventory in years

### Emerging Topics from Current Work
- Tag governance at 31k resource scale
- Private endpoint DNS patterns
- Cost allocation for shared infrastructure
- Azure policy enforcement in enterprise
- Cross-subscription architecture patterns

---

## Current Projects & Blockers

### Active Work
- **Tag Repair:** Circular dependency problem
  - Need clean tags to justify FinOps Toolkit budget
  - Need FinOps Toolkit to fix tags at 31k resource scale
  - Resolution approach TBD (manual high-value resources first? budget approval without perfect data?)

### Technical Stack Status
- **Deployment:** Flask + Frozen-Flask → GitHub Pages working smoothly
- **Email Capture:** Kit (formerly ConvertKit) active on KQL Cheat Sheet
- **Analytics:** Deployed and tracking
- **Publishing Workflow:** Established and consistent
- **Local Testing:** `flask run` → `python freeze.py` → commit → push

---

## Metrics (Current Snapshot)

### Primary Metrics
- **Publishing Consistency:** 3+ posts/week (12 weeks, 32 posts = 2.67/week average, trending up)
- **Email Signups:** 2 subscribers, 8.7% conversion rate on KQL Cheat Sheet
- **Organic Search:** 5 clicks from Google Search Console in first 28 days

### What to Watch
- Email conversion rate trends (currently strong at 8.7%)
- Most popular posts (need more analytics time)
- Traffic sources (when sufficient data available)
- Time on page (content quality indicator)

---

## Writing Patterns That Work

### Content Structure (From Audit Series)
1. **Problem Statement** - What's broken, why it matters, who it affects
2. **Technical Deep-Dive** - Complete working solutions, not fragments
3. **Step-by-Step Implementation** - "Grill assembly manual" format
4. **Code Examples** - 15+ working scripts/queries per post
5. **Cost Breakdowns** - Real numbers for different environment sizes
6. **Troubleshooting** - Common mistakes and how to fix them
7. **Verification Steps** - How to know it's working
8. **Lessons Learned** - What didn't work, what would be done differently

### Writing Style
- Direct, no fluff or filler
- Assume reader is smart but new to topic
- Lead with problem, not theory
- Code-heavy with clear explanations
- Honest about failures and debugging process
- Proper attribution to sources
- Full working code examples (never fragments or placeholders)
- Every button click documented when teaching implementation

---

## Synovus Context (Relevant to Content)

### Work Environment
- **Role:** Azure Architect at regional bank
- **Remote worker:** All work done remotely
- **Lab environment:** Full Azure tenant separate from production (can break things, iterate fast)
- **Access:** Windows Virtual Desktop (WVD)
- **Constraint:** Cannot use LinkedIn due to company policy (blog is primary platform)

### Job Security
- Synovus merging with Pinnacle Financial Q1 2026
- Job secure - one of only 2 cloud experts
- Position strengthens through merger

### Active Migration Project
- **Scale:** 44 subscriptions, 21 AD domains, 300+ applications, 31k+ resources
- **Infrastructure:** Dual ExpressRoute circuits, VMware bridge to on-premises
- **Timeline:** Q1 2026 merger
- **Tools Built:** IPAM tool (GitHub repo), migration checklist (Excel), Resource Graph queries

---

## Session Notes (Oct 27, 2025)

### Recent Achievements (Oct 26)
- Completed three-part audit compliance series
- Deployed analytics to site
- Confirmed email capture working with strong conversion rate
- Exceeded original publishing velocity target (3+ vs 2/week)

### Key Insights
- "Grill assembly manual" format resonates - people want exact steps
- Audit/compliance content fills real gap in Azure documentation
- 8.7% email conversion rate suggests content quality hitting target
- Original content pipeline (8 posts) now complete, pivoting to ongoing work topics
- Blog momentum strong at 12 weeks

### Current Status
- 32 posts in 12 weeks
- Analytics deployed
- Email capture working
- Organic search starting to show
- No immediate content blockers

---

**Document Version:** 2.0  
**Created:** October 5, 2025  
**Updated:** October 27, 2025  
**Next Update:** After significant milestone or monthly review

---

## Quick Reference for Claude

When starting new sessions:
1. This document captures current blog status as of Oct 27, 2025
2. 32 posts published over 12 weeks (3+ posts/week velocity)
3. Content strategy validated: document real work at Synovus
4. Major audit compliance series completed (3-part)
5. Analytics deployed, email capture working (8.7% conversion)
6. No pressure on monetization timeline - organic growth approach
7. LinkedIn unavailable - blog is primary platform
8. Original 8-post pipeline complete, now drawing from ongoing enterprise work
