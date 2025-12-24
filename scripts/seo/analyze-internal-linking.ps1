# Internal Linking Audit and Optimization
# Analyzes posts and suggests internal linking opportunities

$postsDir = ".\posts"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INTERNAL LINKING AUDIT" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Define topic clusters based on tags and content
$clusters = @{
    'FinOps' = @('cost', 'finops', 'pricing', 'chargeback', 'budget', 'billing')
    'KQL' = @('kql', 'query', 'resource graph', 'kusto')
    'Migration' = @('migration', 'migrate', 'assessment', 'cloud migration')
    'AI' = @('ai', 'openai', 'gpt', 'azure ai', 'foundry')
    'Arc' = @('arc', 'azure arc', 'hybrid', 'vmware')
    'Automation' = @('automation', 'logic apps', 'powershell', 'terraform', 'devops')
    'Governance' = @('governance', 'policy', 'tags', 'compliance', 'rbac')
    'Monitoring' = @('monitoring', 'workbook', 'dashboard', 'alert')
}

# High-ranking posts (positions 1-10) that should link TO lower-ranking posts
$highRankingPosts = @(
    '2025-12-09-azure-command-finder.md',
    '2025-11-25-azure-openai-pricing-real-costs.md',
    '2025-11-03-powershell-7-enterprise-migration.md',
    '2025-10-29-four-logic-apps-every-azure-admin-needs.md',
    '2025-09-23-kql-cheat-sheet-complete.md',
    '2025-12-08-50-linux-commands-azure.md'
)

# Load all posts
$allPosts = @{}
Get-ChildItem -Path $postsDir -Filter "*.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Extract front matter
    if ($content -match '(?s)^---\s*(.*?)\s*---') {
        $frontMatter = $matches[1]
        $tags = @()
        if ($frontMatter -match 'tags:\s*\[(.*?)\]') {
            $tags = $matches[1] -split ',' | ForEach-Object { $_.Trim().Trim('"') }
        }
        
        $title = ""
        if ($frontMatter -match 'title:\s*["'']?(.*?)["'']?\s*$') {
            $title = $matches[1]
        }
        
        $allPosts[$_.Name] = @{
            Title = $title
            Tags = $tags
            Content = $content
            File = $_.FullName
        }
    }
}

Write-Host "Loaded $($allPosts.Count) posts" -ForegroundColor Green
Write-Host ""

# Analyze each post and suggest internal links
$suggestions = @()

foreach ($postFile in $allPosts.Keys) {
    $post = $allPosts[$postFile]
    
    # Determine which cluster this post belongs to
    $postClusters = @()
    foreach ($clusterName in $clusters.Keys) {
        $keywords = $clusters[$clusterName]
        $match = $false
        foreach ($keyword in $keywords) {
            if ($post.Tags -join ' ' -match $keyword -or 
                $post.Title -match $keyword -or
                $postFile -match $keyword) {
                $match = $true
                break
            }
        }
        if ($match) {
            $postClusters += $clusterName
        }
    }
    
    if ($postClusters.Count -eq 0) {
        continue
    }
    
    # Check if this post already has internal links
    $existingLinks = ([regex]::Matches($post.Content, '\[.*?\]\(/blog/(.*?)\)')).Count
    
    # Find high-ranking posts in the same cluster to link FROM
    $linkOpportunities = @()
    foreach ($highPost in $highRankingPosts) {
        if ($highPost -eq $postFile) { continue }
        
        $highPostData = $allPosts[$highPost]
        if (-not $highPostData) { continue }
        
        # Check if high-ranking post is in same cluster
        foreach ($cluster in $postClusters) {
            $keywords = $clusters[$cluster]
            $match = $false
            foreach ($keyword in $keywords) {
                if ($highPostData.Tags -join ' ' -match $keyword -or
                    $highPostData.Title -match $keyword -or
                    $highPost -match $keyword) {
                    $match = $true
                    break
                }
            }
            
            if ($match) {
                # Check if link already exists
                $slug = $postFile -replace '^\d{4}-\d{2}-\d{2}-', '' -replace '\.md$', ''
                if ($highPostData.Content -notmatch $slug) {
                    $linkOpportunities += @{
                        FromPost = $highPost
                        FromTitle = $highPostData.Title
                        Cluster = $cluster
                        Slug = $slug
                    }
                }
            }
        }
    }
    
    if ($linkOpportunities.Count -gt 0) {
        $suggestions += [PSCustomObject]@{
            Post = $postFile
            Title = $post.Title
            Clusters = ($postClusters -join ', ')
            ExistingLinks = $existingLinks
            LinkOpportunities = $linkOpportunities
        }
    }
}

# Display suggestions
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "INTERNAL LINKING OPPORTUNITIES" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$totalOpportunities = 0
foreach ($suggestion in $suggestions | Sort-Object -Property { $_.LinkOpportunities.Count } -Descending) {
    Write-Host "Post: $($suggestion.Post)" -ForegroundColor Green
    Write-Host "Title: $($suggestion.Title)" -ForegroundColor White
    Write-Host "Clusters: $($suggestion.Clusters)" -ForegroundColor Gray
    Write-Host "Existing internal links: $($suggestion.ExistingLinks)" -ForegroundColor Gray
    Write-Host "Link opportunities: $($suggestion.LinkOpportunities.Count)" -ForegroundColor Yellow
    Write-Host ""
    
    foreach ($opp in $suggestion.LinkOpportunities) {
        $totalOpportunities++
        Write-Host "  FROM: $($opp.FromTitle)" -ForegroundColor Cyan
        Write-Host "  File: $($opp.FromPost)" -ForegroundColor Gray
        Write-Host "  Cluster: $($opp.Cluster)" -ForegroundColor Gray
        Write-Host "  Add link to: /blog/$($opp.Slug)" -ForegroundColor Yellow
        Write-Host "  Suggested anchor text: '$($suggestion.Title)'" -ForegroundColor White
        Write-Host "  Location: Add in 'Related Resources' or relevant section discussing $($opp.Cluster)" -ForegroundColor Gray
        Write-Host ""
    }
    Write-Host "---" -ForegroundColor DarkGray
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "SUMMARY" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Posts analyzed: $($allPosts.Count)" -ForegroundColor White
Write-Host "Posts with opportunities: $($suggestions.Count)" -ForegroundColor Yellow
Write-Host "Total linking opportunities: $totalOpportunities" -ForegroundColor Green
Write-Host ""
Write-Host "Expected impact: +10-20 clicks/month from improved internal linking" -ForegroundColor Green
Write-Host ""

# Export to CSV for easier review
$exportData = @()
foreach ($suggestion in $suggestions) {
    foreach ($opp in $suggestion.LinkOpportunities) {
        $exportData += [PSCustomObject]@{
            'Target Post' = $suggestion.Post
            'Target Title' = $suggestion.Title
            'From Post' = $opp.FromPost
            'From Title' = $opp.FromTitle
            'Cluster' = $opp.Cluster
            'Link URL' = "/blog/$($opp.Slug)"
            'Anchor Text' = $suggestion.Title
        }
    }
}

$exportData | Export-Csv "internal-linking-opportunities.csv" -NoTypeInformation
Write-Host "Detailed report saved to: internal-linking-opportunities.csv" -ForegroundColor Cyan
