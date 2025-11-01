# Scripts Directory

Helper scripts for managing the Azure Noob Blog.

## Directory Listing Scripts

### Show-RepoStructure.ps1
Interactive console display of repository structure (excludes generated folders).

**Usage:**
```powershell
# Basic usage (directories only, max depth 3)
.\scripts\Show-RepoStructure.ps1

# Show files too
.\scripts\Show-RepoStructure.ps1 -ShowFiles

# Different max depth
.\scripts\Show-RepoStructure.ps1 -MaxDepth 5

# Specific path
.\scripts\Show-RepoStructure.ps1 -Path .\posts -ShowFiles
```

### Export-RepoStructure.ps1
Exports repository structure to a text file for sharing in chats/documentation.

**Usage:**
```powershell
# Export to default file (repo-structure.txt)
.\scripts\Export-RepoStructure.ps1

# Custom output file
.\scripts\Export-RepoStructure.ps1 -OutputFile my-structure.txt

# Different max depth
.\scripts\Export-RepoStructure.ps1 -MaxDepth 5
```

**Tip:** Use this before sharing repo structure in Claude chats to avoid hitting token limits!

## Excluded Directories

Both scripts automatically exclude these folders to keep output clean:
- `docs/` - Frozen static site (220+ files)
- `.venv/` - Python virtual environment
- `__pycache__/` - Python cache
- `.git/` - Git internals
- `node_modules/` - npm packages (if any)
- `.pytest_cache/`, `.mypy_cache/` - Test/type caches
- `dist/`, `build/` - Build artifacts

## Why These Scripts?

**Problem:** When listing directories with tools, the `docs/` folder (220+ files) causes chat length issues.

**Solution:** These scripts intelligently filter out generated/large folders while showing the actual source structure.

## Quick Reference

```powershell
# View structure in console
.\scripts\Show-RepoStructure.ps1

# Export for sharing
.\scripts\Export-RepoStructure.ps1

# View the exported file
cat repo-structure.txt
```
