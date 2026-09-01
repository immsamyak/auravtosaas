import glob
from bs4 import BeautifulSoup
import os

def process_theme(theme_path):
    footer_path = os.path.join(theme_path, 'sections', 'footer.html')
    if not os.path.exists(footer_path):
        return

    with open(footer_path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form', id='newsletter-subscribe-form')
    if not form:
        print(f"No newsletter form found in {footer_path}")
        return

    # Find the container to extract. It's usually the immediate parent or grandparent.
    # In cyberpunk: parent is a div with h4 'Newsletter_'
    # In fashion: parent is a div with max-w-6xl
    # In goth: parent is a div with max-w-7xl
    container = form.parent
    if container.name == 'div' and not container.has_attr('id'):
        # Usually the container has the h4 heading. If not, go up one more.
        if not container.find(['h4', 'h3', 'h2']):
            container = container.parent
            
    print(f"--- Extracted from {theme_path} ---")
    print(container.prettify()[:200])

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)
