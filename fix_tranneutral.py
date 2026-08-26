files = [
    'backend/templates/dashboard_base.html',
    'backend/templates/admin/admin_base.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_content = content.replace('tranneutral', 'translate')
    
    with open(filepath, 'w') as f:
        f.write(new_content)
        
    print(f"Fixed {filepath}")
