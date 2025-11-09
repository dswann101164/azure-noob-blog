# Project Clarification Template

**Use this email template after every meeting where work is agreed to.**

Force written confirmation of mutual understanding BEFORE starting work. This prevents 90% of project failures.

---

## Template: Project Confirmation Email

```
Subject: Confirming our understanding - [PROJECT NAME]

Hi [Name],

Following up on today's meeting to make sure we're aligned before starting work.

## BUSINESS GOAL
**Problem we're solving:**
[Describe the business problem in non-technical terms]

**How we'll measure success:**
- [Specific metric or outcome]
- [Another metric or outcome]
- [Timeline for seeing results]

## TECHNICAL APPROACH
**What I'm building:**
[One sentence description of the deliverable]

**How it works:**
[2-3 sentences explaining the approach in simple terms]

**What data/access I need:**
- [Specific access or permissions]
- [Data sources required]
- [Dependencies on other teams]

## DELIVERABLE
**What you'll receive:**
[Specific description - dashboard, report, script, infrastructure, etc.]

**Format:**
[Power BI dashboard / Excel report / Terraform code / Azure resources / etc.]

**Example of what it looks like:**
[Attach mockup or screenshot if possible, or describe clearly]

## TIMELINE
**Development:** [X weeks]
**Testing:** [X weeks]
**Deployment:** [Specific date]
**Total:** [X weeks from start to finish]

## WHAT'S NOT INCLUDED
This project does NOT include:
- [Specific scope exclusion]
- [Another exclusion]
- [Why these are excluded - usually complexity, dependencies, or cost]

## ASSUMPTIONS & DEPENDENCIES
**I'm assuming:**
- [Assumption about current state]
- [Assumption about access]
- [Assumption about priorities]

**This depends on:**
- [External dependency]
- [Team dependency]
- [Resource availability]

## RISKS
**What could delay this:**
- [Technical risk and mitigation]
- [Organizational risk and mitigation]
- [Dependency risk and mitigation]

**What could invalidate this approach:**
- [Condition that would require different solution]
- [Discovery that would change scope]

## NEXT STEPS
1. [Your immediate next action]
2. [What you need from them]
3. [When you'll provide next update]

## CONFIRMATION NEEDED
Please confirm:
✓ This matches your understanding of the goal
✓ The deliverable is what you expected
✓ The timeline aligns with your needs
✓ The scope exclusions are acceptable
✓ The assumptions are correct

If anything doesn't match your expectations, please let me know so we can align before I start work.

Thanks,
[Your name]
```

---

## Why This Works

### 1. Forces You to Understand
If you can't fill out this template, you don't understand the project well enough to start.

### 2. Creates Written Record
When scope creeps or expectations drift, you have documentation of what was actually agreed to.

### 3. Surfaces Misunderstandings Early
They'll reply with "Actually, I thought you were building X" - better to discover this now than after 6 weeks.

### 4. Makes You Look Professional
This level of clarity demonstrates expertise. You're not someone who just starts coding and hopes for the best.

### 5. Protects Everyone
When the project succeeds, this shows what you delivered. When it "fails," this shows you delivered exactly what was agreed to.

---

## Customization Examples

### For Infrastructure Projects

```
## INFRASTRUCTURE CHANGES
**What's being deployed:**
- [Specific Azure resources with sizes]
- [Networking changes]
- [Security configurations]

**Impact:**
- [Who/what is affected]
- [Downtime required, if any]
- [Rollback plan]
```

### For Reporting Projects

```
## REPORT DETAILS
**Data sources:**
- [Where data comes from]
- [How current - real-time, daily, weekly?]
- [Data quality limitations]

**Audience:**
- [Who will use this]
- [How they'll access it]
- [Training needed]
```

### For Migration Projects

```
## MIGRATION SCOPE
**What's being migrated:**
- [Specific applications/workloads]
- [Order of migration]
- [What's NOT migrating and why]

**Testing approach:**
- [Test environment setup]
- [Validation criteria]
- [Rollback triggers]
```

---

## Dealing with Pushback

### "This seems like overkill"
"I want to make sure I'm building exactly what you need. This takes 15 minutes now, saves weeks later."

### "We don't have time for this"
"We don't have time to rebuild the wrong thing. This prevents that."

