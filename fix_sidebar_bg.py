import os

files = [
    'backend/templates/dashboard_base.html',
    'backend/templates/admin/admin_base.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Replace all bg-neutral-900 with bg-slate-950
    content = content.replace('bg-neutral-900', 'bg-slate-950')
    # Replace borders to match slate palette (border-neutral-800 to border-slate-800)
    content = content.replace('border-neutral-800', 'border-slate-800')

    with open(filepath, 'w') as f:
        f.write(content)

print("Sidebars successfully matched to the main page dark mode color (slate-950)!")
