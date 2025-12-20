---
title: 'Azure Monitoring Dashboard: Modernize Workbooks (50→200+ Services)'
date: 2025-09-28
modified: 2025-12-20
summary: 'Production Azure monitoring dashboard examples using Workbooks. Enhance from 50 to 200+ services with global filters, KQL queries, and portal integration. Free workbook JSON templates included.'
tags:
- Azure
- Community
- Dashboards
- KQL
- Monitoring
- Open Source
- Workbooks
cover: static/images/hero/azure-workbook-enhancement.png
hub: governance
related_posts:
  - azure-resource-tags-guide
  - azure-tag-governance-policy
  - azure-policy-reality-check
---
## Why Nobody Teaches Workbooks


This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.

Azure Monitor Workbooks are one of the most powerful operational tools in Azure. Yet **zero Azure certifications teach how to build them.**

The AZ-104 exam mentions Workbooks exist. That's it. No hands-on labs. No dashboard design principles. No KQL for data source integration. Nothing about parameters, filters, or creating Workbooks teams actually use.

I wrote about this certification gap here: [The Azure Role Microsoft Forgot to Certify](/blog/azure-reporting-role-microsoft-should-create/).

The irony: Azure admins spend more time building Workbooks and dashboards than deploying VMs, but Microsoft doesn't validate these skills. So we learn from community examples like Billy York's Azure Inventory Workbook.

Here's how I modernized it for 2025.

---

## Dashboard Examples Included

This guide shows you how to build production-grade Azure monitoring dashboards using Workbooks:

**Inventory Dashboards:**
- All 200+ Azure service types across subscriptions
- Global subscription/resource group filtering
- Resource health and compliance status

**Security Dashboards:**
- NSG rule analysis and port exposure
- Untagged resource detection
- Compliance scoring by resource type

**Cost Dashboards:**
- Resource distribution by type and location
- Tag-based cost allocation views
- Orphaned resource identification

