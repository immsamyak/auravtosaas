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
            
    # Now container holds the form and heading.
    # Convert it to a string.
    container_html = str(container)
    
    # We want to replace the hardcoded text with django template tags.
    # We will use BeautifulSoup to modify the DOM before converting to string.
    
    # Let's clone the container so we don't modify the footer soup
    import copy
    container_copy = copy.copy(container)
    
    # Find heading (h4, h3, h2)
    heading = container_copy.find(['h4', 'h3', 'h2'])
    if heading:
        original_text = heading.text.strip()
        heading.string = f"{{{{ settings.heading|default:'{original_text}' }}}}"
        
    # Find subheading (p) before the form
    subheading = container_copy.find('p')
    if subheading and form.find_previous_sibling('p') == subheading:
        original_text = subheading.text.strip()
        subheading.string = f"{{{{ settings.subheading|default:'{original_text}' }}}}"
        
    # Wrap in a section
    final_html = f"""<section class="py-16 px-4 md:px-8 w-full" style="background-color: {{{{ settings.bgColor|default:'transparent' }}}};">
    {str(container_copy)}
</section>
"""
    
    # Unescape the django tags since bs4 escapes them
    final_html = final_html.replace('{{ ', '{{ ').replace(' }}', ' }}')
    final_html = final_html.replace('&lt;', '<').replace('&gt;', '>')
    
    # Save to newsletter.html
    newsletter_path = os.path.join(theme_path, 'sections', 'newsletter.html')
    with open(newsletter_path, 'w') as f:
        f.write(final_html)
        
    print(f"Created {newsletter_path}")

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)

