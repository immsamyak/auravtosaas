import os
import glob
import re

for filepath in glob.glob('apps/*/admin.py'):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Replace all admin.ModelAdmin with ModelAdmin
    content = content.replace('admin.ModelAdmin', 'ModelAdmin')
    # Replace all admin.TabularInline with TabularInline
    content = content.replace('admin.TabularInline', 'TabularInline')
    
    # Ensure imports exist
    if 'from unfold.admin import ModelAdmin' not in content and 'ModelAdmin' in content:
        content = "from unfold.admin import ModelAdmin\n" + content
    if 'from unfold.admin import TabularInline' not in content and 'TabularInline' in content:
        content = "from unfold.admin import TabularInline\n" + content
        
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Updated {filepath}")
