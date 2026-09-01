import os
import glob
from bs4 import BeautifulSoup
import re

def process_theme(theme_path):
    newsletter_path = os.path.join(theme_path, 'sections', 'newsletter.html')
    if not os.path.exists(newsletter_path):
        return

    with open(newsletter_path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove from section wrapper
    section = soup.find('section')
    if section:
        classes = section.get('class', [])
        if isinstance(classes, list):
            classes = [c for c in classes if c not in ['items-center', 'justify-center', 'text-center']]
            section['class'] = classes
        else:
            section['class'] = classes.replace('items-center', '').replace('justify-center', '').replace('text-center', '')

    # We also need to check the inner wrapper div
    inner_div = section.find('div') if section else None
    if inner_div:
        inner_classes = inner_div.get('class', [])
        if isinstance(inner_classes, list):
            # Do not remove mx-auto from inner div, because it constrains the max-width container, 
            # BUT wait, mx-auto on a max-w-3xl centers the container itself.
            # If the user wants the content left-aligned, the text inside will be left-aligned if we remove text-center!
            pass

    final_html = str(soup)
    final_html = final_html.replace('&lt;', '<').replace('&gt;', '>')
    final_html = final_html.replace('style="{{ settings.bgColor|default:\'transparent\' }}"', 'style="background-color: {{ settings.bgColor|default:\'transparent\' }};"')
    final_html = final_html.replace('  ', ' ') # clean up double spaces

    with open(newsletter_path, 'w') as f:
        f.write(final_html)

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)

