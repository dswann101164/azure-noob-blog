# SEO Automation Setup Guide

## Files Created

✓ `scripts/validate-seo.py` - SEO validation script
✓ `scripts/publish-post.ps1` - New publishing workflow
✓ `.github/workflows/auto-index.yml` - Google Indexing API automation

## Quick Setup (30 minutes)

### 1. Install PyYAML (2 minutes)

```powershell
.\.venv\Scripts\pip.exe install pyyaml
```

### 2. Test SEO Validator (2 minutes)

```powershell
.\.venv\Scripts\python.exe .\scripts\validate-seo.py
```

This will scan all your posts and report any SEO issues. Common issues:
- Missing `summary` field
- Title too long (>60 chars)
- Not enough tags (<3)
- Missing cover image

Fix any issues it finds in your markdown files.

### 3. Test Publishing Script (2 minutes)

```powershell
# Dry run - just freeze, don't commit
.\.venv\Scripts\python.exe .\freeze.py

# Full test (make sure you have something to commit first)
.\scripts\publish-post.ps1
```

### 4. Setup Google Indexing API (20 minutes)

#### Step A: Google Cloud Console

1. Go to https://console.cloud.google.com
2. Create new project: "azure-noob-indexing"
3. Enable "Indexing API":
   - Search for "Indexing API" in APIs & Services
   - Click "Enable"
4. Create Service Account:
   - IAM & Admin → Service Accounts
   - Create Service Account: "github-indexer"
   - Grant role: "Owner"
   - Actions → Manage Keys → Add Key → Create new key → JSON
   - Download the JSON file (keep it safe!)

#### Step B: Google Search Console

1. Go to https://search.google.com/search-console
2. Select azure-noob.com property
3. Settings → Users and permissions
4. Add user: Paste the service account email from the JSON file
   - Format: `github-indexer@azure-noob-indexing.iam.gserviceaccount.com`
   - Permission: "Owner"
5. Click "Add"

#### Step C: GitHub Secrets

1. Open the JSON file you downloaded
2. Copy the ENTIRE contents
3. Go to your GitHub repo
4. Settings → Secrets and variables → Actions
5. Click "New repository secret"
6. Name: `GOOGLE_INDEXING_CREDENTIALS`
7. Value: Paste the entire JSON contents
8. Click "Add secret"

### 5. Test the Workflow (5 minutes)

```powershell
# Make a tiny edit to any post (add a space somewhere)
# Publish it
.\scripts\publish-post.ps1

# Wait 30 seconds, then check:
# 1. GitHub → Actions tab → should see "Auto-Index New Posts in Google" running
# 2. Green checkmark = success
# 3. Click on the workflow run to see which URLs were submitted
```

Within 10 minutes, check Google Search Console:
- URL Inspection tool
- Enter your post URL
- Should see "URL submitted via Indexing API"

## Your New Workflow

```powershell
# Write post in VSCode at 3:30 AM
# Save hero image to static/images/hero/

# Publish (does everything automatically)
.\scripts\publish-post.ps1

# Tweet the link
# Done!
```

## What Happens Automatically

1. ✓ SEO validation (catches issues before publishing)
2. ✓ Site freeze (regenerates docs/)
3. ✓ Git commit with smart message
4. ✓ Git push
5. ✓ GitHub Actions triggers
6. ✓ Google gets notified of new URL
7. ✓ Indexing happens within 1-24 hours

## Troubleshooting

**SEO validation fails:**
- Read the output - it tells you exactly what's wrong
- Fix the issues in your markdown frontmatter
- Or skip validation: `.\scripts\publish-post.ps1 -SkipValidation`

**Google Indexing workflow fails:**
- Check GitHub Actions logs for error details
- Most common issue: Service account not added to Search Console
- Verify the secret is named exactly: `GOOGLE_INDEXING_CREDENTIALS`

**Script not found errors:**
- Make sure you're running from the repo root: `C:\Users\dswann\Documents\GitHub\azure-noob-blog`
- Use `.\scripts\publish-post.ps1` not just `publish-post.ps1`

## Cost

- PyYAML: Free
- SEO validation: Free
- Google Indexing API: Free (200 URLs/day limit)
- GitHub Actions: Free (2000 minutes/month)

**Total: $0/month**

## Next Steps After 30 Days

Once you have data:
1. Analyze which posts rank fastest
2. Identify high-performing tags
3. Add internal linking suggestions
4. Build weekly ranking reports

But first - get this core automation working!
