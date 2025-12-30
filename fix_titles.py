import os

files = [
    r'posts\2025-10-16-azure-chargeback-tags-model.md',
    r'posts\2025-10-31-azure-tag-governance-policy.md',
    r'posts\2025-11-03-azure-cost-optimization-facade.md',
    r'posts\azure-cost-management-is-confusing-but-you-can-tame-it.md'
]

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into front matter and body
    parts = content.split('---', 2)
    if len(parts) >= 3:
        front_matter = parts[1]
        body = parts[2]
        
        # Fix title field - add quotes if it contains a colon and isn't quoted
        lines = front_matter.split('\n')
        new_lines = []
        for line in lines:
            if line.startswith('title:') and ':' in line[6:]:  # Has colon after "title:"
                # Extract the title value
                title_value = line[6:].strip()
                if not (title_value.startswith('"') and title_value.endswith('"')):
                    line = f'title: "{title_value}"'
            new_lines.append(line)
        
        # Reassemble
        new_content = '---' + '\n'.join(new_lines) + '---' + body
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f'✅ Fixed title in: {filepath}')
    else:
        print(f'❌ Could not parse: {filepath}')

print('\n✅ All titles fixed! Now run: python freeze.py')
