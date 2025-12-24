#!/usr/bin/env bash
set -e

# 1. Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
  cat > .gitignore << 'EOF'
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
*.db

# Virtual env
.venv/
env/
venv/

# Build artifacts
build/
dist/
*.egg-info/

# IDE/editor junk
.vscode/
.idea/
*.swp
.DS_Store
Thumbs.db

# Logs
*.log

# OS
desktop.ini
EOF
  echo ".gitignore created ✅"
else
  echo ".gitignore already exists, skipping..."
fi

# 2. Untrack venv if it was staged
git rm -r --cached .venv 2>/dev/null || true

# 3. Stage and commit everything
git add .
git commit -m "Initial commit with Flask blog and deploy workflow" || echo "Nothing to commit"

# 4. Make sure branch is main
git branch -M main

# 5. Set remote and push
git remote add origin https://github.com/dswann101164/azure-noob-blog.git 2>/dev/null || true
git push -u origin main
