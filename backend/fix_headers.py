import os
import glob
import re

ADMIN_TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/admin"

header_html = '<h1 class="text-4xl font-extrabold text-slate-900 tracking-tight">Superadmin <span class="text-indigo-600 font-light">Console</span></h1>'

for filepath in glob.glob(ADMIN_TEMPLATES_DIR + '/**/*.html', recursive=True):
    if filepath.endswith('list.html') or filepath.endswith('form.html'):
        with open(filepath, 'r') as f:
            content = f.read()
            
        # The original header is something like <h1 class="text-4xl font-extrabold text-slate-900">Brand</h1>
        # or similar. Let's find it.
        # Note: in list.html and form.html, it's usually inside <div class="flex justify-between items-center mb-8">
        # Let's just regex replace <h1 class="text-4xl font-extrabold text-slate-900">.*?</h1>
        
        new_content = re.sub(r'<h1 class="text-4xl font-extrabold text-slate-900.*?>.*?</h1>', header_html, content)
        
        if new_content != content:
            with open(filepath, 'w') as f:
                f.write(new_content)
            print(f"Fixed header in {filepath}")

print("All headers updated.")
