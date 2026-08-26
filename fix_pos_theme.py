import os
import re

mapping = {
    'bg-theme-bg-secondary': 'bg-slate-900',
    'bg-theme-bg': 'bg-slate-950',
    'bg-theme-surface-hover': 'bg-slate-800',
    'bg-theme-surface': 'bg-slate-900',
    'border-theme-border-subtle': 'border-slate-800',
    'border-theme-border': 'border-slate-700',
    'border-theme-input-border': 'border-slate-700',
    'text-theme-text-primary': 'text-white',
    'text-theme-text-secondary': 'text-slate-200',
    'text-theme-text-muted': 'text-slate-400',
    'text-theme-text-disabled': 'text-slate-500'
}

files = [
    'backend/apps/orders/templates/pos/terminal.html',
    'backend/apps/orders/templates/pos/customer_display.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Remove the injected tags
    content = content.replace(" <script src=\"{% static 'js/tailwind.config.js' %}\"></script>\n", "")
    content = content.replace(" <link rel=\"stylesheet\" href=\"{% static 'css/app.css' %}\">\n", "")
    content = content.replace("{% load static %}\n", "")

    # Replace classes
    # Use word boundary or simple replace since class names are exact
    # We sort mapping by length descending to prevent partial replacements (e.g. bg-theme-bg before bg-theme-bg-secondary)
    sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
    for k in sorted_keys:
        # Use regex to ensure word boundaries
        content = re.sub(r'\b' + re.escape(k) + r'\b', mapping[k], content)

    with open(filepath, 'w') as f:
        f.write(content)

print("POS terminal themes statically hardened!")
