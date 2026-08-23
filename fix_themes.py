import os
import glob

themes_dir = "backend/templates/storefront"
theme_dirs = glob.glob(os.path.join(themes_dir, "theme_*"))

for theme_dir in theme_dirs:
    base_html_path = os.path.join(theme_dir, "base.html")
    if not os.path.exists(base_html_path):
        continue
        
    with open(base_html_path, 'r') as f:
        content = f.read()
        
    # Check if we already loaded it
    if "{% load analytics_tags %}" not in content:
        # Add after {% load static %} or at the top
        if "{% load static %}" in content:
            content = content.replace("{% load static %}", "{% load static %}\n{% load analytics_tags %}")
        else:
            content = "{% load analytics_tags %}\n" + content
            
    if "{% render_brand_analytics brand %}" not in content:
        # Add right before </body>
        if "</body>" in content:
            content = content.replace("</body>", "    {% render_brand_analytics brand %}\n</body>")
        else:
            # Fallback to end of file
            content += "\n{% render_brand_analytics brand %}\n"
            
    with open(base_html_path, 'w') as f:
        f.write(content)
        
print(f"Updated {len(theme_dirs)} themes.")
