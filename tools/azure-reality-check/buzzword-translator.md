# Buzzword Translator

**Stop pretending. Start communicating.**

This guide translates common business buzzwords and technical jargon into what they actually mean - and what questions you should ask to force clarity.

---

## Business Buzzwords → Technical Reality

### "Digital Transformation"

**What they probably mean:**
- Move some apps to the cloud
- Modernize our website
- Use more SaaS products

**Questions to ask:**
- Which specific applications or processes are we transforming?
- What does "transformed" look like? Can you show me an example?
- What's changing for end users? For IT operations?
- What's the timeline and budget?

**Red flags:**
- No specific applications mentioned
- "Transform everything" with no prioritization
- 6-month timeline for complete transformation
- No discussion of organizational change

---

### "Cloud-Native Architecture"

**What they probably mean:**
- Rewrite apps to use Azure services
- OR just lift-and-shift to cloud
- OR use containers/Kubernetes

**Questions to ask:**
- Are we rewriting applications or migrating existing ones?
- Which Azure services specifically?
- Do we have the skills to support this architecture?
- What happens to our existing apps?

**Red flags:**
- Assumes all apps can be rewritten
- No discussion of legacy dependencies
- Ignores regulatory requirements
- "It's more scalable" without defining scale needs

---

### "Implement DevOps"

