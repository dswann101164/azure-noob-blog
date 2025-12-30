import os

files = [
    r'posts\2025-10-31-azure-tag-governance-policy.md',
    r'posts\2025-11-03-azure-cost-optimization-facade.md',
    r'posts\azure-cost-management-is-confusing-but-you-can-tame-it.md'
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('summary:'):
            summary_lines = [lines[i].replace('summary: ', '').strip()]
            i += 1
            while i < len(lines) and lines[i].startswith('  '):
                summary_lines.append(lines[i].strip())
                i += 1
            full_summary = ' '.join(summary_lines)
            new_lines.append(f'summary: "{full_summary}"\n')
        else:
            new_lines.append(lines[i])
            i += 1
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f'✅ Fixed: {filepath}')

print('\n✅ All 3 files fixed! Now run: python freeze.py')
