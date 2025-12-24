# GitHub Callout Component - Usage Guide

## Quick Copy/Paste

Add this HTML to any blog post to create a GitHub callout box:

```html
<div class="github-callout">
  <div class="github-callout-icon">📦</div>
  <div class="github-callout-content">
    <strong>Get the working code:</strong>
    <a href="https://github.com/dswann101164/YOUR-REPO-NAME" target="_blank" rel="noopener">GitHub Repository</a>
  </div>
</div>
```

## Variations

### Standard (Full Size)
```html
<div class="github-callout">
  <div class="github-callout-icon">📦</div>
  <div class="github-callout-content">
    <strong>Get the working code:</strong>
    <a href="https://github.com/dswann101164/azure-ipam" target="_blank" rel="noopener">Azure IPAM Tool on GitHub</a>
  </div>
</div>
```

### Compact Version (Smaller)
```html
<div class="github-callout compact">
  <div class="github-callout-icon">📦</div>
  <div class="github-callout-content">
    <strong>Code:</strong>
    <a href="https://github.com/dswann101164/workbook-modernizer" target="_blank" rel="noopener">GitHub</a>
  </div>
</div>
```

### Different Icons
You can swap the emoji for different contexts:
- 📦 - Default (packages/tools)
- 🔧 - Scripts/automation
- 📊 - Dashboards/workbooks
- 🚀 - Deployment tools
- 💾 - Data/templates
- ⚙️ - Configuration files

### With Description
```html
<div class="github-callout">
  <div class="github-callout-icon">🔧</div>
  <div class="github-callout-content">
    <strong>Get the complete PowerShell script with installation instructions:</strong>
    <a href="https://github.com/dswann101164/azure-vm-automation" target="_blank" rel="noopener">Azure VM Automation Scripts</a>
  </div>
</div>
```

## Where to Place

### Best Practices:
1. **After the introduction** - Right after you describe what the tool/script does
2. **Before code examples** - Let readers grab the full version before showing snippets
3. **At the end** - As a final call-to-action after the post

### Example Post Structure:
```markdown
---
title: "Azure IPAM Tool"
---

[Introduction paragraph about the problem]

<div class="github-callout">
  [GitHub callout here]
</div>

## The Problem

[Rest of your post with code examples]
```

## Styling Details

The component automatically:
- Uses Azure blue accent colors
- Has a subtle hover effect (lifts up slightly)
- Responsive (stacks nicely on mobile)
- High contrast for accessibility
- Matches your blog's design system

## Testing

After adding to a post:
1. Run `flask run`
2. Navigate to the post
3. Check that the callout displays properly
4. Test the hover effect
5. Click the link to verify it works

Then freeze and deploy:
```bash
python freeze.py
git add posts docs static
git commit -m "Add GitHub callout to [post name]"
git push
```
