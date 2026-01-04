---
title: "Azure VM Inventory with KQL: Track VMs Across 40+ Subscriptions (Free Workbook)"
date: 2025-09-23
modified: 2026-01-04
summary: "Free Azure VM inventory workbook with production-tested KQL queries. Track 200+ VM types across 40+ subscriptions, identify Update Manager vs Intune systems, and generate compliance reports. Instant download workbook included."
tags:
- Azure
- Intune
- Inventory
- KQL
- Resource Graph
- Update Management
- VM Inventory
- VM Management
cover: "/static/images/hero/azure-vm-inventory-kql.png"
hub: governance
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
---
## What problem are we solving?


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

As an Azure administrator, your environment is a sprawling landscape of Windows Servers, Linux boxes, and Windows clients. The challenge: **Which ones are patched by Azure Update Manager and which fall under Intune?**  
Without a unified view, you risk compliance gaps and manual guesswork. This post shows how a single KQL query can deliver clarity and save hours of troubleshooting.

---