# Google Search Console Indexing Issues - Diagnostic & Fix Toolkit

Your GSC report shows **361 pages blocked from indexing** (46% of discovered pages). This toolkit helps you identify and fix these issues systematically.

## 📊 Current State (Jan 10, 2026)

- **Total pages**: 868 (421 indexed, 447 not indexed)
- **Impressions**: Growing explosively (4,200+ weekly, up 525x since October)
- **Critical Issues**:
  - 212 pages with redirect ← **PRIORITY 1** (58% of blocked pages)
  - 79 pages 404 ← **PRIORITY 2** (22% of blocked pages)
  - 86 pages with noindex tag
  - 50 pages with canonical alternate
  - 19 pages crawled but not indexed

## 🛠️ Toolkit Components

### 1. Site Diagnostic Tool
**File**: `diagnose-gsc-issues.py`  
**Usage**: `.\run-gsc-diagnostic.ps1`

Analyzes your frozen site (`docs/`) to detect:
- Noindex tags
- Meta refresh redirects
- Canonical tag mismatches
- Pages missing from sitemap
- Thin content (<300 words)

**Run this first** to understand what's happening in your actual HTML files.

### 2. Redirect Analyzer
**File**: `analyze-gsc-redirects.py`  
**Requires**: Export from GSC

How to use:
1. Go to GSC → Indexing → Pages
2. Filter: "Page with redirect"
3. Export data (top right button)
4. Save as `gsc-redirects.csv` in blog root
5. Run: `python analyze-gsc-redirects.py`

This will:
- Categorize redirect types
- Identify date-prefixed URLs
- Generate redirect rules for `app.py`
- Show which redirects are already handled

### 3. 404 Analyzer
**File**: `analyze-gsc-404s.py`  
**Requires**: Export from GSC

How to use:
1. Go to GSC → Indexing → Pages
2. Filter: "Not found (404)"
3. Export data
4. Save as `gsc-404s.csv` in blog root
5. Run: `python analyze-gsc-404s.py`

This will:
- Find similar live URLs (fuzzy matching)
- Detect WordPress artifacts (safe to ignore)
- Identify typos/old slugs that need redirects
- Generate redirect rules for `app.py`

## 🎯 Recommended Fix Sequence

### Step 1: Run Diagnostic (5 minutes)
```powershell
.\run-gsc-diagnostic.ps1
```

This shows what's actually in your frozen site. Most issues should be clean.

### Step 2: Export GSC Data (10 minutes)
Export both:
- "Page with redirect" → `gsc-redirects.csv`
- "Not found (404)" → `gsc-404s.csv`

### Step 3: Analyze Redirects (5 minutes)
```bash
python analyze-gsc-redirects.py
```

Look for patterns. Most should be:
- HTTP → HTTPS (already handled)
- Date-prefixed URLs (already handled)
- Old slugs (need manual redirects)

### Step 4: Analyze 404s (10 minutes)
```bash
python analyze-gsc-404s.py
```

This finds broken links and suggests fixes. Common causes:
- Old post slugs that changed
- Typos in external links
- WordPress remnants (if you migrated)

### Step 5: Add Strategic Redirects (15 minutes)

Edit `app.py`, find the `strategic_redirects` dictionary, and add:

```python
strategic_redirects = {
    # Existing redirects
    '/azure-openai-pricing/': '/blog/azure-openai-pricing-real-costs/',
    
    # Add new redirects here
    '/old-slug/': '/blog/new-slug/',
    '/blog/typo-version/': '/blog/correct-version/',
}
```

### Step 6: Freeze & Deploy (5 minutes)
```powershell
python freeze.py
git add .
git commit -m "fix: add strategic redirects for GSC 404s and redirects"
git push
```

### Step 7: Request Re-indexing (15 minutes)
1. Go to GSC → Sitemaps
2. Remove old sitemap
3. Submit updated sitemap
4. Wait 24-48 hours for Google to re-crawl

### Step 8: Remove Dead URLs (optional, 30 minutes)
For URLs that will never exist:
1. GSC → Removals
2. Temporarily remove URL
3. Add each dead URL
4. Google will drop them from index within 24 hours

## 📈 Expected Results

After fixes:
- **Week 1**: Google re-crawls updated sitemap
- **Week 2**: Redirect count drops by 50-70%
- **Week 3**: 404 count drops to <20
- **Week 4**: Indexed pages increase by 100-150

Your impressions should continue climbing as Google indexes more pages correctly.

## 🔍 Why This Matters

**Current state**: 361 blocked pages = wasted crawl budget  
**After fixes**: Those pages get indexed = more search visibility  
**Impact**: Your 4,200 weekly impressions could jump to 6,000-8,000

The issues aren't breaking your site - your indexed pages are performing great (525x impression growth). But fixing these unlocks the other 46% of your content.

## 💡 Technical Explanation

### Why are there redirects?

Your `app.py` has these redirect rules:
```python
@app.before_request
def handle_trailing_slashes_and_redirects():
    # Force HTTPS
    # Force non-WWW
    # Add trailing slashes
    # Redirect date-prefixed URLs
```

These are CORRECT for users, but Google sees them as "redirects" in the index. The problem isn't your code - it's that Google has OLD URLs in its index that trigger these redirects.

### Why are there 404s?

Common causes:
1. Old external links pointing to URLs that changed
2. Typos in links from other sites
3. Google cached old URLs before you changed post slugs
4. WordPress remnants if you migrated from WordPress

### Why the noindex tags?

Likely intentional on pages like:
- `/thank-you/` (conversion tracking)
- `/search/` (duplicate content)
- Product download pages

This is CORRECT - keep those noindexed.

## 📞 Need Help?

If the analyzers find something unexpected:
1. Check the output carefully
2. Look at the actual HTML in `docs/`
3. Compare to live site behavior
4. Review `app.py` redirect logic

The most likely outcome: **212 redirects = old URLs Google cached, 79 404s = external broken links**. Both fix themselves over time, but you can speed it up with strategic redirects and URL removals.

---

**Bottom line**: Your site's healthy. This is cleanup work to maximize the indexing of your growing content library. Run the diagnostic first, then decide if the fixes are worth the time investment.
