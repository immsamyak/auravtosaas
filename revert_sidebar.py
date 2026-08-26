import os

files = [
    'backend/templates/dashboard_base.html',
    'backend/templates/admin/admin_base.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Revert the sidebar back to its original neutral-900
    content = content.replace('bg-slate-950', 'bg-neutral-900')
    content = content.replace('border-slate-800', 'border-neutral-800')

    with open(filepath, 'w') as f:
        f.write(content)

print("Sidebars reverted!")
