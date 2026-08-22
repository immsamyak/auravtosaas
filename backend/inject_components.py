import os
import glob
import re

ADMIN_DIR = "/Users/saamyak/COllege Project/Aura/backend/apps/admin"
TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/custom_admin"

# 1. Inject paginate_by = 15 into all ListViews
for py_file in glob.glob(os.path.join(ADMIN_DIR, "*.py")):
    with open(py_file, 'r') as f:
        content = f.read()
    
    # regex to find context_object_name = 'objects' and inject paginate_by
    if "context_object_name = 'objects'" in content and "paginate_by =" not in content:
        content = content.replace(
            "context_object_name = 'objects'", 
            "context_object_name = 'objects'\n    paginate_by = 15"
        )
        with open(py_file, 'w') as f:
            f.write(content)

# 2. Inject components into all list.html templates
for list_html in glob.glob(os.path.join(TEMPLATES_DIR, "*", "*", "list.html")):
    with open(list_html, 'r') as f:
        content = f.read()
    
    # Replace old breadcrumb with include
    # The old breadcrumb block starts with <div class="flex justify-between items-center mb-8">
    # Wait, my generate script didn't put breadcrumbs in the list.html! It just put the h1.
    
    # Let's see what is actually in list.html:
    # <div class="flex justify-between items-center mb-8">
    
    # We will inject the breadcrumb right after <div class="max-w-7xl mx-auto">
    model_name = os.path.basename(os.path.dirname(list_html)).title()
    
    if "components/breadcrumb.html" not in content:
        content = content.replace(
            '<div class="flex justify-between items-center mb-8">',
            f'{{% include "components/breadcrumb.html" with current="{model_name} Management" %}}\n    <div class="flex justify-between items-center mb-8">'
        )
    
    # Inject pagination after </table>
    if "components/pagination.html" not in content:
        content = content.replace(
            '</table>',
            '</table>\n        {% include "components/pagination.html" %}'
        )
        
    with open(list_html, 'w') as f:
        f.write(content)

# 3. Inject components into admin_base.html
base_html = os.path.join(TEMPLATES_DIR, "admin_base.html")
with open(base_html, 'r') as f:
    content = f.read()

if "components/toast.html" not in content:
    content = content.replace(
        '</body>',
        '    {% include "components/toast.html" %}\n</body>'
    )
    with open(base_html, 'w') as f:
        f.write(content)

print("Components successfully injected!")
