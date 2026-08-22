import os
import glob
import re

for filepath in glob.glob('apps/*/admin.py'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'from unfold.admin import ModelAdmin' not in content and 'admin.ModelAdmin' in content:
        content = "from unfold.admin import ModelAdmin\n" + content
        content = content.replace('admin.ModelAdmin', 'ModelAdmin')
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Updated {filepath}")
