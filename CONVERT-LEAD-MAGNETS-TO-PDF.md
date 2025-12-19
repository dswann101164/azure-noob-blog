# CONVERT-LEAD-MAGNETS-TO-PDF.md

# Converting Lead Magnets to PDF

Your lead magnets are ready at:
- `static/downloads/Azure-AI-Cost-Cheat-Sheet-2025.md`
- `static/downloads/KQL-Query-Library-Complete.md`

## Option 1: Online Converter (Easiest)

### Method 1: Markdown to PDF
1. Go to: https://www.markdowntopdf.com/
2. Click "Choose File" and select: `Azure-AI-Cost-Cheat-Sheet-2025.md`
3. Click "Convert"
4. Download the PDF
5. Save to: `static/downloads/Azure-AI-Cost-Cheat-Sheet-2025.pdf`
6. Repeat for: `KQL-Query-Library-Complete.md`

### Method 2: Dillinger (Better Formatting)
1. Go to: https://dillinger.io/
2. Click "Import from" → "Markdown File"
3. Select: `Azure-AI-Cost-Cheat-Sheet-2025.md`
4. Click "Export as" → "PDF"
5. Save to: `static/downloads/Azure-AI-Cost-Cheat-Sheet-2025.pdf`
6. Repeat for: `KQL-Query-Library-Complete.md`

## Option 2: Pandoc (If Installed)

### Check if Pandoc is installed:
```powershell
pandoc --version
```

### Install Pandoc (if needed):
```powershell
winget install --id=JohnMacFarlane.Pandoc
```

### Convert to PDF:
```powershell
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

pandoc static/downloads/Azure-AI-Cost-Cheat-Sheet-2025.md -o static/downloads/Azure-AI-Cost-Cheat-Sheet-2025.pdf --pdf-engine=wkhtmltopdf

pandoc static/downloads/KQL-Query-Library-Complete.md -o static/downloads/KQL-Query-Library-Complete.pdf --pdf-engine=wkhtmltopdf
```

## After Conversion

Once you have the PDFs:

1. **Verify the PDFs look good** (open and check formatting)

2. **Deploy the PDFs:**
```powershell
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

python freeze.py

git add static/downloads/*.pdf
git add docs/

git commit -m "Add: Lead magnet PDFs (Azure AI Cost Cheat Sheet + KQL Query Library)"

git push origin main
```

3. **Add download CTAs to blog posts:**

### In OpenAI Pricing Post
Add before "Related Posts":
```markdown
---

## 📥 Free Download: Azure AI Cost Cheat Sheet

**Get the complete pricing reference** with model comparison tables, cost calculator, and optimization strategies.

[Download Azure AI Cost Cheat Sheet (PDF)](/static/downloads/Azure-AI-Cost-Cheat-Sheet-2025.pdf)

Includes:
- GPT-4, GPT-4o, GPT-3.5 pricing tables
- Real cost calculator formula
- Hidden costs checklist
- PTU vs pay-as-you-go decision matrix

---
```

### In KQL Posts
Add before "Related Posts":
```markdown
---

## 📥 Free Download: Complete KQL Query Library

**Get 30+ production-ready KQL queries** for cost analysis, security audits, and inventory management.

[Download KQL Query Library (PDF)](/static/downloads/KQL-Query-Library-Complete.pdf)

Includes:
- Cost analysis and FinOps queries
- Security and compliance queries
- Performance and inventory queries
- Network analysis queries
- Azure Arc queries

---
```

## Expected Impact

- **Email list foundation** for future product sales
- **Higher engagement** on pricing and KQL posts
- **Backlink opportunities** when people share the PDFs
- **Authority building** through valuable free resources

---

**Estimated time:** 10-15 minutes total
