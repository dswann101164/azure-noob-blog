# FullofIT Blog — Workflow Cheat Sheet

## TL;DR (every time)
```powershell
# local preview
preview        # add -Port 5051 -Open if you like

# publish to GitHub Pages
publish
Prereqs (one-time per machine)
powershell
Copy code
cd "C:\Local Sites\fullofitlocal"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt  # flask, frozen-flask, markdown, pygments, pyyaml
Set aliases (already done):

powershell
Copy code
notepad $PROFILE
# Add:
# Set-Alias preview  "C:\Local Sites\fullofitlocal\tools\preview.ps1"
# Set-Alias publish  "C:\Local Sites\fullofitlocal\tools\publish-post.ps1"
. $PROFILE
Daily loop
1) Write/edit a post
Add/edit files in posts/*.md

Front matter keys supported: slug, title, date, summary, tags, cover

2) Preview locally
powershell
Copy code
preview                 # default: http://127.0.0.1:5050
# options:
preview -Open           # opens your browser
preview -Port 5051      # runs on 5051
preview -BindHost localhost -Port 5050 -Open
Check:

http://127.0.0.1:5050/

http://127.0.0.1:5050/search/

http://127.0.0.1:5050/healthz → {"ok": true, "posts": N}

3) Publish
powershell
Copy code
publish
This will:

Freeze site into docs/

Commit changes (source + docs)

Rebase onto origin/main

Push (triggers GitHub Pages)

Verify:

https://azure-noob.com/

https://azure-noob.com/search/ (hard refresh or add ?v=1)

Common tasks
New post (quick scaffold)
Create posts/my-new-post.md:

md
Copy code
---
title: My New Post
date: 2025-09-13
summary: One-liner about this post.
tags: [azure, howto]
cover: optional-image.png
---

# My New Post

Content here…
Add a hero/cover image
Put file at static/images/hero/<filename>

Set cover: <filename> in front matter

Troubleshooting (fast)
Server starts then “exits”
PowerShell shows a dev warning as an error. Our preview.ps1 already ignores it. Use preview (not python app.py) to run.

Can’t connect to 5050
Try another port:

powershell
Copy code
preview -Port 5051 -Open
ImportError: No module named ...
Make sure venv is active and install:

powershell
Copy code
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Script not found / “module tools could not be loaded”
Run with a path:

powershell
Copy code
.\tools\preview.ps1
# or inside tools:
.\preview.ps1
Aliases not found
Reload profile:

powershell
Copy code
. $PROFILE
Get-Alias preview
Get-Alias publish
Pages didn’t update
Run publish again (it will create an empty commit if no docs changes). Then hard refresh the site (Ctrl+F5).

What the helper scripts do
tools\preview.ps1
Activates .venv

Sets env:

SITE_URL=http://<host>:<port>

RUN_HOST, RUN_PORT (used by run_local.py)

Starts Flask via tools\run_local.py without the reloader

Accepts: -Port, -BindHost, -Open

tools\run_local.py
Ensures project root on sys.path

Reads RUN_HOST/RUN_PORT (defaults: 127.0.0.1:5050)

Runs app.app.run(debug=True, use_reloader=False)

tools\publish-post.ps1
Activates .venv

Sets SITE_URL=https://azure-noob.com

Freezes to docs/

Commits & pushes to current branch

Sanity commands
powershell
Copy code
# health check (local)
curl http://127.0.0.1:5050/healthz

# quick import test
python - << 'PY'
import flask, markdown, yaml
from flask_frozen import Freezer
print("✅ imports OK")
PY

# see what’s listening on a port
netstat -ano | findstr ":5050"
File map (key bits)
pgsql
Copy code
app.py                    # Flask app
freeze.py                 # builds docs/ (Frozen-Flask)
posts/                    # your markdown posts
templates/                # Jinja templates (base, search, etc.)
static/                   # CSS/images
docs/                     # generated site (GitHub Pages)
tools/preview.ps1         # local run helper
tools/run_local.py        # local run driver
tools/publish-post.ps1    # build + push
yaml
Copy code

---

👉 Save this as `tools\WORKFLOW.md`, then commit with:

```powershell
git add tools\WORKFLOW.md
git commit -m "Add WORKFLOW.md cheat sheet"
git push