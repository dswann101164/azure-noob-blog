param(
  [Parameter(Mandatory=$true)][string]$Title,     # e.g. 'My First Azure VM'
  [string]$Slug = $null
)

$today = Get-Date -Format 'yyyy-MM-dd'
if(-not $Slug){
  $Slug = ($Title.ToLower() -replace '[^a-z0-9]+','-').Trim('-')
}
$path = ".\posts\$today-$Slug.md"

$front = @"
---
title: "$Title"
date: $today
slug: $Slug
description: ""
tags: [azure]
cover: /static/images/logo.png
---
"@

Set-Content $path $front -Encoding UTF8
Write-Host "Created $path"
