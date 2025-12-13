# BATCH INTERNAL LINKING FIX SCRIPT
# This adds hub links and related_posts to all posts with 0 internal links

$hubTemplates = @{
    'finops' = 'This guide is part of our [Azure FinOps hub](/hub/finops/) covering cost management, chargeback models, and financial operations at enterprise scale.'
    'kql' = 'This guide is part of our [KQL Mastery hub](/hub/kql/) covering query patterns, optimization techniques, and real-world Azure Resource Graph examples.'
    'governance' = 'This guide is part of our [Azure Governance hub](/hub/governance/) covering policy enforcement, compliance frameworks, and enterprise controls.'
    'migration' = 'This guide is part of our [Azure Migration hub](/hub/migration/) covering assessment, planning, execution, and post-migration optimization.'
    'monitoring' = 'This guide is part of our [Azure Monitoring hub](/hub/monitoring/) covering workbooks, alerting, and operational visibility.'
    'automation' = 'This guide is part of our [Azure Automation hub](/hub/automation/) covering Infrastructure as Code, CI/CD pipelines, and DevOps practices.'
    'ai' = 'This guide is part of our [AI-Assisted Azure Operations hub](/hub/ai/) exploring how AI tools transform cloud administration and productivity workflows.'
}

# Manual fix list (filename|hub|insert_after_text|related_posts)
$fixes = @"
2025-10-31-azure-tag-governance-policy.md|governance|**The problem:** Nobody talks about tag governance enforcement until it's too late.|azure-resource-tags-guide,tag-governance-247-variations,azure-costs-apps-not-subscriptions,azure-finops-complete-guide
2025-11-03-powershell-7-enterprise-migration.md|automation|PowerShell 7 isn't just an upgrade - it's a migration project.|if-you-cant-code-your-architecture,terraform-azure-devops-cicd-series-index,software-rationalization-step-zero-devops
2025-11-03-linux-commands-azure-admin-career.md|automation|Linux proficiency is now table stakes for Azure administrators.|powershell-7-enterprise-migration,azure-osi-model-for-admins,50-linux-commands-azure
2025-11-04-software-rationalization-step-zero-devops.md|governance|Before you implement DevOps, you need to know what software you have.|terraform-azure-devops-cicd-series-index,if-you-cant-code-your-architecture,cloud-migration-reality-check
2025-11-08-terraform-azure-devops-cicd-part6-troubleshooting.md|automation|Troubleshooting Terraform pipelines requires understanding both Terraform and Azure DevOps.|terraform-azure-devops-cicd-series-index,terraform-remote-state-azure,if-you-cant-code-your-architecture
2025-11-09-buzzwords-meetings-confusion.md|governance|Buzzwords create communication gaps in enterprise IT.|software-rationalization-step-zero-devops,three-ai-roles,azure-landing-zone-reality-check
2025-11-10-only-1-percent-know-these-tools.md|automation|Most Azure admins don't know these tools exist.|azure-service-inventory-tool,azure-ipam-tool,workbook-app-tool,pbix-modernizer-tool
2025-11-10-pull-meta-from-arm.md|automation|ARM templates contain metadata that's hard to extract programmatically.|azure-service-inventory-tool,terraform-remote-state-azure,if-you-cant-code-your-architecture
2025-11-14-application-migration-checklist-azure.md|migration|Application migration requires more than just lifting and shifting VMs.|cloud-migration-reality-check,azure-migrate-enterprise-hybrid,azure-migration-roi-wrong,azure-hybrid-benefit-complete
2025-11-16-terraform-remote-state-azure.md|automation|Remote state management is the difference between Terraform working and Terraform chaos.|terraform-azure-devops-cicd-series-index,if-you-cant-code-your-architecture,azure-landing-zone-reality-check
2025-10-28-azure-ai-collaboration-gap.md|ai|AI tools close the collaboration gap between technical and non-technical teams.|azure-debugging-ai-rule,three-ai-roles,will-ai-replace-azure-administrators-by-2030,the-ai-admin
2025-10-28-migrating-my-avd-win10-to-win11-512gb.md|automation|AVD migration from Windows 10 to 11 isn't straightforward.|cloud-migration-reality-check,azure-migrate-enterprise-hybrid,application-migration-checklist-azure
2025-10-29-four-logic-apps-every-azure-admin-needs.md|automation|Logic Apps automate the repetitive tasks Azure admins hate.|azure-service-inventory-tool,workbook-app-tool,if-you-cant-code-your-architecture
2025-10-29-azure-icons-reference.md|automation|Azure icons change constantly - this reference stays current.|azure-service-inventory-tool,azure-periodic-table-service-dictionary,azure-dashboards-cloud-noc
2025-10-29-azure-service-inventory-tool.md|automation|Service inventory tools prevent zombie resources from costing money.|only-1-percent-know-these-tools,azure-ipam-tool,workbook-app-tool,azure-cost-optimization-what-actually-works
2025-11-03-azure-cost-optimization-facade.md|finops|Cost optimization theater looks good in presentations but doesn't save money.|azure-cost-optimization-what-actually-works,azure-finops-complete-guide,azure-chargeback-tags-model,chris-bowman-dashboard
2025-11-03-azure-osi-model-for-admins.md|automation|The OSI model explains Azure networking better than Microsoft docs.|private-endpoint-dns-hybrid-ad,azure-landing-zone-reality-check,linux-commands-azure-admin-career
"@

