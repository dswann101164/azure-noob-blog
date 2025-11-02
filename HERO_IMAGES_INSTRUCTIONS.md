# Hero Images - Generation Instructions

## Quick Start (Automated - Recommended)

I've created a Python script that will generate all 7 hero images at once.

### Step 1: Install Required Package

```powershell
pip install Pillow
```

### Step 2: Run the Generation Script

```powershell
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog
python create_hero_images.py
```

This will create all 7 images in `static/images/hero/` with:
- Correct dimensions (1200×630px)
- Azure blue gradient backgrounds
- Professional typography
- Consistent styling

---

## What Gets Created

The script generates these images:

1. **terraform-devops-series-index.png** - Series landing page
2. **terraform-devops-part1.png** - Prerequisites & Architecture  
3. **terraform-devops-part2.png** - Build Pipelines
4. **terraform-devops-part3.png** - Release Pipeline & Approval Gates
5. **terraform-devops-part4.png** - Branch Policies
6. **terraform-devops-part5.png** - Production Best Practices
7. **terraform-devops-part6.png** - Troubleshooting

---

## Alternative: Manual Creation (If Python Script Doesn't Work)

If you prefer to create these manually or the Python script has issues:

### Option 1: Use Canva (Easiest)

1. Go to **[Canva.com](https://www.canva.com)**
2. Create custom size: **1200 × 630 px**
3. Use template: "Twitter Header" or "Social Media Post"
4. Background: Azure blue gradient (#003D7A → #0078D4)
5. Add text overlays per the specifications in `HERO_IMAGES_NEEDED.md`
6. Export as PNG

### Option 2: Use PowerPoint

1. **Open PowerPoint**
2. **Design > Slide Size > Custom Slide Size**
   - Width: 16.67 inches
   - Height: 8.75 inches
   - (These scale to 1200×630px at 72 DPI)
3. **Design > Format Background**
   - Gradient fill
   - Color 1: Dark Azure (#003D7A)
   - Color 2: Azure Blue (#0078D4)
4. **Insert > Text Box**
   - Add title text (white, Arial Bold, 60pt)
   - Add subtitle text (light gray, Arial, 32pt)
5. **File > Save As > PNG**
6. Save each slide as individual PNG

### Option 3: Use Figma (Professional)

1. Go to **[Figma.com](https://www.figma.com)**
2. Create frame: 1200 × 630
3. Add rectangle: Full frame, gradient fill
4. Add text layers per spec
5. Export as PNG (2x resolution recommended)

---

## After Creating Images

Once you have the images:

```powershell
# Navigate to blog root
cd C:\Users\dswann\Documents\GitHub\azure-noob-blog

# Verify images are in place
ls static/images/hero

# You should see all 7 PNG files

# Generate static site
python freeze.py

# Commit and push
git add static/images/hero posts docs
git commit -m "Add hero images for Terraform CI/CD series"
git push origin main
```

---

## Troubleshooting

### "Module 'PIL' not found"

```powershell
pip install Pillow
```

### "Python not recognized"

```powershell
# Use full path to Python
C:\Users\dswann\AppData\Local\Programs\Python\Python311\python.exe create_hero_images.py
```

Or install Python from: https://www.python.org/downloads/

### "Permission denied writing to static/images/hero"

```powershell
# Create directory first
mkdir static\images\hero -Force
python create_hero_images.py
```

---

## Design Specifications (For Manual Creation)

### Colors
- **Background Gradient:** #003D7A (dark) → #0078D4 (light)
- **Title Text:** #FFFFFF (white)
- **Subtitle Text:** #F3F2F1 (light gray)
- **Accent:** #844FBA (Terraform purple)

### Typography
- **Title:** Arial Bold, 60pt
- **Subtitle:** Arial Regular, 32pt  
- **Branding:** Arial Bold, 24pt

### Layout
- **Dimensions:** 1200 × 630 pixels
- **Branding:** "Azure Noob" in top left (40px margin)
- **Title:** Centered, vertically middle
- **Subtitle:** Below title, centered
- **Accent line:** 360px wide, 5px height, below branding

---

## Quick Reference: Text for Each Image

### Series Index
- **Title:** Enterprise Terraform CI/CD
- **Subtitle:** Complete 6-Part Series

### Part 1
- **Title:** Part 1: Prerequisites
- **Subtitle:** Foundation & Architecture

### Part 2
- **Title:** Part 2: Build Pipelines
- **Subtitle:** Status Checks & Plan Creation

### Part 3
- **Title:** Part 3: Release Pipeline
- **Subtitle:** Deployment & Approval Gates

### Part 4
- **Title:** Part 4: Branch Policies
- **Subtitle:** GitOps Enforcement

### Part 5
- **Title:** Part 5: Production Setup
- **Subtitle:** Multi-Environment Best Practices

### Part 6
- **Title:** Part 6: Troubleshooting
- **Subtitle:** Real Production Issues & Solutions

---

## Need Help?

1. Check that `create_hero_images.py` exists in your blog root
2. Verify Python and Pillow are installed
3. Try running with `python -v create_hero_images.py` for verbose output
4. If all else fails, use Canva (free, web-based, takes ~30 minutes for all 7)
