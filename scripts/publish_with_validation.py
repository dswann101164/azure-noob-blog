#!/usr/bin/env python
"""
Complete publishing workflow with canonical validation
"""

import subprocess
import sys

def run_command(cmd, description):
    """Run a command and report status"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ {description} failed")
        return False
    print(f"✓ {description} completed")
    return True

def main():
    print("\n" + "="*80)
    print("AZURE NOOB PUBLISHING WORKFLOW")
    print("="*80)
    
    steps = [
        ("python freeze.py", "1. Freezing Flask site to /docs"),
        ("python fix_static_html_noindex.py", "2. Adding noindex to static HTML"),
        ("python validate_canonicals.py", "3. Validating canonical URLs"),
    ]
    
    for cmd, description in steps:
        if not run_command(cmd, description):
            print("\n❌ Publishing workflow failed")
            sys.exit(1)
    
    print("\n" + "="*80)
    print("✓ ALL CHECKS PASSED - READY TO COMMIT")
    print("="*80)
    print("\nNext steps:")
    print("  git add docs posts")
    print('  git commit -m "Publish new post + canonical fixes"')
    print("  git push")
    print("")

if __name__ == '__main__':
    main()
