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

    # Determine the container to extract
    container = form.parent
    if container.name == 'div' and not container.has_attr('id'):
        if not container.find(['h4', 'h3', 'h2']):
            container = container.parent
            
    # Remove the container
    container.decompose()
    
    # Unescape the django tags since bs4 escapes them
    # Wait, BeautifulSoup might mess up other Django template tags!
    # A better approach: find the exact string of the container and string replace it in the original HTML to avoid messing up Django tags.
    container_html = str(container)
    # But container_html might have been modified by bs4 (attributes sorted, tags closed).
    print(f"Needs removing from {theme_path}")

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)

