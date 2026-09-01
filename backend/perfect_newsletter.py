import os
import glob
from bs4 import BeautifulSoup
import re

def process_theme(theme_path):
    theme_name = os.path.basename(theme_path)
    map_path = os.path.join(theme_path, 'sections', 'map.html')
    newsletter_path = os.path.join(theme_path, 'sections', 'newsletter.html')
    
    if not os.path.exists(map_path) or not os.path.exists(newsletter_path):
        return

    # Extract the original form from the current newsletter.html
    with open(newsletter_path, 'r') as f:
        news_html = f.read()
    news_soup = BeautifulSoup(news_html, 'html.parser')
    form = news_soup.find('form')
    
    if not form:
        print(f"No form found in {theme_name}")
        return
        
    # Clean up the form classes (remove stuff my previous scripts forced)
    form_classes = form.get('class', [])
    if isinstance(form_classes, list):
        form_classes = [c for c in form_classes if c not in ['mx-auto', 'max-w-md', 'w-full', 'mt-10']]
        form['class'] = form_classes
    else:
        for c in ['mx-auto', 'max-w-md', 'w-full', 'mt-10']:
            form_classes = form_classes.replace(c, '')
        form['class'] = form_classes.strip()

    # Now, open map.html and use it as the base
    with open(map_path, 'r') as f:
        map_html = f.read()
    base_soup = BeautifulSoup(map_html, 'html.parser')
    
    # Update headings
    h2 = base_soup.find('h2')
    if h2:
        h2.string = "{{ settings.heading|default:'Subscribe to our Newsletter' }}"
        
    p = base_soup.find('p')
    if p:
        p.string = "{{ settings.subheading|default:'Get the latest updates and offers directly in your inbox.' }}"
        
    # Find the map container (usually the div containing iframe, or h-[500px])
    map_container = None
    for div in base_soup.find_all('div'):
        classes = div.get('class', [])
        if isinstance(classes, list) and ('h-[500px]' in classes or 'h-96' in classes or 'min-h-[400px]' in classes):
            map_container = div
            break
        elif isinstance(classes, str) and ('h-[500px]' in classes or 'h-96' in classes or 'min-h-[400px]' in classes):
            map_container = div
            break

    if not map_container:
        # Fallback: find the iframe's parent
        iframe = base_soup.find('iframe')
        if iframe:
            map_container = iframe.parent
            if map_container.name != 'div':
                map_container = iframe

    if map_container:
        # Check if text-center is in the wrapper (usually max-w-7xl)
        is_centered = False
        text_center_div = base_soup.find(lambda tag: tag.name == 'div' and 'text-center' in (tag.get('class') or []))
        if text_center_div:
            is_centered = True
            
        # Add layout classes to form so it looks good standalone
        f_classes = form.get('class', [])
        if isinstance(f_classes, list):
            f_classes.extend(['max-w-md', 'w-full', 'mt-8'])
            if is_centered:
                f_classes.append('mx-auto')
            form['class'] = f_classes
        else:
            f_c = f_classes + " max-w-md w-full mt-8"
            if is_centered:
                f_c += " mx-auto"
            form['class'] = f_c.strip()

        # Replace map_container with our form!
        map_container.replace_with(form)
    else:
        print(f"Could not find map container in {theme_name}")
        return

    # Unescape Django tags
    final_html = str(base_soup)
    final_html = final_html.replace('&lt;', '<').replace('&gt;', '>')
    
    # Make sure background color is dynamic
    # Map usually has bg-something, we should inject style="background-color: {{ settings.bgColor|default:'transparent' }};"
    # Find root div
    root_match = re.search(r'<div[^>]*class="[^"]*"[^>]*>', final_html)
    if root_match:
        root_tag = root_match.group(0)
        if 'style="' in root_tag:
            pass # already has style
        else:
            new_root_tag = root_tag.replace('>', ' style="background-color: {{ settings.bgColor|default:\'transparent\' }};">')
            final_html = final_html.replace(root_tag, new_root_tag, 1)

    with open(newsletter_path, 'w') as f:
        f.write(final_html)

    print(f"Perfected {theme_name}")

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)

