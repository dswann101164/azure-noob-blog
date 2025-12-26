# Azure Noob Digital Products

This directory contains source files for Azure Noob digital products (ebooks, guides, query libraries).

## Directory Structure

```
digital-products/
├── README.md                           # This file
├── azure-noob-pdf-styles.css          # CSS for PDF exports
├── logo.png                            # Azure Noob logo
├── Complete-KQL-Query-Library.md      # $29 Premium KQL Pack (48 queries)
└── [future products]
```

## Products

### Complete KQL Query Library ($29)
**File:** `Complete-KQL-Query-Library.md`

48 production-tested Azure Resource Graph queries covering:
- VM Inventory & Management (10 queries)
- Networking (10 queries) 
- Security & Compliance (8 queries)
- Cost & FinOps (8 queries)
- Storage & Disks (5 queries)
- Azure Arc (3 queries)
- Databricks (2 queries)
- Advanced Scenarios (2 queries)
- SQL to KQL Translation Guide
- Performance Optimization
- Troubleshooting Guide

## How to Export PDFs

### Option 1: VS Code Markdown PDF Extension (Recommended)

1. **Install Extension:**
   - Open VS Code
   - Install "Markdown PDF" extension by yzane

2. **Configure Settings:**
   ```json
   {
     "markdown-pdf.styles": [
       "C:\\Users\\dswann\\Documents\\GitHub\\azure-noob-blog\\digital-products\\azure-noob-pdf-styles.css"
     ],
     "markdown-pdf.highlightStyle": "monokai",
     "markdown-pdf.breaks": true,
     "markdown-pdf.scale": 1
   }
   ```

3. **Export:**
   - Open markdown file
   - Press `Ctrl+Shift+P`
   - Type "Markdown PDF: Export (pdf)"
   - Select PDF

### Option 2: Pandoc (Alternative)

```bash
pandoc Complete-KQL-Query-Library.md -o Complete-KQL-Query-Library.pdf --css=azure-noob-pdf-styles.css
```

## Styling

All PDFs use Azure Noob brand colors:
- **Background:** #1E1E1E (dark)
- **Primary Text:** #FFFFFF (white)
- **Accent:** #0078D4 (Azure blue)
- **Code Blocks:** #2D2D2D with #0078D4 borders
- **Tables:** Azure blue headers, dark backgrounds

## File Organization

**Keep Local:**
- Source `.md` files stay in this directory
- Generated PDFs go here for local testing
- Don't commit generated PDFs to git (add to .gitignore)

**For Sale:**
- Export final PDFs with proper styling
- Upload to Gumroad or payment processor
- Keep source files private

## Product Roadmap

### In Development
- [ ] Arc Merger Survival Pack
- [ ] FinOps War Manual
- [ ] Napkin Test Governance Guide

### Completed
- [x] Complete KQL Query Library (48 queries)
- [x] Enterprise Azure Inventory KQL Pack (6-page free/starter)

## Notes

- Logo path in markdown: `../static/images/logo.png` (relative)
- Logo path in PDF: `logo.png` (copies to this directory)
- All queries tested on 30,000+ resources in production
- Pricing strategy: $9 starters, $19-29 full packs

## Support

Issues with PDF export? Check:
1. CSS file path in VS Code settings
2. Logo file exists in directory
3. Markdown PDF extension installed
4. Try "Reload Window" in VS Code

---

**Last Updated:** December 2025
