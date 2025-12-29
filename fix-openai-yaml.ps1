# SAFE FIX - Manually edit the YAML without regex
$postPath = "posts\2025-11-25-azure-openai-pricing-real-costs.md"

Write-Host "`n🔧 FIXING AZURE OPENAI POST (SAFE VERSION)`n" -ForegroundColor Cyan

# Read the file
$lines = Get-Content $postPath

# Find where YAML ends
$yamlEnd = 0
for ($i = 1; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq "---") {
        $yamlEnd = $i
        break
    }
}

# Extract YAML and content
$yaml = $lines[0..$yamlEnd]
$content = $lines[($yamlEnd + 1)..($lines.Count - 1)]

# Build new YAML
$newYaml = @"
---
title: "Azure OpenAI Pricing 2025: GPT-4o Token Cost Table & Calculator (Updated Dec 2025)"
date: 2025-11-25
modified: 2025-12-29
summary: "Complete Azure OpenAI pricing table for Dec 2025: GPT-4o (`$0.005/1K input), GPT-4 Turbo (`$0.01/1K), GPT-3.5 (`$0.002/1K). Includes cost calculator, hidden fine-tuning fees (`$1,836/month), token comparison table, and production cost examples from enterprise deployments."
tags:
- Azure
- FinOps
- AI
- OpenAI
- Cost Management
cover: /static/images/hero/azure-openai-costs.png
slug: azure-openai-pricing-real-costs
hub: finops
related_posts:
  - azure-finops-complete-guide
  - azure-cost-optimization-complete-guide
  - azure-resource-tags-guide
faq_schema: true
---
"@

# Combine and save
$newContent = $newYaml + "`n" + ($content -join "`n")
Set-Content $postPath $newContent -NoNewline

Write-Host "✅ YAML fixed!`n" -ForegroundColor Green

# Test with Python
Write-Host "🧪 Testing YAML parsing..." -ForegroundColor Yellow
python -c "import yaml; yaml.safe_load(open('$postPath').read().split('---')[1]); print('✅ YAML is valid!')"

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ YAML VALIDATED! Safe to freeze.`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ YAML still broken. Manual fix needed.`n" -ForegroundColor Red
    exit 1
}

# Freeze
Write-Host "🧊 Freezing site..." -ForegroundColor Yellow
python freeze.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ FREEZE SUCCESSFUL!`n" -ForegroundColor Green
    
    # Commit
    git add posts/ docs/
    git commit -m "feat(seo): Gemini fix - Data-heavy Azure OpenAI title

PROBLEM: Position 5.76 but 0 clicks from 5,068 impressions
FIX: More data-heavy title with 'Table & Calculator (Updated Dec 2025)'
CHANGES: Title + Summary lead with specific prices
EXPECTED: CTR 0% -> 2.5-3.5% = 127-178 clicks/month"
    
    git push origin main
    
    Write-Host "`n✅ DEPLOYED!`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ FREEZE FAILED`n" -ForegroundColor Red
}
