import os
import glob
from bs4 import BeautifulSoup

def process_theme(theme_path):
    newsletter_path = os.path.join(theme_path, 'sections', 'newsletter.html')
    if not os.path.exists(newsletter_path):
        return

    with open(newsletter_path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    form = soup.find('form')
    
    if form:
        form_classes = form.get('class', [])
        if isinstance(form_classes, list):
            if 'mt-8' not in form_classes and 'mt-10' not in form_classes and 'mt-12' not in form_classes:
                form_classes.append('mt-10')
            form['class'] = form_classes
        else:
            if 'mt-8' not in form_classes and 'mt-10' not in form_classes and 'mt-12' not in form_classes:
                form['class'] = form_classes + ' mt-10'

    final_html = str(soup)
    final_html = final_html.replace('&lt;', '<').replace('&gt;', '>')
    final_html = final_html.replace('style="{{ settings.bgColor|default:\'transparent\' }}"', 'style="background-color: {{ settings.bgColor|default:\'transparent\' }};"')

    with open(newsletter_path, 'w') as f:
        f.write(final_html)

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)