$fixLines = $fixes -split "`n" | Where-Object { $_ -match '\S' }
$postsDir = "C:\Users\dswann\Documents\GitHub\azure-noob-blog\posts"

Write-Host "Starting batch fix of $($fixLines.Count) posts..." -ForegroundColor Cyan
$fixed = 0
$errors = 0

foreach ($line in $fixLines) {
    $parts = $line -split '\|'
    $filename = $parts[0].Trim()
    $hub = $parts[1].Trim()
    $insertAfter = $parts[2].Trim()
    $relatedPosts = $parts[3].Trim() -split ','
    
    $filepath = Join-Path $postsDir $filename
    
    if (-not (Test-Path $filepath)) {
        Write-Host "  SKIP: $filename (not found)" -ForegroundColor Yellow
        continue
    }
    
    try {
        $content = Get-Content $filepath -Raw -Encoding UTF8
        
        # Check if already has hub link
        if ($content -match '/hub/') {
            Write-Host "  SKIP: $filename (already has hub link)" -ForegroundColor Gray
            continue
        }
        
        # Extract frontmatter and body
        if ($content -match '(?s)^---\s*\n(.*?)\n---\s*\n(.*)$') {
            $frontmatter = $Matches[1]
            $body = $Matches[2]
            
            # Add hub to frontmatter if not present
            if ($frontmatter -notmatch "^hub:", "Multiline") {
                $frontmatter += "`nhub: $hub"
            }
            
            # Add related_posts if not present
            if ($frontmatter -notmatch "related_posts:", "Multiline") {
                $frontmatter += "`nrelated_posts:"
                foreach ($post in $relatedPosts) {
                    $frontmatter += "`n  - $($post.Trim())"
                }
            }
            
            # Add hub link to body after specified text
            $hubLink = $hubTemplates[$hub]
            if ($body -match [regex]::Escape($insertAfter)) {
                $body = $body -replace [regex]::Escape($insertAfter), "$insertAfter`n`n$hubLink`n"
            } else {
                # If can't find exact text, add after first paragraph
                $body = $body -replace '(^.+?\n\n)', "`$1`n$hubLink`n`n"
            }
            
            # Rebuild file
            $newContent = "---`n$frontmatter`n---`n$body"
            
            # Save
            Set-Content -Path $filepath -Value $newContent -Encoding UTF8 -NoNewline
            
            Write-Host "  FIXED: $filename" -ForegroundColor Green
            $fixed++
            
        } else {
            Write-Host "  ERROR: $filename (couldn't parse frontmatter)" -ForegroundColor Red
            $errors++
        }
        
    } catch {
        Write-Host "  ERROR: $filename - $_" -ForegroundColor Red
        $errors++
    }
}

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "SUMMARY:" -ForegroundColor Yellow
Write-Host "  Fixed: $fixed posts" -ForegroundColor Green
Write-Host "  Errors: $errors posts" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Cyan
