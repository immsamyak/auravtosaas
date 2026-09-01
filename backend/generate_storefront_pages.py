import os
import glob
import re
from bs4 import BeautifulSoup

def get_theme_classes(theme_path):
    map_path = os.path.join(theme_path, 'sections', 'map.html')
    if not os.path.exists(map_path):
        return "py-12", "max-w-7xl mx-auto px-4"
        
    with open(map_path, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    root = soup.find(lambda tag: tag.name in ['div', 'section'] and not tag.find_parent())
    if not root: root = soup.div
    
    root_c = ' '.join(root.get('class', [])) if root else ''
    
    # Try to find container
    container = None
    if root:
        for child in root.find_all('div', recursive=False):
            if 'max-w-' in ' '.join(child.get('class', [])):
                container = child
                break
    
    container_c = ' '.join(container.get('class', [])) if container else 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'
    
    # Extract padding and margins from root
    root_padding = ' '.join([c for c in root_c.split() if c.startswith('py-') or c.startswith('pt-') or c.startswith('pb-') or c.startswith('my-')])
    if not root_padding:
        root_padding = "py-12"
        
    return root_padding, container_c

def generate_pages():
    source_files = {
        'account.html': 'apps/brands/templates/brands/store_account.html',
        'checkout.html': 'apps/orders/templates/orders/checkout.html',
        'order_success.html': 'apps/orders/templates/orders/order_success.html',
        'track_order.html': 'apps/orders/templates/orders/track_order.html'
    }
    
    # Read core content
    core_contents = {}
    for name, path in source_files.items():
        with open(path, 'r') as f:
            content = f.read()
            # Remove extends block
            content = re.sub(r'{% extends .*? %}\n', '', content)
            # Remove load tags
            content = re.sub(r'{% load static %}\n', '', content)
            # Remove block content
            content = re.sub(r'{% block content %}', '', content)
            content = re.sub(r'{% endblock %}', '', content)
            
            # Find the top-level div and replace its classes with placeholders
            soup = BeautifulSoup(content, 'html.parser')
            # Since these are django templates with logic, BeautifulSoup might mess up django tags.
            # So let's just do a regex replace on the first <div class="...">
            match = re.search(r'<div class="([^"]+)"', content)
            if match:
                original_classes = match.group(1)
                # Keep AlpineJS or specific classes, remove layout classes
                kept_classes = [c for c in original_classes.split() if not c.startswith('py-') and not c.startswith('pb-') and not c.startswith('pt-') and not c.startswith('max-w-') and not c.startswith('mx-')]
                new_class_str = "{ROOT_PADDING} " + " ".join(kept_classes)
                content = content[:match.start(1)] + new_class_str + content[match.end(1):]
                
            core_contents[name] = content.strip()

    themes = glob.glob('templates/storefront/theme_*')
    for theme in themes:
        root_padding, container_c = get_theme_classes(theme)
        
        for name, content in core_contents.items():
            final_content = content.replace('{ROOT_PADDING}', root_padding)
            
            dest_path = os.path.join(theme, name)
            with open(dest_path, 'w') as f:
                f.write("{% extends theme_base %}\n{% load static %}\n\n{% block content %}\n")
                f.write(final_content)
                f.write("\n{% endblock %}\n")
            print(f"Generated {dest_path}")

if __name__ == '__main__':
    generate_pages()
