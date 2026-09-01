import os
import glob
from bs4 import BeautifulSoup
import re

def process_theme(theme_path):
    map_path = os.path.join(theme_path, 'sections', 'map.html')
    newsletter_path = os.path.join(theme_path, 'sections', 'newsletter.html')
    
    if not os.path.exists(map_path) or not os.path.exists(newsletter_path):
        return

    # Extract original form styling from current newsletter.html
    with open(newsletter_path, 'r') as f:
        news_html = f.read()
    news_soup = BeautifulSoup(news_html, 'html.parser')
    
    form = news_soup.find('form')
    input_field = news_soup.find('input', type='email')
    button = news_soup.find('button', type='submit')
    
    form_c = ' '.join(form.get('class', [])) if form else ''
    input_c = ' '.join(input_field.get('class', [])) if input_field else ''
    button_c = ' '.join(button.get('class', [])) if button else ''
    button_t = button.text.strip() if button else 'Subscribe'
    
    # Clean up form classes
    for c in ['mx-auto', 'max-w-md', 'w-full', 'mt-10', 'mt-8']:
        form_c = form_c.replace(c, '').strip()

    # Extract map styling
    with open(map_path, 'r') as f:
        map_html = f.read()
    map_soup = BeautifulSoup(map_html, 'html.parser')
    
    # 1. Section root classes (the first div)
    root = map_soup.find(lambda tag: tag.name in ['div', 'section'] and not tag.find_parent())
    if not root: root = map_soup.div
    root_c = ' '.join(root.get('class', [])) if root else ''
    
    # Remove 'py-20' or 'py-24' and standardise to py-16 md:py-24 so it always has padding, or just keep what map has
    
    # 2. Inner wrapper classes (the div containing h2)
    h2 = map_soup.find('h2')
    h2_c = ' '.join(h2.get('class', [])) if h2 else ''
    
    p = map_soup.find('p')
    p_c = ' '.join(p.get('class', [])) if p else ''
    
    inner_wrapper = h2.parent if h2 else None
    inner_c = ' '.join(inner_wrapper.get('class', [])) if inner_wrapper else 'text-center mb-12'

    # 3. Constraining container (usually the div above inner_wrapper, like max-w-7xl mx-auto)
    container = inner_wrapper.parent if inner_wrapper else None
    container_c = ' '.join(container.get('class', [])) if container else 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8'
    
    # If the script above failed, provide defaults
    if 'text-center' not in inner_c: inner_c += ' text-center'

    # Build the perfect HTML
    new_html = f"""<div class="{root_c}" style="background-color: {{{{ settings.bgColor|default:'transparent' }}}};">
    <div class="{container_c}">
        <div class="{inner_c}">
            <h2 class="{h2_c}">{{{{ settings.heading|default:'Subscribe to our Newsletter' }}}}</h2>
            <p class="{p_c}">{{{{ settings.subheading|default:'Get the latest updates and offers directly in your inbox.' }}}}</p>
        </div>
        <form action="{{% url 'newsletter_subscribe' brand.slug %}}" method="POST" id="newsletter-subscribe-form" class="{form_c} max-w-md mx-auto w-full mt-8">
            {{% csrf_token %}}
            <input type="email" name="email" required placeholder="Your email address" class="{input_c}">
            <button type="submit" class="{button_c}">{button_t}</button>
        </form>
    </div>
</div>
"""
    
    # Clean up multiple spaces
    new_html = re.sub(r' +', ' ', new_html)
    
    with open(newsletter_path, 'w') as f:
        f.write(new_html)

    print(f"Generated ultimate {os.path.basename(theme_path)}")

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)

