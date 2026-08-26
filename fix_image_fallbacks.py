import os
import re

base_dir = "backend/templates/storefront"
html_files = []
for root, dirs, files in os.walk(base_dir):
    for f in files:
        if f.endswith(".html"):
            html_files.append(os.path.join(root, f))

onerror_attr = '''onerror="this.onerror=null; this.src='{% if brand.logo %}{{ brand.logo.url }}{% else %}https://placehold.co/400x600/e2e8f0/64748b?text=No+Image{% endif %}';"'''

for filepath in html_files:
    with open(filepath, "r") as f:
        content = f.read()
    
    original_content = content
    
    # 1. Add onerror to <img> tags containing product.images.first or product.variants.first
    # We find <img ... src="...product..." ... /> and inject onerror if it's not already there.
    def add_onerror(match):
        img_tag = match.group(0)
        if "onerror=" not in img_tag:
            # insert onerror before the closing /> or >
            if img_tag.endswith("/>"):
                return img_tag[:-2] + f" {onerror_attr}/>"
            else:
                return img_tag[:-1] + f" {onerror_attr}>"
        return img_tag
    
    content = re.sub(r'<img[^>]*src="[^"]*product\.(images|variants)[^"]*"[^>]*>', add_onerror, content)
    
    # 2. Replace the {% else %} block of the product images condition with the brand logo fallback
    # The pattern is: {% if product.images.first %} ... {% else %} ... {% endif %}
    # But wait! There could be multiple {% if %} blocks in the file.
    # We specifically want the one that is used for product cards.
    # A safer way: replace {% else %} \n <div ...> \n ... \n </div> \n {% endif %}
    # We can match `{% elif product.variants.first.image %}...{% else %}...{% endif %}`
    
    pattern = re.compile(r'({% elif product\.variants\.first\.image %}.*?)(?:{% else %}.*?)(?={% endif %})', re.DOTALL)
    
    replacement = r'\1{% elif brand.logo %}\n<img alt="{{ brand.name }}" class="w-full h-full object-contain p-8 opacity-50" src="{{ brand.logo.url }}"/>\n{% else %}\n<div class="w-full h-full flex items-center justify-center bg-gray-100/10 text-gray-400"><i class="fa-solid fa-image text-3xl opacity-30"></i></div>\n'
    
    content = pattern.sub(replacement, content)

    if content != original_content:
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Updated {filepath}")

print("Done.")
