cat > posts/2025-10-02-mission-iron-tag.md << 'EOF'
---
title: "Operation Iron Tag — Hold the Line"
date: 2025-10-02
summary: "First campaign action: enforce CostCenter and Environment tags across the front. 100 XP · Medal: Policy Paladin"
tags: ["Quest","Azure Governance","Policy","WW2"]
cover: "/static/images/hero/cloud-wars.png"
---

> Field Dispatch: Untagged resources are slipping past our defenses and burning budget. Command has ordered immediate enforcement of tagging policy across the subscription.

## Orders
1. Create Policy: Azure Policy → Definitions → *Require tag and its value*  
   - Tag: `CostCenter`  
   - (Bonus) Tag: `Environment` (`Prod`/`Dev`/`Test`)
2. Assign the policy at Subscription or Resource Group.
3. Verify compliance:
```bash
az policy state list --query "[].{resource:resourceId,compliance:complianceState}" --output table
