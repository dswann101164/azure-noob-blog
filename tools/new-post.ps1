param(
  [Parameter(Mandatory=$true)][string]$Title,
  [string]$Slug = $null
)

$today = Get-Date -Format 'yyyy-MM-dd'
if(-not $Slug){
  $Slug = ($Title.ToLower() -replace '[^a-z0-9]+','-').Trim('-')
}
# Absolute path: [IO.File] resolves relative paths against the process directory, not $PWD
$path = Join-Path (Get-Location).Path "posts\$today-$Slug.md"

$front = @"
---
title: "$Title"
date: $today
slug: $Slug
description: ""
tags: [azure]
cover: /static/images/logo.png
---
# $Title

Write your intro here…
"@

# UTF-8 without BOM (Set-Content -Encoding UTF8 adds a BOM in PS 5.1, which breaks front matter)
$utf8NoBom = New-Object System.Text.UTF8Encoding $false
[System.IO.File]::WriteAllText($path, $front, $utf8NoBom)
Write-Host "Created $path"
