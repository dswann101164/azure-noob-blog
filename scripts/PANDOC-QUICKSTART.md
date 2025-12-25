# PANDOC PDF AUTOMATION - QUICK START GUIDE

## 📦 What You Have

Three PowerShell scripts in `/scripts/`:

1. **install-pandoc.ps1** - Installs Pandoc + LaTeX (one-time setup)
2. **convert-all-pdfs.ps1** - Converts all 7 guides to PDF automatically
3. **azure-template.tex** - Professional LaTeX template with Azure branding

---

## 🚀 QUICK START (3 Commands)

### Step 1: Install Pandoc (One-Time, ~30 minutes)

```powershell
# Open PowerShell AS ADMINISTRATOR (right-click > Run as Administrator)
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog\scripts

# Run installation script
.\install-pandoc.ps1
```

**What it does:**
- Installs Chocolatey package manager
- Installs Pandoc (markdown converter)
- Installs MiKTeX (LaTeX engine - ~4GB download)
- Verifies installation

**Wait time:** 10-30 minutes depending on internet speed

**After completion:** Close PowerShell and reopen (loads new PATH)

---

### Step 2: Convert All PDFs (2 minutes)

```powershell
# Open NEW PowerShell window (regular, not admin)
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog\scripts

# Run conversion script
.\convert-all-pdfs.ps1
```

**What it does:**
- Finds all 7 blog post markdown files
- Converts each to professional PDF using Azure template
- Adds branding, headers, footers, table of contents
- Saves to `/static/downloads/`
- Reports success/failure for each

**Output:**
```
✓ Linux-Commands-Azure-Admins-2025.pdf (2.3 MB)
✓ Windows-Commands-Azure-Admins-2025.pdf (1.8 MB)
✓ PowerShell-7-Migration-Checklist-2025.pdf (1.2 MB)
✓ Terraform-Troubleshooting-Guide-2025.pdf (1.5 MB)
✓ Private-Endpoint-DNS-Guide-2025.pdf (1.1 MB)
✓ Azure-Update-Manager-Reference-2025.pdf (0.9 MB)
✓ Azure-Hybrid-Benefit-Compliance-Guide-2025.pdf (1.4 MB)
```

---

### Step 3: Commit to Git

```powershell
# Add PDFs to git
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog
git add static/downloads/*.pdf

# Commit
git commit -m "Add 7 professional PDF reference guides for Azure Admin Library"

# Push
git push
```

---

## 🎨 Template Features

The `azure-template.tex` includes:

✅ **Professional Title Page**
- Azure-Noob.com branding
- Guide title and subtitle
- Author, date, version info
- Copyright notice

✅ **Automatic Table of Contents**
- Numbered sections
- Clickable page links
- Auto-generated from headers

✅ **Headers & Footers**
- Left header: "Azure-Noob.com"
- Right header: Guide title
- Left footer: Copyright
- Center footer: Page numbers
- Right footer: Version

