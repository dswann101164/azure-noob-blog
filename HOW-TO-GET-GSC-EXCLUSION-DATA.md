# 📋 How to Get Detailed GSC Coverage Report

## What We Need

The detailed list of **328 "Not indexed" URLs** with their exclusion reasons.

---

## Step-by-Step Instructions

### Method 1: Via GSC Interface (Recommended)

1. **Go to Google Search Console**
   - https://search.google.com/search-console
   - Select azure-noob.com property

2. **Navigate to Pages Report**
   - Left sidebar → Click **"Pages"** (under Indexing)

3. **Scroll to "Why pages aren't indexed"**
   - You should see a section with reasons like:
     - Duplicate without user-selected canonical
     - Crawled - currently not indexed
     - Discovered - currently not indexed
     - Alternate page with proper canonical tag
     - Page with redirect
     - Not found (404)
     - etc.

4. **Click on Each Exclusion Reason**
   - Click on the first reason (e.g., "Duplicate without user-selected canonical")
   - You'll see a list of URLs with that issue
   - Click **"Export"** → **"Download"**
   - Repeat for each exclusion reason

5. **Upload All Downloaded Files**
   - You'll have multiple Excel/CSV files
   - Upload them all here

---

### Method 2: Via URL Inspection Tool (For Specific URLs)

If you want to check specific URLs:

1. **Copy a few sample URLs from your site**
   - Example: `https://azure-noob.com/blog/kql-cheat-sheet-complete/index.html`
   - Example: `https://azure-noob.com/blog/2025-01-15-kql-cheat-sheet-complete/`

2. **Use URL Inspection Tool**
   - Top search bar in GSC
   - Paste URL
   - Press Enter
   - See if it says "URL is on Google" or "URL is not on Google"
   - Note the reason

---

### Method 3: Check Your Sitemap Status

1. **Go to Sitemaps**
   - Left sidebar → **"Sitemaps"**
   - Look at `/sitemap.xml`
   - Check "Discovered URLs" vs "Indexed URLs"

2. **Common Issues:**
   - Discovered: 437
   - Indexed: 437
   - If "Discovered" > "Indexed", some sitemap URLs aren't indexing

---

## What I'm Looking For

**Specific patterns like:**

❌ **Duplicate URLs:**
- `/blog/post-name/` (indexed ✅)
- `/blog/post-name/index.html` (duplicate ❌)

❌ **Date-prefixed URLs:**
- `/blog/2025-01-15-post-name/` (redirect needed ❌)
- `/blog/post-name/` (indexed ✅)

❌ **Tag/Category pages:**
- `/tags/azure/page/2/` (low-quality ❌)
- `/tags/azure/` (indexed ✅)

❌ **404 errors:**
- Old URLs that should redirect

---

## Quick Visual Check

**In GSC → Pages, you should see something like:**

```
Why pages aren't indexed

Duplicate without canonical: 150 pages
Crawled - not indexed: 89 pages
Page with redirect: 45 pages
Discovered - not indexed: 30 pages
Not found (404): 14 pages
```

**I need:**
- Screenshot of this breakdown, OR
- Export of each category showing the URLs

---

## Alternative: Give Me Sample URLs

If GSC export is difficult, just copy-paste 20-30 URLs from each exclusion category.

Example format:
```
Duplicate without canonical:
- https://azure-noob.com/blog/post1/index.html
- https://azure-noob.com/blog/post2/index.html
...

Crawled - not indexed:
- https://azure-noob.com/tags/azure/page/2/
- https://azure-noob.com/tags/governance/page/3/
...
```

---

## Why This Matters

328 "not indexed" pages = Google is confused about your URL structure.

**Possible issues:**
1. Duplicate content (index.html versions)
2. Pagination pages (tag/page/2/)
3. Old URLs with redirects not working
4. Low-quality auto-generated pages

**Once I see the URLs, I can:**
1. Identify the patterns
2. Fix redirects in app.py
3. Update sitemap.xml
4. Add canonical tags where needed
5. Add noindex to low-quality pages

---

## Next Steps

1. Go to GSC → Pages → "Why pages aren't indexed"
2. Click each exclusion reason
3. Export and upload all files

**Or:** 

Take a screenshot of the "Why pages aren't indexed" section showing the counts for each reason, and I'll tell you which ones to investigate first.
