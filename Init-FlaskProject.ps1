<#
Creates a ready-to-run Flask project with:
- .venv (Python virtual env)
- app.py with 2 routes (/ and /about)
- templates/ (base.html, index.html, about.html)
- static/styles.css
- requirements.txt (flask)
- .vscode/launch.json for F5 debugging in VS Code
- run.ps1 convenience launcher
Run this script from the intended project root folder.
#>

$ErrorActionPreference = "Stop"

function Ensure-Python {
  if (Get-Command python -ErrorAction SilentlyContinue) { return }
  if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    throw "Python not found and winget is unavailable. Install Python 3.12+ from python.org, then re-run."
  }
  Write-Host "Installing Python via winget..."
  winget install -e --id Python.Python.3.12 --accept-package-agreements --accept-source-agreements
  # refresh PATH for current session
  $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" +
              [System.Environment]::GetEnvironmentVariable("Path","User")
  if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw "Python still not found after install. Close & reopen PowerShell and run the script again."
  }
}

function Ensure-Folder([string]$p) {
  if (-not (Test-Path $p)) { New-Item -ItemType Directory -Path $p | Out-Null }
}

Write-Host "Project root: $(Get-Location)"

# 0) Python
Ensure-Python
python --version | Write-Host
python -m pip --version | Write-Host

# 1) venv
if (-not (Test-Path ".\.venv")) {
  Write-Host "Creating virtual environment .venv ..."
  python -m venv .venv
}
# allow activation for this session only
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
. .\.venv\Scripts\Activate.ps1

# 2) deps
if (-not (Test-Path ".\requirements.txt")) {
  "flask" | Out-File -Encoding ascii ".\requirements.txt"
}
Write-Host "Installing Python packages ..."
pip install -r ".\requirements.txt"

# 3) folders
Ensure-Folder ".\templates"
Ensure-Folder ".\static"
Ensure-Folder ".\.vscode"

# 4) files
$appPy = @'
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    # renders templates/index.html (extends base.html)
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    # Dev server only; use a real WSGI server for production
    app.run(debug=True)  # http://127.0.0.1:5000
'@

$baseHtml = @'
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{% block title %}FullofIT Local{% endblock %}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="{{ url_for('static', filename='styles.css') }}" rel="stylesheet">
</head>
<body>
  <header class="site-header">
    <nav class="nav">
      <a href="{{ url_for('home') if 'home' in globals() else '/' }}">Home</a>
      <a href="{{ url_for('about') }}">About</a>
    </nav>
  </header>
  <main class="container">
    {% block content %}{% endblock %}
  </main>
  <footer class="site-footer">
    <small>© {{  (now() | default('') )  }} FullofIT (dev)</small>
  </footer>
</body>
</html>
'@

$indexHtml = @'
{% extends "base.html" %}
{% block title %}Home · FullofIT Local{% endblock %}
{% block content %}
<h1>It works 🎉</h1>
<p>This Flask app is running locally. Edit <code>templates/index.html</code> and <code>static/styles.css</code> to see live changes.</p>
{% endblock %}
'@

$aboutHtml = @'
{% extends "base.html" %}
{% block title %}About · FullofIT Local{% endblock %}
{% block content %}
<h1>About</h1>
<p>Starter Flask structure with a base template, simple CSS, and VS Code debugging.</p>
{% endblock %}
'@

$stylesCss = @'
:root { --fg:#111; --muted:#666; --bg:#fff; --accent:#0a7; }
* { box-sizing: border-box }
body { margin:0; font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial; color:var(--fg); background:var(--bg); }
.container { max-width: 880px; margin: 2.5rem auto; padding: 0 1rem; line-height: 1.6; }
h1 { margin: 0 0 .75rem; }
.nav { display:flex; gap:1rem; padding: .75rem 1rem; background:#f6f6f6; border-bottom:1px solid #eee; }
.nav a { text-decoration:none; color:var(--fg); padding:.25rem .5rem; border-radius:.5rem; }
.nav a:hover { background: #eaf7f3; color: var(--accent); }
.site-footer { border-top:1px solid #eee; padding:1rem; text-align:center; color:var(--muted); }
code { background:#f2f2f2; padding:.15rem .35rem; border-radius:.3rem; }
'@

$launchJson = @'
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Flask: app.py (Debug)",
      "type": "python",
      "request": "launch",
      "program": "${workspaceFolder}/app.py",
      "console": "integratedTerminal",
      "justMyCode": true
    }
  ]
}
'@

$runPs1 = @'
# Activate venv and run Flask dev server
param([int]$Port = 5000)
Set-ExecutionPolicy -Scope Process Bypass -Force
. .\.venv\Scripts\Activate.ps1
$env:FLASK_ENV="development"
python app.py
'@

if (-not (Test-Path ".\app.py"))                { $appPy     | Out-File -Encoding utf8 ".\app.py" }
if (-not (Test-Path ".\templates\base.html"))   { $baseHtml  | Out-File -Encoding utf8 ".\templates\base.html" }
if (-not (Test-Path ".\templates\index.html"))  { $indexHtml | Out-File -Encoding utf8 ".\templates\index.html" }
if (-not (Test-Path ".\templates\about.html"))  { $aboutHtml | Out-File -Encoding utf8 ".\templates\about.html" }
if (-not (Test-Path ".\static\styles.css"))     { $stylesCss | Out-File -Encoding utf8 ".\static\styles.css" }
if (-not (Test-Path ".\.vscode\launch.json"))   { $launchJson| Out-File -Encoding utf8 ".\.vscode\launch.json" }
$runPs1 | Out-File -Encoding utf8 ".\run.ps1"

Write-Host "`nAll set ✅"
Write-Host "Next steps:"
Write-Host "  1) .\.venv\Scripts\Activate.ps1"
Write-Host "  2) python app.py   (or press F5 in VS Code)"
Write-Host "  3) Ope
