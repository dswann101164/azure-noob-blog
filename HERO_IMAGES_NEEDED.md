# Hero Images Needed for Terraform + Azure DevOps CI/CD Series

This document lists the hero images that need to be created for the complete Terraform + Azure DevOps CI/CD blog series. All images should be placed in `/static/images/hero/`.

## Image Specifications

**Dimensions:** 1200px × 630px (optimal for social sharing)
**Format:** PNG (preferred) or JPG
**Color scheme:** Match Azure Noob blog theme
**Include:** Azure icons where relevant (reference: AzureIconsReference.xlsx)

## Required Hero Images

### 1. Series Index
**Filename:** `terraform-devops-series-index.png`
**Post:** 2025-11-02-terraform-azure-devops-cicd-series-index.md
**Visual concept:**
- Central theme: Complete CI/CD workflow
- Include: Terraform logo, Azure DevOps logo, arrows showing flow
- Text overlay: "Enterprise-Grade Terraform CI/CD in Azure DevOps"
- Tagline: "6-Part Complete Guide"

**Suggested elements:**
- Terraform hexagon logo
- Azure DevOps icon
- Git branch icons
- Lock/approval gate icons
- Pipeline/workflow arrows

---

### 2. Part 1 - Prerequisites & Architecture
**Filename:** `terraform-devops-part1.png`
**Post:** 2025-11-03-terraform-azure-devops-cicd-part1-prerequisites.md
**Visual concept:**
- Foundation/building blocks theme
- Include: Storage Account icon, Key Vault icon, Service Principal icon
- Text overlay: "Part 1: Prerequisites & Architecture"

**Azure icons to use:**
- Azure Storage Account (10086-icon-service-Storage-Accounts.svg)
- Azure Key Vault (10245-icon-service-Key-Vaults.svg)
- Azure Active Directory (Microsoft Entra ID)

**Suggested layout:**
- Three main icons in a row (Storage, Key Vault, Service Principal)
- Connecting lines showing relationships
- Foundation/blueprint aesthetic

---

### 3. Part 2 - Build Pipelines
**Filename:** `terraform-devops-part2.png`
**Post:** 2025-11-04-terraform-azure-devops-cicd-part2-build-pipelines.md
**Visual concept:**
- Pipeline/workflow theme
- Include: Azure Pipelines icon, validation checkmarks, artifact box
- Text overlay: "Part 2: Build Pipelines"

**Azure icons to use:**
- Azure Pipelines icon
- Git repository icon
- Build artifact icon

**Suggested layout:**
- Horizontal pipeline flow
- Status Check pipeline (top) → Plan Pipeline (bottom)
- Checkmarks for validation steps
- Artifact box at the end

---

### 4. Part 3 - Release Pipeline & Approval Gates
**Filename:** `terraform-devops-part3.png`
**Post:** 2025-11-05-terraform-azure-devops-cicd-part3-release-pipeline.md
**Visual concept:**
- Approval gate theme (emphasis on governance)
- Include: Lock/approval icons, release pipeline, Azure resources
- Text overlay: "Part 3: Release Pipeline & Approval Gates"

**Azure icons to use:**
- Azure Pipelines (release)
- Azure Resources (generic cloud icons)
- Lock/security icon

**Suggested layout:**
- Artifact → Approval Gate (big lock) → Deployment → Azure
- Human figure icon at approval gate
- Green checkmark after approval

---

### 5. Part 4 - Branch Policies
**Filename:** `terraform-devops-part4.png`
**Post:** 2025-11-06-terraform-azure-devops-cicd-part4-branch-policies.md
**Visual concept:**
- Git branching theme with enforcement
- Include: Git branch diagrams, PR icon, shield/protection icon
- Text overlay: "Part 4: Branch Policies & Pull Request Automation"

**Elements to use:**
- Git branch diagram (feature → main)
- Pull request icon
- Shield/protection symbol
- Checkmarks for required checks

**Suggested layout:**
- Branching diagram showing feature branch → PR → main
- Barriers/gates on the merge path
- Status check symbols

---

### 6. Part 5 - Production Best Practices
**Filename:** `terraform-devops-part5.png`
**Post:** 2025-11-07-terraform-azure-devops-cicd-part5-production-best-practices.md
**Visual concept:**
- Multi-environment theme
- Include: Dev/Test/Prod environments, promotion arrows
- Text overlay: "Part 5: Production Best Practices"

**Azure icons to use:**
- Multiple environment representations
- Azure Resource Groups (one per environment)
- Upward arrows (promotion)

**Suggested layout:**
- Three columns: Dev | Test | Prod
- Different colored shields or badges per environment
- Arrows showing promotion flow left to right
- Prod column has extra security/approval icons

