# Azure Rationalization Toolkit - GitHub Repo Plan

## Repository Details
**Name:** `azure-rationalization-toolkit`  
**Description:** Production-ready tools for software rationalization in multi-subscription Azure environments. AppID-first governance.  
**License:** MIT  
**Topics:** `azure`, `finops`, `devops`, `governance`, `cost-optimization`, `tagging`

---

## Repository Structure

```
azure-rationalization-toolkit/
├── README.md                          # Main documentation
├── LICENSE                            # MIT License
├── .gitignore                         # Standard Azure/PowerShell ignores
│
├── policies/                          # Azure Policy Definitions
│   ├── README.md
│   ├── require-appid-tag.json        # Deny resources without AppID
│   ├── require-costcenter-tag.json   # Deny resources without CostCenter
│   ├── require-owner-tag.json        # Deny resources without Owner
│   ├── deny-untagged-resources.json  # Master policy
│   ├── sunset-date-enforcement.json  # Require sunset date for IaaS
│   └── deploy-policies.ps1           # Deploy all policies at once
│
├── kql/                               # KQL Queries for Resource Graph
│   ├── README.md
│   ├── untagged-resources.kql        # Find resources missing tags
│   ├── cost-by-appid.kql             # Roll up costs by AppID
│   ├── orphaned-resources.kql        # Find abandoned resources
│   ├── sunset-audit.kql              # Check sunset dates
│   ├── security-zone-audit.kql       # Validate zone compliance
│   └── cross-subscription-apps.kql   # Map apps across subs
│
├── automation/                        # PowerShell Automation Scripts
│   ├── README.md
│   ├── auto-tag-resources.ps1        # Bulk tag existing resources
│   ├── retire-by-appid.ps1           # Delete app across all subs
│   ├── cost-rollup-report.ps1        # Generate AppID cost report
│   ├── orphan-cleanup.ps1            # Find and delete orphans
│   └── sunset-enforcement.ps1        # Alert on expired sunset dates
│
├── bicep/                             # Bicep Templates
│   ├── README.md
│   ├── tagging-module.bicep          # Reusable tagging module
│   └── resource-group-template.bicep # RG with proper naming
│
├── github-actions/                    # CI/CD Workflows
│   ├── README.md
│   ├── tag-enforcement.yml           # Validate tags in PR
│   ├── cost-report.yml               # Weekly cost report
│   └── retire-app.yml                # Automated retirement workflow
│
├── powerbi/                           # Power BI Templates
│   ├── README.md
│   ├── appid-cost-dashboard.pbix     # Main cost dashboard
│   └── setup-guide.md                # How to connect to Azure
│
├── docs/                              # Documentation
│   ├── getting-started.md
│   ├── appid-design-guide.md
│   ├── tagging-standard.md
│   └── 7-rs-framework.md
│
└── examples/                          # Real-world examples
    ├── README.md
    ├── tagging-standard.yaml          # Example org tagging standard
    └── app-inventory-template.xlsx    # Starter spreadsheet
```

---

## README.md Content (Draft)

```markdown
# Azure Rationalization Toolkit

> **AppID-first governance for multi-subscription Azure environments.**

Before you migrate, modernize, or look at the cloud — you must know what you own, what it costs, and whether it should exist.

This toolkit provides **production-ready** policies, queries, and automation to implement software rationalization at scale.

## 🎯 What This Solves

**The Problem:**
- "How many apps do we have?" → Nobody knows
- Cloud bill split across 47 subscriptions → No app-level cost visibility
- Dev/Test/Prod in separate subs → Can't retire "the app"

**The Solution:**
- **AppID tags** on every resource (enforced by policy)
- **KQL queries** to roll up costs across subscriptions
- **Automation** to retire, replatform, or audit

## 🚀 Quick Start

### 1. Deploy Policies (5 minutes)
```powershell
./policies/deploy-policies.ps1 -SubscriptionId "your-sub-id"
```

### 2. Run Discovery (2 minutes)
```kql
# Copy from: kql/untagged-resources.kql
# Paste into: Azure Resource Graph Explorer
```

### 3. Generate Cost Report (5 minutes)
```powershell
./automation/cost-rollup-report.ps1 -OutputPath ./report.csv
```

## 📚 Documentation

- [Getting Started Guide](docs/getting-started.md)
- [AppID Design Guide](docs/appid-design-guide.md)
- [Tagging Standard](docs/tagging-standard.md)
- [7 R's Framework](docs/7-rs-framework.md)

## 🛠️ What's Inside

| Category | Contents |
|----------|----------|
| **Policies** | Ready-to-deploy Azure Policy definitions |
| **KQL** | Resource Graph queries for discovery & audit |
| **Automation** | PowerShell scripts for tagging, retirement, reporting |
| **Power BI** | Cost dashboard template (AppID roll-up) |
| **GitHub Actions** | CI/CD workflows for enforcement |

## 💡 Key Concepts

### The AppID: Your Atomic Unit of Truth

```yaml
AppID: ERP-001              # Unique identifier
Environment: Prod           # Dev, Test, Prod
CostCenter: FIN-1001       # Finance dept
Owner: erp-team@org.com    # Who owns this
SecurityZone: PCI          # Compliance zone
WorkloadTier: Critical     # SLA tier
SunsetDate: 2027-12-31     # Retirement date (if applicable)
```

### The DevOps Reality

**One app = Multiple subscriptions:**
- `sub-dev-finance` (Dev environment)
- `sub-test-finance` (Test environment)
- `sub-prod-pci` (Prod - PCI compliance zone)

**AppID bridges them all.**

## 📖 Related Resources

- [Blog Post: Software Rationalization - Step Zero](https://azure-noob.com/blog/software-rationalization-step-zero-devops/)
- [Microsoft: Azure Tagging Best Practices](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging)
- [FinOps Foundation: Cloud Cost Optimization](https://www.finops.org/)

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📄 License

MIT License - see [LICENSE](LICENSE)

## ⭐ If This Helped You

- Star this repo
- Share on LinkedIn
- Tell your cloud architect friends

---

**Built by:** [David Swann](https://azure-noob.com)  
**Blog:** [Azure Noob](https://azure-noob.com)
```

---

## Files to Create Tomorrow

### Priority 1: Core Policies (30 min)
- `require-appid-tag.json`
- `require-costcenter-tag.json`
- `deny-untagged-resources.json`
- `deploy-policies.ps1`

### Priority 2: KQL Queries (20 min)
- `untagged-resources.kql`
- `cost-by-appid.kql`
- `orphaned-resources.kql`
- `sunset-audit.kql`

### Priority 3: Automation (45 min)
- `auto-tag-resources.ps1`
- `retire-by-appid.ps1`
- `cost-rollup-report.ps1`

### Priority 4: Documentation (30 min)
- `README.md` (from draft above)
- `docs/getting-started.md`
- `docs/tagging-standard.md`

**Total Time: ~2.5 hours**

---

## Launch Checklist

- [ ] Create GitHub repo: `azure-rationalization-toolkit`
- [ ] Add all files from structure above
- [ ] Write comprehensive README
- [ ] Add LICENSE (MIT)
- [ ] Create releases/v1.0.0
- [ ] Link from blog post
- [ ] Share on LinkedIn (if allowed)
- [ ] Submit to awesome-azure lists

---

## Metrics to Track

**Week 1:**
- Stars
- Forks
- Downloads (if packaged)

**Month 1:**
- Issues opened
- PRs submitted
- Blog post traffic → repo clicks

**Goal:** 100+ stars in first month
