import os
import glob
import re

TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/custom_admin"

# Fix dashboard.html
dash_path = os.path.join(TEMPLATES_DIR, "dashboard.html")
with open(dash_path, 'r') as f:
    dash_content = f.read()

# Regex to remove the <nav ...> ... </nav> block
dash_content = re.sub(r'<!-- Breadcrumb -->\n\s*<nav.*?aria-label="Breadcrumb">.*?</nav>', 
                      '{% include "components/breadcrumb.html" with current="Overview Dashboard" %}', 
                      dash_content, flags=re.DOTALL)

with open(dash_path, 'w') as f:
    f.write(dash_content)

# Fix form.html in all 40 models
for form_html in glob.glob(os.path.join(TEMPLATES_DIR, "*", "*", "form.html")):
    model_name = os.path.basename(os.path.dirname(form_html)).title()
    
    with open(form_html, 'r') as f:
        form_content = f.read()
    
    # We didn't actually generate a nav in form.html previously, wait...
    # Oh yes we did in `generate_custom_admin.py` I used `<!-- Breadcrumb -->`? No I didn't!
    # Wait, in the FIRST script (the Unfold upgrade), I did, but in `generate_custom_admin.py` I only put:
    # <div class="mb-8"><h1 class="text-4xl ...
    
    if '{% include "components/breadcrumb.html"' not in form_content:
        # inject above <div class="mb-8">
        form_content = form_content.replace(
            '<div class="mb-8">',
            f'{{% include "components/breadcrumb.html" with current="{model_name} Details" %}}\n    <div class="mb-8">'
        )
        
    with open(form_html, 'w') as f:
        f.write(form_content)

print("Breadcrumb components fixed across all templates.")