**What they probably mean:**
- Speed up deployments
- Reduce deployment failures
- Cultural change (but they don't know what that means)

**Questions to ask:**
- Which team and which application first?
- What does success look like? Faster? More reliable? Both?
- What needs to change organizationally?
- Who owns the pipeline? Developers? Operations?

**Red flags:**
- Buying tools before defining process
- "Cultural transformation" with no change management
- Expected results in 30 days
- No discussion of who's on-call

---

### "We're Adopting FinOps"

**What they probably mean:**
- CFO wants to understand cloud costs
- Need to show department spend
- Hope to reduce costs somehow

**Questions to ask:**
- How do you want costs broken down? By department? Application? Cost center?
- Do we have the tagging in place to support this?
- Who will own cost optimization decisions?
- Is this about visibility, accountability, or reduction?

**Red flags:**
- Expects immediate 30% cost reduction
- Doesn't understand tagging requirements
- Assumes tools solve cultural problems
- No discussion of who makes trade-off decisions

---

### "Follow Microsoft Best Practices"

**What they probably mean:**
- Implement something from Cloud Adoption Framework
- Make our Azure "more professional"
- Satisfy auditors

**Questions to ask:**
- Which specific best practices? CAF? Well-Architected Framework?
- Are we implementing for new resources or retrofitting existing?
- What's the business value versus effort required?
- What assumptions in the docs don't match our environment?

**Red flags:**
- Assumes greenfield deployment
- Doesn't account for legacy constraints
- Expected compliance overnight
- No discussion of migration effort

---

### "Multi-Cloud Strategy"

**What they really mean:**
- We acquired a company using AWS
- OR consultant convinced us to avoid vendor lock-in
- OR we want negotiating leverage with Microsoft

**Questions to ask:**
- What specific workloads need to be portable?
- Do we have expertise in multiple clouds?
- What's the cost of maintaining multi-cloud capability?
- Are we truly architecting for portability or just supporting both?

**Red flags:**
- "Cloud-agnostic" with no workload examples
- No discussion of operational complexity
- Assumes portability is free
- No realistic plan for maintaining expertise

---

### "Landing Zones"

**What they probably mean:**
- Structured subscription architecture
- Security baselines for new workloads
- Microsoft CAF implementation

**Questions to ask:**
- Is this for new workloads or existing subscriptions?
- Do we have capacity to deploy 400-resource template?
- How does this interact with our existing resources?
- What's the rollback plan if this conflicts with production?

**Red flags:**
- Deploying to production without testing
- Assuming zero conflicts with existing resources
- No discussion of existing subscription architecture
- Expected immediate compliance

---

### "Governance Framework"

**What they probably mean:**
- Azure Policy implementation
- Tagging standards
- Cost control
- Security baselines

**Questions to ask:**
- What specific behaviors are we trying to prevent or enforce?
- Are we governing new resources or remediating existing?
- Who approves exceptions?
- How do we measure success?

**Red flags:**
- "Complete governance" with no specifics
- No discussion of exception process
- Assuming 100% compliance
- No plan for handling legacy resources

---

### "We Need Visibility"

**What they probably mean:**
- Can't see what's deployed
- Don't know who owns what
- Can't track costs
- Lost control

**Questions to ask:**
- Visibility into what specifically? Resources? Costs? Security?
- What decisions would better visibility enable?
- What's the deliverable? Dashboard? Report? Alert system?
- Who's the audience?

**Red flags:**
- Building dashboards nobody will use
- No clear decision enabled by visibility
- "Everything" without prioritization
- No discussion of data quality issues

---

## Technical Jargon → Plain Business Language

### "Leverage Azure Policy for compliance"

**What we actually mean:**
- Write rules to block bad deployments
- OR enforce tagging standards
- OR remediate non-compliant resources

**Say this instead:**
- "Set up automated rules to prevent resources from being created without required tags"
- "Block deployment of resources that don't meet security standards"
- "Automatically fix resources that violate policies"

---

### "Implement Infrastructure as Code"

**What we actually mean:**
- Script our deployments with Terraform/Bicep
- Make infrastructure repeatable
- Version control our infrastructure

**Say this instead:**
- "Script our deployments so they're repeatable and documented"
- "Put our infrastructure in version control like we do with code"
- "Make disaster recovery possible by having infrastructure as code"

---

### "Query Resource Graph for inventory"

**What we actually mean:**
- Run KQL queries to list resources
- Extract metadata from Azure
- Generate reports on what's deployed

**Say this instead:**
- "Generate automated list of everything deployed in Azure"
- "Create inventory report showing all VMs, storage accounts, etc."
- "Pull resource information for compliance reporting"

---

### "Deploy landing zone architecture"

**What we actually mean:**
- Create subscription template with security baselines
- Structure subscriptions following CAF
- Implement hub-and-spoke networking

**Say this instead:**
- "Create subscription template with built-in security for new projects"
- "Set up structured environment for new workloads"
- "Implement network architecture for secure connectivity"

---

### "Establish FinOps framework"

**What we actually mean:**
- Implement tagging for cost allocation
- Build cost reporting dashboards
- Create process for cost review

**Say this instead:**
- "Set up cost tracking so each department sees their Azure spending"
- "Implement tagging so we can allocate costs accurately"
- "Create monthly cost review process with department owners"

---

### "Remediate security findings"

**What we actually mean:**
- Fix issues flagged by security tools
- Apply security patches
- Reconfigure resources to meet policy

**Say this instead:**
- "Fix the security vulnerabilities identified in the scan"
- "Apply the missing security patches"
- "Reconfigure resources to meet security requirements"

---

### "Refactor to microservices"

**What we actually mean:**
- Break monolithic app into smaller pieces
- Deploy services independently
- Increase deployment complexity significantly

**Say this instead:**
- "Break the application into smaller, independent services"
- "Enable faster updates to specific features without redeploying everything"
- "Warning: This increases operational complexity and requires new skills"

---

### "Implement observability"

**What we actually mean:**
- Set up logging and monitoring
- Create dashboards and alerts
- Track application performance

**Say this instead:**
- "Set up monitoring so we know when things break"
- "Create dashboards showing application health"
- "Implement alerts for critical issues"

---

### "Optimize resource utilization"

**What we actually mean:**
- Right-size VMs based on actual usage
- Remove unused resources
- Schedule resources to run only when needed

**Say this instead:**
- "Resize VMs to match actual usage and save money"
- "Delete resources nobody's using"
- "Turn off non-production resources outside business hours"

---

### "Implement zero-trust architecture"

**What we actually mean:**
- Remove implicit trust from network location
- Require authentication everywhere
- Use least-privilege access

**Say this instead:**
- "Require authentication for every access, even inside our network"
- "Give users only the minimum access they need"
- "Stop trusting traffic just because it's internal"

---

## Questions That Force Clarity

**When you hear buzzwords, ask:**

1. **"Can you show me an example of what that looks like?"**
   - Forces concrete thinking
   - Reveals whether they understand it themselves

2. **"What problem does this solve for us specifically?"**
   - Grounds buzzwords in actual business needs
   - Identifies if it's solution-first thinking

3. **"What would need to be true for this to succeed?"**
   - Surfaces assumptions
   - Identifies dependencies and risks

4. **"What's NOT included in this?"**
   - Defines scope clearly
   - Prevents expectation gaps

5. **"If this succeeds, what changes for [specific person/team]?"**
   - Makes impacts concrete
   - Identifies organizational change needed

6. **"How will we know if this is working?"**
   - Defines success metrics
   - Creates accountability

7. **"What happens if we don't do this?"**
   - Tests whether it's actually important
   - Reveals true priorities

8. **"What's the simplest version we could do first?"**
   - Prevents boiling the ocean
   - Creates early wins

---

## Red Flag Phrases

**When you hear these, demand clarification:**

- "Transform everything"
- "Best practices"
- "Industry standard"
- "Quick win"
- "Low hanging fruit"
- "Move the needle"
- "Synergize"
- "Leverage"
- "Paradigm shift"
- "Game changer"
- "It just works"
- "Everyone's doing it"

**These phrases hide complexity and prevent honest discussion.**

---

## The Core Principle

**If you can't explain it simply, you don't understand it well enough to implement it.**

Before saying yes to any project:
1. Force concrete examples
2. Define what's NOT included
3. Surface assumptions
4. Document understanding in writing
5. Get written confirmation

**Clarity prevents failure. Buzzwords guarantee it.**

---

**Next:** Use the [project-clarification-template.md](project-clarification-template.md) to document your understanding after meetings.
