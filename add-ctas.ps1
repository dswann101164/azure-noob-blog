# ADD CTAs TO TOP BLOG POSTS
# This PowerShell script adds product CTAs to your top-performing posts

$CTA = @"

---

## 🎯 Ready for Production-Ready Queries?

This guide covers the basics, but **scaling to 30,000+ resources requires battle-tested patterns.**

**The Complete KQL Query Library includes:**
- ✅ 48 copy-paste ready queries (VMs, networking, security, cost)
- ✅ Advanced joins (VMs → NICs → Disks → Subnets → Subscriptions)
- ✅ Enterprise-scale tested on 31,000+ resources
- ✅ Performance optimization for massive environments
- ✅ SQL to KQL translation guide
- ✅ Lifetime updates

**Launch price: `$19** (regular `$29)

[Get the Complete KQL Library →](https://davidnoob.gumroad.com/l/hooih)

---
"@

$posts = @(
    "2025-12-10-azure-finops-complete-guide.md",
    "2025-09-23-azure-vm-inventory-kql.md",
    "2025-12-06-azure-arc-ghost-registrations.md",
    "2025-12-08-50-windows-commands-azure.md",
    "2025-12-08-50-linux-commands-azure.md",
    "2025-10-28-kql-query-library-git.md",
    "2025-11-03-azure-cost-optimization-complete-guide.md",
    "2025-12-11-azure-hybrid-benefit-complete.md"
)

foreach ($post in $posts) {
    $filepath = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts\$post"
    
    if (Test-Path $filepath) {
        # Read the file
        $content = Get-Content $filepath -Raw
        
        # Check if CTA already exists
        if ($content -notmatch "Complete KQL Query Library") {
            # Add CTA before the last line
            $content = $content.TrimEnd() + "`n" + $CTA
            
            # Write back
            Set-Content $filepath $content -NoNewline
            
            Write-Host "✅ Added CTA to $post" -ForegroundColor Green
        } else {
            Write-Host "⏭️  Skipped $post (CTA already exists)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ File not found: $post" -ForegroundColor Red
    }
}

Write-Host "`n✅ DONE! CTAs added to 8 blog posts" -ForegroundColor Green
Write-Host "Now run: python freeze.py && git add . && git commit -m 'Add product CTAs to top posts' && git push"
