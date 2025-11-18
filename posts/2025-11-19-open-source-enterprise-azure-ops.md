---
title: "Why I Open-Sourced My Enterprise Azure Operations Repository"
date: 2025-11-19
summary: "Microsoft tells you how to create Azure resources. I'm documenting how to actually operate them at enterprise scale. Here's why I'm sharing operational knowledge that most architects keep private, and how AI helped me build portable intellectual property."
tags: ["Azure", "Career", "GitHub", "FinOps", "AI"]
cover: "/static/images/hero/open-source-ops.png"
---

# Why I Open-Sourced My Enterprise Azure Operations Repository

**This is a follow-up to [The AI Admin: Stop Being a Human API Wrapper](/blog/the-ai-admin/)**

Yesterday I wrote about how AI is eliminating operational toil in Azure administration - the shift from manual execution to AI-assisted automation. Today I'm sharing what I built *using* that AI-assisted workflow: an open-source repository of enterprise Azure operational patterns.

I just published [azure-enterprise-ops](https://github.com/dswann101164/azure-enterprise-ops) on GitHub. It contains the operational templates, KQL queries, Terraform patterns, and MCP server configurations I use to manage 44 Azure subscriptions with 31,000+ resources during a major bank merger.

**This isn't a portfolio project. This is production code.**

Most Azure architects guard this stuff like trade secrets. I'm publishing it because I have a thesis: *operational knowledge compounds faster when it's shared than when it's hoarded.*

And here's the meta-lesson: **AI accelerated this transformation from private notes to public repository by 5x.** What would have taken 200+ hours of manual work took 40 hours with AI assistance.

This post documents both *what* I'm sharing and *how* AI helped me build portable intellectual property.

## The Documentation Gap Nobody Talks About

Microsoft's Azure documentation is excellent at showing you how to create resources. Here's how to deploy a VM. Here's how to configure a VNet. Here's how to set up Key Vault.

**What it doesn't show you:**

- Which subscription goes in which management group when you have 44 of them?
- How do you allocate costs when applications span multiple subscriptions?
- What's your NSG rule strategy across an entire enterprise?
- How do you migrate 21 Active Directory domains during a merger?
- How do you actually implement FinOps at scale?

Cloud Adoption Framework? Great theory. Doesn't tell you how to handle the political reality of cost allocation when Finance wants chargebacks but application teams don't tag resources.

MVPs blog about new features. They don't blog about "here's how we finally got everyone to tag their resources after 18 months of fighting."

Certification courses teach you concepts. They don't teach you "here's the KQL query you'll run 50 times a week for the next three years."

**That gap? That's where actual value lives.**

## What I'm Sharing (And Why)

The [azure-enterprise-ops](https://github.com/dswann101164/azure-enterprise-ops) repository contains:

### Documentation (`/docs`)
- **Architecture Patterns**: Hub-spoke networking at scale, governance structures, migration strategies
- **Security Operations**: Real NSG rules (not "allow all from 10.0.0.0/8"), Key Vault patterns, Azure AD integration
- **Troubleshooting Guide**: Common production issues with actual fixes
- **MCP Servers**: AI-assisted Azure administration workflows (the infrastructure from [The AI Admin](/blog/the-ai-admin/))

### Examples (`/examples`)
- **Automation Scenarios**: End-to-end PowerShell and Terraform patterns
- **Cost Analysis**: KQL queries for FinOps, cost allocation strategies, budget automation
- **Resource Queries**: Azure Resource Graph queries for inventory, compliance, and analysis

### Terraform (`/terraform`)
- Production-ready infrastructure code
- Modular design patterns
- Variables and outputs for reuse
- Key Vault integration

### MCP Integration (`/mcp`)
- Model Context Protocol server configs
- AI-powered Azure operations workflows
- The actual configuration I use for AI-assisted administration

## The "Portable IP" Strategy

Here's my career thesis: **I can't take proprietary code with me when I leave a job, but I can take patterns and knowledge.**

Every time I solve a problem at work, I ask: "Can I generalize this?"

- Specific to my company? Stays private.
- Generic operational pattern? Gets documented and published.

This repository is the result of that practice. I've sanitized every reference to:
- Company names
- Specific resource counts
- Internal tooling
- Proprietary configurations

What remains is pure operational knowledge: *how you actually run Azure at enterprise scale*.

**Why this matters for you:**

If you're managing Azure in a regulated industry, you're probably solving similar problems to me. Financial services, healthcare, government - we all deal with:
- Multi-subscription governance
- Complex cost allocation
- Merger and acquisition scenarios
- Hybrid cloud integration
- Compliance requirements

Publishing this means:
1. You get working solutions to common problems
2. I get feedback and contributions
3. We both get professional visibility for knowing this stuff
4. The knowledge compounds as others add their patterns

## How AI Accelerated This (The Meta-Lesson)

Building this repository took about 40 hours of work. Without AI, it would have taken 200+.

**This is the AI Admin strategy in practice:** I used the same AI tooling I wrote about in [yesterday's post](/blog/the-ai-admin/) to accelerate my own content creation workflow.

**Here's my actual workflow:**

### Phase 1: Content Generation (AI-Assisted)
I gave Claude Desktop access to my internal documentation and said "help me turn this into publishable content."

It:
- Extracted patterns from company-specific examples
- Converted internal wikis to markdown
- Reorganized content for external audiences
- Suggested structure and navigation

**Human time: ~8 hours of review and direction**  
**AI time: Instant transformations that would've been 50+ hours of manual work**

### Phase 2: Sanitization (AI-Powered)
I built PowerShell scripts with AI to:
- Find and replace company-specific terms
- Convert real resource names to generic examples
- Strip internal identifiers
- Verify no sensitive data remained

**Human time: ~2 hours writing sanitization requirements**  
**AI time: Generated scripts that would've taken 20 hours to write manually**

### Phase 3: Documentation (AI-Enhanced)
Claude helped me:
- Write comprehensive READMEs
- Create contribution guidelines
- Add inline code comments
- Generate setup instructions

**Human time: ~5 hours of review and editing**  
**AI time: Draft generation that saved 30+ hours**

### Phase 4: Repository Structure (AI-Designed)
I described my goals and constraints. Claude suggested:
- Folder organization
- File naming conventions
- README structure
- .gitignore patterns

**Human time: ~2 hours of implementation**  
**AI time: Architecture design that would've taken 10+ hours of research**

**Total: 40 hours of human work instead of 200+**

The AI didn't write the operational knowledge - I built that over three years. But it accelerated the transformation from "private notes" to "publishable repository" by 5x.

**This is what I meant by "AI Admin"** - not letting AI replace you, but using AI to eliminate toil so you can focus on higher-value work. In this case, the higher-value work was deciding *what* to share and *how* to position it. AI handled the execution layer.

## The "Applications, Not Subscriptions" Insight

Here's the single most valuable pattern in this repository:

**Microsoft's cost management is built around subscriptions. But applications are your real organizational unit.**

When you have 44 subscriptions, you don't care about "Subscription XYZ spent $50K this month." You care about "The Customer Portal application spent $50K across three subscriptions."

Cloud Adoption Framework doesn't cover this. Certification courses don't teach it. Vendor consultants won't tell you (because it makes their billing complicated).

**But it's the fundamental reality of enterprise cost management.**

The repository includes:
- KQL queries to aggregate costs by application
- Tagging strategies for cross-subscription applications
- PowerShell automation for cost allocation
- Terraform patterns for application-centric resource organization

This one pattern has saved our organization hundreds of hours of manual cost allocation work.

## Why Most People Don't Share This

**"If I share my expertise, I lose my competitive advantage."**

I hear this constantly. Here's why it's wrong:

### 1. Knowledge Compounds, It Doesn't Deplete
Publishing this doesn't make me know less. It makes the community know more. And when the community knows more, I benefit from their contributions and improvements.

### 2. Execution Matters More Than Knowledge
Knowing *how* to implement FinOps at scale is different from *actually doing it* under political pressure, budget constraints, and legacy technical debt.

Publishing the "how" doesn't eliminate the value of the "doing it."

### 3. Shared Context Creates Opportunities
When someone sees this repository and thinks "this person actually understands enterprise Azure operations," that's a professional connection I wouldn't have had otherwise.

Can't use LinkedIn due to company policy. This repository is my professional visibility.

### 4. Real Expertise Can't Be Copied
The patterns in this repository represent three years of production experience. You can read them in an hour. Understanding when to apply them, how to adapt them, and what trade-offs matter - that takes experience.

Publishing the patterns doesn't make me replaceable. It proves I've done the work.

## What This Means for You

### If You're Managing Azure at Scale
Clone the repository. Use the KQL queries. Adapt the Terraform patterns. Submit pull requests with your own improvements.

Enterprise Azure operations is a small community. We're all solving similar problems. Sharing solutions benefits everyone.

### If You're Building Your Career
This is a template for building portable intellectual property:

1. **Document everything you learn** (even if it's just notes to yourself)
2. **Extract the patterns** (what's specific vs. what's general?)
3. **Publish the general knowledge** (GitHub, blog posts, speaking)
4. **Maintain separation** (company IP stays private)
5. **Build in public** (let AI accelerate the transformation)

Your expertise is valuable. Make it visible.

### If You're Learning Azure
Start with the `/examples` folder. Those are working solutions to common problems.

Don't just read them. Run them. Modify them. Break them. Understand why they work.

The best way to learn Azure isn't certification courses. It's reading production code and operational documentation from people who actually run this stuff.

## The Repository Structure

Here's what you'll find:

```
azure-enterprise-ops/
├── docs/                    # Operational patterns and guides
│   ├── architecture.md      # Hub-spoke, governance, migrations
│   ├── security.md          # NSG rules, Key Vault, Azure AD
│   ├── troubleshooting.md   # Common issues with fixes
│   └── mcp-servers.md       # AI-assisted administration
├── examples/                # Working code, not POCs
│   ├── automation-scenarios.md
│   ├── cost-analysis.md     # FinOps queries and strategies
│   └── query-resources.md   # Resource Graph KQL
├── terraform/               # Production-ready infrastructure
│   ├── main.tf
│   ├── key-vault.tf
│   └── variables.tf
└── mcp/                     # AI operations integration
    ├── README.md
    └── servers.json
```

Everything includes:
- Working code (not pseudocode)
- Inline comments explaining *why*, not just *what*
- Before/after examples
- Lessons learned

## Contributing

The repository includes `CONTRIBUTING.md` with guidelines for:
- Suggesting KQL queries
- Submitting operational patterns
- Reporting issues
- Code review process

**I want contributions.** If you're managing Azure at scale and have patterns that work, share them.

The community benefits when we share operational reality instead of hoarding expertise.

## What's Next

This is version 1.0 of the repository. Here's what I'm planning:

### Short Term (Next Month)
- Azure Monitor Workbooks for cost visualization
- Additional KQL query library
- Terraform modules for common patterns
- More MCP integration examples

### Medium Term (Q1 2026)
- Video walkthroughs of complex scenarios
- FinOps automation toolkit
- Guest contributions from other architects

### Long Term (2026)
- Potentially building a SaaS product around these patterns
- Speaking at Azure/FinOps conferences
- Creating a comprehensive course for enterprise Azure operations

## The AI-Assisted Future

As I wrote in [The AI Admin](/blog/the-ai-admin/), traditional Azure administration is becoming AI-assisted automation. That's not a threat - it's an opportunity.

When AI can handle 75-90% of routine Azure administration tasks, the value shifts from *execution* to:
- **Pattern recognition**: Knowing which approach fits which scenario
- **Architectural decisions**: Understanding trade-offs at scale
- **Process design**: Automating workflows end-to-end
- **Knowledge sharing**: Teaching AI (and humans) better patterns

This repository is my contribution to that shift. Instead of hoarding operational knowledge, I'm sharing it so:
- You can train AI agents with better patterns
- Junior engineers can learn from production examples
- The Azure community has real operational documentation
- We all benefit from shared expertise

## Get Started

**Repository**: [github.com/dswann101164/azure-enterprise-ops](https://github.com/dswann101164/azure-enterprise-ops)

1. Browse the `/docs` for patterns
2. Check `/examples` for working code
3. Review `SETUP.md` for detailed configuration
4. Submit issues or pull requests

**Questions?** Open a GitHub issue or comment below.

**Want more content like this?** This blog covers real-world Azure operational challenges that vendor documentation doesn't. No basic tutorials. No certification prep. Just the stuff that actually matters when you're managing Azure at scale.

---

## Key Takeaways

1. **The gap between "tutorial complete" and "production at 3 AM"** is where real value lives
2. **Applications, not subscriptions** are your organizational unit for cost management
3. **Operational knowledge compounds** when shared, not when hoarded
4. **AI accelerates** the transformation from private notes to publishable content (5x faster)
5. **Portable intellectual property** is the career strategy for 2025+
6. **Real expertise** is proven through execution, not protected by secrecy
7. **AI Admin strategy in practice**: Use AI to eliminate toil, focus on strategy

**Star the repo** if you find it useful. The GitHub algorithm rewards engagement, and that helps others discover operational content.

**Share your own patterns** via pull requests. We all benefit when we share what actually works.

---

*Managing enterprise Azure infrastructure while documenting what vendor consultants won't tell you. Not on LinkedIn - connect via blog comments or GitHub issues.*