### "Just start building, we'll figure it out"
"That approach has failed for me before. I need written confirmation of scope."

### "Don't you trust us?"
"I trust us to forget details from verbal conversations. This protects both of us."

### "We're agile, we don't need detailed planning"
"Agile doesn't mean no planning. It means short iterations with clear goals. This defines the first iteration."

---

## Common Mistakes to Avoid

### ❌ DON'T:
- Write this template and not send it
- Wait for them to ask questions
- Assume silence means agreement
- Start work before getting confirmation
- Skip the "what's NOT included" section

### ✅ DO:
- Send within 24 hours of the meeting
- Follow up if no response in 2 days
- Update the template when requirements change
- Reference it when scope creeps
- Keep a folder of all confirmations

---

## Template Variations by Role

### For Presenting to Leadership
```
Subject: Executive Summary - [PROJECT]

## BUSINESS VALUE
[What problem this solves]
[How much it costs to not solve it]
[Expected ROI or benefit]

## APPROACH
[High-level approach in 2 sentences]

## TIMELINE & COST
[Duration and resource requirements]

## DECISION NEEDED
[What you need from them to proceed]

[Detailed technical approach attached as appendix]
```

### For Technical Team Coordination
```
Subject: Technical Alignment - [PROJECT]

## ARCHITECTURE
[Technical design decisions]
[Integration points]
[Technology choices and why]

## DEPENDENCIES
[What we need from other teams]
[Timeline for dependencies]
[Escalation if dependencies block]

## DEFINITION OF DONE
[Specific technical acceptance criteria]
[Testing requirements]
[Documentation deliverables]
```

### For Vendor/Consultant Engagement
```
Subject: Statement of Work Confirmation - [PROJECT]

## DELIVERABLES
[Specific outputs expected]
[Format and quality standards]
[Delivery schedule]

## YOUR RESPONSIBILITIES
[What vendor provides]
[Access/information needed]
[Response time commitments]

## OUR RESPONSIBILITIES
[What you provide]
[Decision-making authority]
[Payment terms]

## SUCCESS CRITERIA
[How we measure if this worked]
[Acceptance criteria]
[Warranty/support period]
```

---

## The One-Sentence Version

**If you only remember one thing:**

> "Before starting any project, send an email summarizing what you're building, what success looks like, and what's NOT included. Get written confirmation. Reference it when scope creeps."

---

## Integration with Your Workflow

### Immediate After Meeting
1. Open this template
2. Fill it out while details are fresh
3. Identify anything you're unclear about
4. Email stakeholders with questions
5. Wait for clarity before finalizing

### Before Sending
- Review with a colleague
- Check that a non-technical person could understand it
- Verify all assumptions are listed
- Confirm exclusions are explicit

### After Sending
- File confirmation in project folder
- Add to project tracking system
- Reference in kickoff meeting
- Update when requirements change

### During Project
- Reference when stakeholders request additions
- Update if scope formally changes
- Attach to status reports
- Use in retrospectives

---

## Real Examples

### Bad (Vague Agreement)
```
"I'll build a cost dashboard showing department spend."
```
**Problem:** What data? What timeframe? What format? How is "department" defined? Who accesses it?

### Good (Clarified Agreement)
```
"I'll build a Power BI dashboard showing Azure consumption costs by department for the current month and prior 12 months. Cost will be allocated based on the 'CostCenter' resource tag. Department mapping comes from the Finance-provided spreadsheet. Finance team will have read access. Dashboard updates daily at 6 AM. This does NOT include costs for untagged resources (currently 40% of total) - those will show as 'Unallocated.' Timeline: 4 weeks."
```
**Why better:** Specific data source, allocation method, access, update frequency, known limitations, and timeline.

---

## The Hard Truth

**90% of failed projects fail because:**
- Nobody documented what was agreed to
- Different people understood different things
- Scope crept without acknowledgment
- Success criteria were never defined
- Both sides assumed the other understood

**This template prevents all of that.**

**It takes 15 minutes. It saves weeks.**

**Use it.**

---

**Next Steps:**
1. Save this template to your email drafts
2. After your next project meeting, fill it out
3. Send it to stakeholders
4. Insist on written confirmation
5. Reference it when things go sideways

**Your project success rate will transform overnight.**
