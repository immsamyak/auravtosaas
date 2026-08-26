import re

files = [
    'backend/templates/dashboard_base.html',
    'backend/templates/admin/admin_base.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
        
    # Find the <aside> block
    start_idx = content.find('<aside')
    end_idx = content.find('</aside>') + len('</aside>')
    
    if start_idx != -1 and end_idx != -1:
        aside_content = content[start_idx:end_idx]
        
        # Replace slate- with neutral- in the aside block
        new_aside = aside_content.replace('slate-', 'neutral-')
        
        # Replace the aside block in the content
        new_content = content[:start_idx] + new_aside + content[end_idx:]
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        
        print(f"Fixed sidebar in {filepath}")

