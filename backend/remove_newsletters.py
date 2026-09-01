import os
import glob
from bs4 import BeautifulSoup
import re

def process_theme(theme_path):
    footer_path = os.path.join(theme_path, 'sections', 'footer.html')
    if not os.path.exists(footer_path):
        return

    with open(footer_path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form', id='newsletter-subscribe-form')
    if not form:
        print(f"No form in {theme_path}")
        return

    # Find heading and subheading before the form to remove them
    elements_to_remove = [form]
    
    # Check previous siblings
    prev = form.previous_sibling
    while prev:
        if prev.name in ['h2', 'h3', 'h4', 'h5', 'h6', 'p']:
            elements_to_remove.append(prev)
            prev = prev.previous_sibling
        elif prev.name is None and prev.text.strip() == '':
            # It's a whitespace NavigableString, safe to ignore/remove
            elements_to_remove.append(prev)
            prev = prev.previous_sibling
        else:
            # We hit something else (like an <a> tag, or copyright), stop looking back
            break
            
    parent = form.parent
    
    # Remove the elements
    for el in elements_to_remove:
        el.extract()
        
    # If parent is now essentially empty (only whitespace), remove parent too
    if not parent.text.strip() and not parent.find(['img', 'a', 'div', 'ul', 'li', 'span', 'i', 'svg']):
        parent.extract()
        
    final_html = str(soup)
    # Unescape common html entities if bs4 escaped them
    final_html = final_html.replace('&lt;', '<').replace('&gt;', '>')
    
    with open(footer_path, 'w') as f:
        f.write(final_html)
        
    print(f"Cleaned {footer_path}")

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)