---

### 7. Part 6 - Troubleshooting
**Filename:** `terraform-devops-part6.png`
**Post:** 2025-11-08-terraform-azure-devops-cicd-part6-troubleshooting.md
**Visual concept:**
- Debugging/problem-solving theme
- Include: Wrench/tools, warning symbols, debug icons
- Text overlay: "Part 6: Troubleshooting & Common Issues"

**Elements to use:**
- Wrench or screwdriver icon (tools)
- Warning/alert triangles
- Magnifying glass (investigation)
- Red X → Green checkmark (problem → solution)

**Suggested layout:**
- Split design: Problem side (red/orange) | Solution side (green)
- Tool icons scattered throughout
- Code snippet or terminal window aesthetic

---

## Design Guidelines

### Color Palette
Use colors consistent with your blog's theme:
- **Primary:** Azure blue (#0078D4)
- **Secondary:** Terraform purple (#844FBA)
- **Success:** Green (#107C10)
- **Warning:** Orange (#FF8C00)
- **Error:** Red (#E81123)
- **Background:** Dark navy or white (depending on blog theme)

### Typography
- **Font:** Sans-serif (e.g., Segoe UI, Open Sans, Roboto)
- **Title size:** 48-60px (bold)
- **Subtitle/tagline:** 24-32px
- **Ensure readability:** High contrast text on background

### Azure Icons
Reference the `AzureIconsReference.xlsx` file for exact icon names and SVG file paths. Key icons for this series:
- Storage Accounts: `10086-icon-service-Storage-Accounts.svg`
- Key Vault: `10245-icon-service-Key-Vaults.svg`
- Azure Pipelines: (from Azure DevOps icon set)
- Resource Groups: `10007-icon-service-Resource-Groups.svg`

### Design Tools
Recommended tools for creating these images:
- **Figma** (free, web-based, collaborative)
- **Canva** (free templates, easy to use)
- **Adobe Illustrator** (professional)
- **PowerPoint** (surprisingly good for tech diagrams)
- **Excalidraw** (hand-drawn aesthetic)

### Export Settings
- Format: PNG
- Resolution: 1200 × 630px
- DPI: 72 (web standard)
- Color mode: RGB
- Compression: Optimize for web (keep under 500KB if possible)

---

## Alternative: AI-Generated Images

If designing custom images isn't feasible, consider using AI tools:

### Option 1: DALL-E / Midjourney
Prompt template:
```
"Create a hero image for a technical blog post about [TOPIC]. 
Style: Clean, professional, technical diagram aesthetic. 
Include: [Azure icons, Terraform logos, CI/CD pipeline elements]. 
Color scheme: Azure blue, purple accents. 
Dimensions: 1200x630px. 
Text overlay: '[TITLE]'"
```

### Option 2: Stable Diffusion
Similar prompt structure, focus on technical accuracy and clean design.

### Option 3: Use Azure Icons Directly
Simple approach:
1. Export key icons from AzureIconsReference.xlsx
2. Arrange in PowerPoint or Figma
3. Add title text overlay
4. Export as PNG

---

## Status Tracking

Use this checklist to track hero image creation:

- [ ] Series Index (`terraform-devops-series-index.png`)
- [ ] Part 1 - Prerequisites (`terraform-devops-part1.png`)
- [ ] Part 2 - Build Pipelines (`terraform-devops-part2.png`)
- [ ] Part 3 - Release Pipeline (`terraform-devops-part3.png`)
- [ ] Part 4 - Branch Policies (`terraform-devops-part4.png`)
- [ ] Part 5 - Production Best Practices (`terraform-devops-part5.png`)
- [ ] Part 6 - Troubleshooting (`terraform-devops-part6.png`)

---

## Temporary Placeholder Images

Until custom hero images are created, you can use:

**Option 1: Solid color with text overlay**
- Background: Azure blue gradient
- Text: Post title in white
- Simple but professional

**Option 2: Azure portal screenshot**
- Blurred screenshot of Azure DevOps pipelines
- Text overlay: Post title
- Quick to create, relevant visual

**Option 3: Generic tech abstract**
- Blue/purple gradient
- Hexagon pattern (Terraform aesthetic)
- Text overlay: Post title

---

## Notes

- All 7 posts are now written and committed to the repository
- Hero images are the last remaining task before publication
- Posts are already configured with the correct cover image paths
- Once images are created, just drop them into `/static/images/hero/`
- No code changes needed after images are added

---

**Total images needed:** 7
**Estimated time to create:** 2-4 hours (depending on design experience)
**Priority:** Medium (posts work without images, but images improve SEO and social sharing)
