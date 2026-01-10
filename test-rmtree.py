# Test if shutil.rmtree is actually deleting the docs directory
import shutil
import os
from pathlib import Path

DEST = "docs"

print("Testing shutil.rmtree behavior...")
print(f"Target directory: {DEST}")
print(f"Directory exists: {os.path.exists(DEST)}")

if os.path.exists(DEST):
    print(f"\nContents before deletion:")
    tags_dir = Path(DEST) / "tags"
    if tags_dir.exists():
        problem_dirs = []
        for item in tags_dir.iterdir():
            if ' ' in item.name or item.name[0].isupper():
                problem_dirs.append(item.name)
        
        if problem_dirs:
            print(f"Found {len(problem_dirs)} problem directories with spaces/caps:")
            for d in problem_dirs[:10]:
                print(f"  - {d}")
        else:
            print("No problem directories found")
    
    print(f"\nAttempting shutil.rmtree('{DEST}', ignore_errors=True)...")
    try:
        shutil.rmtree(DEST, ignore_errors=True)
        print("✓ rmtree completed")
    except Exception as e:
        print(f"✗ rmtree failed: {e}")
    
    print(f"\nDirectory exists after rmtree: {os.path.exists(DEST)}")
    
    if os.path.exists(DEST):
        print("⚠ WARNING: Directory still exists! Windows file lock issue!")
        print("\nChecking what's left:")
        if tags_dir.exists():
            remaining = list(tags_dir.iterdir())
            print(f"  {len(remaining)} items still in docs/tags/")
            for item in remaining[:5]:
                print(f"    - {item.name}")
