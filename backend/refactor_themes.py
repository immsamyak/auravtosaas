import os
import re

THEMES = [
    {
        "index": "templates/storefront/theme_fashion/index.html",
        "base": "templates/storefront/theme_fashion/base.html",
        "extends_path": "storefront/theme_fashion/base.html"
    },
    {
        "index": "templates/storefront/theme_electronics/index.html",
        "base": "templates/storefront/theme_electronics/base.html",
        "extends_path": "storefront/theme_electronics/base.html"
    },
    {
        "index": "templates/storefront/theme_beauty/index.html",
        "base": "templates/storefront/theme_beauty/base.html",
        "extends_path": "storefront/theme_beauty/base.html"
    },
    {
        "index": "templates/storefront/theme_home/index.html",
        "base": "templates/storefront/theme_home/base.html",
        "extends_path": "storefront/theme_home/base.html"
    },
    {
        "index": "templates/storefront/theme_fitness/index.html",
        "base": "templates/storefront/theme_fitness/base.html",
        "extends_path": "storefront/theme_fitness/base.html"
    },
    {
        "index": "apps/brands/templates/brands/storefront.html",
        "base": "apps/brands/templates/brands/store_base.html",
        "extends_path": "brands/store_base.html"
    }
]

def split_template(theme):
    with open(theme['index'], 'r') as f:
        content = f.read()
    
    # 1. Identify the split points.
    # The header usually ends before <!-- Hero --> or similar.
    # The footer usually starts at <!-- Footer -->.
    
    # Wait, the default storefront doesn't have <!-- Hero -->, it has <!-- Minimalist High-End Header -->
    hero_marker = "<!-- Hero -->" if "<!-- Hero -->" in content else "<!-- Minimalist High-End Header -->"
    footer_marker = "<!-- Footer -->" if "<!-- Footer -->" in content else "</body>"

    if hero_marker not in content:
        print(f"Skipping {theme['index']} - could not find hero marker")
        return
        
    parts = content.split(hero_marker)
    top_part = parts[0]
    rest = hero_marker + parts[1]
    
    parts2 = rest.rsplit(footer_marker, 1)
    middle_part = parts2[0]
    bottom_part = footer_marker + parts2[1] if len(parts2) > 1 else "</body>\n</html>"

    # Assemble base.html
    base_html = top_part + "\n{% block store_content %}{% endblock %}\n\n" + bottom_part
    
    # Assemble index.html
    index_html = f"{{% extends \"{theme['extends_path']}\" %}}\n{{% load analytics_tags %}}\n\n{{% block store_content %}}\n" + middle_part + "\n{% endblock %}\n"
    
    with open(theme['base'], 'w') as f:
        f.write(base_html)
        
    with open(theme['index'], 'w') as f:
        f.write(index_html)
        
    print(f"Processed {theme['index']}")

for t in THEMES:
    split_template(t)
