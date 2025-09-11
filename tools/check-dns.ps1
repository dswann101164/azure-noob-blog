# check-dns.ps1
$domainRoot = "azure-noob.com"
$domainWWW  = "www.azure-noob.com"

# GitHub Pages IPs
$githubIPs = @("185.199.108.153","185.199.109.153","185.199.110.153","185.199.111.153")

Write-Host "🔎 Checking DNS for $domainRoot and $domainWWW"
Write-Host "Looking for GitHub Pages IPs: $($githubIPs -join ', ')"
Write-Host "Press Ctrl+C to stop.`n"

while ($true) {
  $ts = Get-Date -Format 'HH:mm:ss'
  Write-Host "[$ts]"

  # ROOT (@) -> A records
  $rootA = (Resolve-DnsName -Type A $domainRoot -ErrorAction SilentlyContinue |
            Where-Object { $_.QueryType -eq 'A' }).IPAddress
  if ($rootA) {
    Write-Host " $domainRoot (A) → $($rootA -join ', ')"
    if ($rootA | Where-Object { $_ -in $githubIPs }) {
      Write-Host "   ✅ Root points to GitHub Pages" -ForegroundColor Green
    } else {
      Write-Host "   ⚠️ Root not on GitHub yet" -ForegroundColor Yellow
    }
  } else {
    Write-Host " $domainRoot (A) → ❌ no record" -ForegroundColor Red
  }

  # WWW -> prefer CNAME, fallback to A
  $wwwCNAME = (Resolve-DnsName -Type CNAME $domainWWW -ErrorAction SilentlyContinue |
               Select-Object -First 1).NameHost
  if ($wwwCNAME) {
    Write-Host " $domainWWW (CNAME) → $wwwCNAME"
    if ($wwwCNAME -like "*.github.io.") {
      Write-Host "   ✅ www CNAME points to GitHub Pages" -ForegroundColor Green
    } else {
      Write-Host "   ⚠️ www CNAME not pointing to GitHub" -ForegroundColor Yellow
    }
  } else {
    $wwwA = (Resolve-DnsName -Type A $domainWWW -ErrorAction SilentlyContinue |
             Where-Object { $_.QueryType -eq 'A' }).IPAddress
    if ($wwwA) {
      Write-Host " $domainWWW (A) → $($wwwA -join ', ')"
      if ($wwwA | Where-Object { $_ -in $githubIPs }) {
        Write-Host "   ✅ www A points to GitHub Pages" -ForegroundColor Green
      } else {
        Write-Host "   ⚠️ www A not on GitHub yet" -ForegroundColor Yellow
      }
    } else {
      Write-Host " $domainWWW → ❌ no CNAME/A record" -ForegroundColor Red
    }
  }

  Write-Host ""
  Start-Sleep -Seconds 300   # 5 minutes
}