[Jump to implementation →](#key-technical-enhancements)

---

Azure Monitor Workbooks are powerful tools for creating custom dashboards and reports, but keeping them current with Azure's rapidly expanding service catalog can be challenging. Recently, I enhanced Billy York's excellent Azure Inventory Workbook to support modern Azure environments while fixing several technical issues that had accumulated over time.

## Building on Solid Foundations

Billy York created the original Azure Inventory Workbook as a comprehensive tool for analyzing Azure resources using Azure Resource Graph queries. His work provided an excellent foundation with well-structured KQL queries and a logical organization that made it easy to navigate different resource types.

However, as Azure has evolved significantly since 2022, several gaps had emerged:
- Limited support for modern services introduced between 2020-2025
- Broken conditional visibility in some tabs
- Missing global filtering capabilities
- No direct portal integration for resource management

## Key Technical Enhancements

### Expanded Service Coverage (50+ to 200+ Services)

The original workbook supported common Azure services, but modern environments often include newer offerings like Azure Container Apps, Static Web Apps, and enhanced AI services. I systematically expanded the resource type mappings:

```kql
| extend type = case(
    type contains 'microsoft.containerservice/managedclusters', 'AKS Clusters',
    type contains 'microsoft.web/staticsites', 'Static Web Apps',
    type contains 'microsoft.cognitiveservices/accounts', 'Cognitive Services',
    type contains 'microsoft.machinelearningservices/workspaces', 'ML Workspaces',
    // ... 200+ service mappings
    strcat("Not Translated: ", type))
```

This expansion ensures that modern Azure environments display meaningful service names rather than cryptic resource provider identifiers.

### Fixed Conditional Visibility Issues

One significant problem was the Security Hygiene Issues tab, which was completely non-functional due to missing conditional visibility parameters. The fix involved:

1. **Adding proper parameter definitions:**
```json
{
  "id": "main-tab-parameter",
  "version": "KqlParameterItem/1.0", 
  "name": "selectedTab",
  "type": 1,
  "value": "overview"
}
```

2. **Implementing working conditional visibility:**
```json
"conditionalVisibility": {
  "parameterName": "selectedTab",
  "comparison": "isEqualTo", 
  "value": "Security Hygiene Issues"
}
```

### Global Filtering System

Enterprise environments often need to focus on specific resource groups or tagged resources. I implemented global filtering that works across all tabs:

```kql
| where resourceGroup =~ '{ResourceGroup}' or '{ResourceGroup}' == ''
| where tostring(tags) contains '{TagFilter}' or '{TagFilter}' == ''
```

The key technical detail here is using `tostring(tags)` to enable the `contains` operator, since tags are stored as complex objects in Azure Resource Graph.

### Portal Integration and User Experience

Resource management often requires jumping to the Azure portal. I added clickable resource links throughout the workbook:

```kql
| extend ResourceLink = strcat('https://portal.azure.com/#resource', id)
```

Combined with formatter configurations that make resource names clickable:

```json
{
  "columnMatch": "name",
  "formatter": 7,
  "formatOptions": {
    "linkTarget": "Url",
    "linkColumnName": "ResourceLink",
    "showIcon": true
  }
}
```

### Intelligent Resource Naming

Azure Advisor recommendations often display GUIDs instead of meaningful resource names. I solved this with intelligent name resolution:

```kql
| extend resourceName = case(
    isempty(rawResourceName) or strlen(rawResourceName) > 50, split(affectedResource, '/')[8],
    rawResourceName contains "-" and strlen(rawResourceName) > 30, "Subscription-level",
    rawResourceName
)
```

This logic extracts the actual resource name from the resource ID when the displayed name is unhelpful.

## New Functional Capabilities

### Security Hygiene Monitoring

The enhanced workbook includes proactive security monitoring that identifies common misconfigurations:

```kql
| extend Issue = case(
    type =~ 'microsoft.storage/storageaccounts' and tostring(properties.supportsHttpsTrafficOnly) != 'true', 
    'Storage allows HTTP traffic',
    type =~ 'microsoft.keyvault/vaults' and tostring(properties.enableSoftDelete) != 'true', 
    'Key Vault soft delete disabled',
    type =~ 'microsoft.compute/virtualmachines' and tostring(identity.type) in ('', 'None'), 
    'VM without managed identity',
    'No issues detected'
)
```

### Cost and Advisor Integration

A dedicated tab surfaces Azure Advisor recommendations with proper resource context, helping teams prioritize cost optimization and performance improvements.

### Enhanced Visual Indicators

Modern workbooks benefit from clear visual cues. I implemented consistent icon usage throughout:

```json
"formatOptions": {
  "thresholdsOptions": "icons",
  "thresholdsGrid": [
    {
      "operator": "==",
      "thresholdValue": "PowerState/running",
      "representation": "Available",
      "text": "{0}{1}"
    },
    {
      "operator": "==", 
      "thresholdValue": "PowerState/deallocated",
      "representation": "disabled",
      "text": "{0}{1}"
    }
  ]
}
```

## Community Collaboration Approach

This enhancement project reinforced several important principles for working with community tools:

**Proper Attribution**: Billy York's original work deserved full credit. The enhanced version clearly builds upon his foundation rather than replacing it.

**Transparent Communication**: I created a GitHub issue on the original repository to inform Billy York about the enhancements, opening the door for potential collaboration.

**Independent Value**: While respecting the original project, the enhanced version provides immediate value to users who need modern service support.

## Installation and Usage

The enhanced workbook is available at: https://github.com/dswann101164/azure-inventory-workbook-enhanced

**Installation steps:**
1. Download the `.workbook` file from the repository
2. In Azure Monitor, navigate to Workbooks
3. Click "New" then "Advanced Editor"
4. Paste the workbook content and save
5. Ensure you have Reader access to the resources you want to inventory

**Key features to explore:**
- Global filtering by resource group and tags
- Modern service support across all tabs
- Security hygiene monitoring for compliance checks
- Cost optimization recommendations from Azure Advisor
- Direct portal links for resource management

## Technical Lessons Learned

Working with Azure Monitor Workbooks highlighted several important considerations:

**Parameter Management**: Complex workbooks need careful parameter organization. Global parameters should be defined early and referenced consistently.

**Conditional Visibility**: This powerful feature requires precise parameter matching. Small typos can break entire sections.

**KQL Performance**: Resource Graph queries should filter early and extend late to optimize performance across large Azure environments.

**Community Engagement**: The Azure community values tools that solve real operational problems. Proper attribution and collaborative approaches build trust and encourage adoption.

## Looking Forward

The enhanced workbook demonstrates how community tools can evolve to meet changing needs while respecting original contributors. Azure's service catalog continues expanding rapidly, and community-driven tools like this help practitioners keep pace with new capabilities.

For Azure administrators and architects managing complex environments, having comprehensive visibility into resource inventory, security posture, and cost optimization opportunities is essential. Tools like this enhanced workbook provide that visibility while integrating seamlessly into existing Azure workflows.

## Repository and Community

The enhanced Azure Inventory Workbook is available on GitHub with full documentation and installation instructions. Community feedback and contributions are welcome as Azure continues evolving and new services emerge.

**GitHub Repository**: https://github.com/dswann101164/azure-inventory-workbook-enhanced  
**Original Work by Billy York**: https://github.com/scautomation/Azure-Inventory-Workbook

This project exemplifies how the Azure community can collaborate to maintain and improve valuable tools, ensuring they remain relevant and useful as the platform evolves.