✅ **Azure Brand Colors**
- Azure Blue (#0078D4) for headings
- Light blue backgrounds for code
- Professional gray for text

✅ **Code Block Styling**
- Syntax highlighting
- Gray background boxes
- Proper line wrapping
- Professional monospace font

✅ **Callout Boxes**
- Pro Tips (blue)
- Warnings (yellow)
- Enterprise Notes (green)

✅ **Professional Tables**
- Azure blue borders
- Clean formatting
- Auto-width columns

---

## 🔧 Customization

### Change Title/Subtitle for a Guide

Edit `convert-all-pdfs.ps1`:

```powershell
@{
    Name = "Linux Commands for Azure Admins"
    SourceFile = "2025-12-08-50-linux-commands-azure.md"
    OutputFile = "Linux-Commands-Azure-Admins-2025.pdf"
    Title = "YOUR NEW TITLE HERE"           # <-- Change this
    Subtitle = "YOUR NEW SUBTITLE HERE"     # <-- Change this
}
```

### Convert Single Guide

```powershell
pandoc posts\2025-12-08-50-linux-commands-azure.md `
  -o static\downloads\Linux-Commands-Azure-Admins-2025.pdf `
  --template=scripts\azure-template.tex `
  --pdf-engine=pdflatex `
  --toc `
  --number-sections `
  -V "title=50 Essential Linux Commands for Azure Admins" `
  -V "subtitle=Complete 2025 Guide" `
  -V "author=David Swann" `
  -V "date=December 2025" `
  -V "version=1.0"
```

### Modify Template Colors

Edit `azure-template.tex`:

```latex
% Azure Brand Colors
\definecolor{azureblue}{RGB}{0,120,212}      % Main headings
\definecolor{azuredark}{RGB}{16,110,190}     % Sub headings
\definecolor{azurelight}{RGB}{80,230,255}    % Callouts
\definecolor{codegray}{RGB}{245,245,245}     % Code backgrounds
\definecolor{textgray}{RGB}{50,49,48}        % Body text
```

---

## ⚠️ Troubleshooting

### Error: "pandoc: command not found"

**Solution:** Close and reopen PowerShell to reload PATH

### Error: "pdflatex: command not found"

**Solution:** 
1. Verify MiKTeX installed: `Get-Command pdflatex`
2. If not, run `choco install miktex -y`
3. Close and reopen PowerShell

### Error: "! LaTeX Error: File not found"

**Solution:** Missing LaTeX package. MiKTeX will prompt to install on first run. Click "Install" when prompted.

### PDF Generated but Formatting Looks Wrong

**Solution:**
1. Check source markdown has proper heading levels (# ## ###)
2. Verify code blocks use triple backticks with language: ```bash
3. Check tables use proper markdown table syntax

### PDF File Size > 5 MB

**Solution:**
1. Remove large embedded images from markdown
2. Compress images before embedding
3. Or: Accept larger size (not critical for digital product)

---

## 📊 Expected Results

| Guide | Estimated Size | Page Count |
|-------|---------------|------------|
| Linux Commands | 2-3 MB | 35-45 pages |
| Windows Commands | 1-2 MB | 30-40 pages |
| PowerShell 7 | 1-2 MB | 25-30 pages |
| Terraform | 1-2 MB | 25-35 pages |
| Private Endpoint | 1-2 MB | 20-25 pages |
| Update Manager | 1-2 MB | 20-25 pages |
| Hybrid Benefit | 1-2 MB | 25-30 pages |
| **TOTAL** | **10-15 MB** | **180-230 pages** |

---

## 🎯 Quality Checklist

After conversion, verify each PDF:

- [ ] Title page looks professional
- [ ] Table of contents auto-generated
- [ ] Headers/footers on all pages
- [ ] Code blocks formatted with gray background
- [ ] Tables render correctly
- [ ] Page numbers sequential
- [ ] No blank pages
- [ ] File size < 5 MB
- [ ] All internal links work
- [ ] Text is selectable (not images)

---

## 📁 File Structure

After running scripts:

```
azure-noob-blog/
├── scripts/
│   ├── install-pandoc.ps1           ← Run once (admin)
│   ├── convert-all-pdfs.ps1         ← Run to generate PDFs
│   ├── azure-template.tex           ← Professional template
│   └── PANDOC-QUICKSTART.md         ← This file
├── posts/
│   ├── 2025-12-08-50-linux-commands-azure.md
│   ├── 2025-12-08-50-windows-commands-azure.md
│   └── ... (other blog posts)
└── static/downloads/
    ├── Linux-Commands-Azure-Admins-2025.pdf       ← Generated
    ├── Windows-Commands-Azure-Admins-2025.pdf     ← Generated
    ├── PowerShell-7-Migration-Checklist-2025.pdf  ← Generated
    └── ... (other PDFs)
```

---

## ⏱️ Time Investment

**First Run (with installation):**
- Install Pandoc + LaTeX: 10-30 min (mostly waiting)
- Run conversion script: 2-5 min
- Quality check all PDFs: 20-30 min
- **Total: 30-65 minutes**

**Subsequent Runs (updates):**
- Modify blog post markdown
- Run conversion script: 1-2 min
- Quality check: 5 min
- **Total: 6-7 minutes**

---

## 🚀 READY TO START?

Run this now:

```powershell
# Open PowerShell AS ADMINISTRATOR
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog\scripts
.\install-pandoc.ps1
```

Then come back here when it finishes!

---

**Questions? Issues? Let me know and I'll help debug!** 🎯
