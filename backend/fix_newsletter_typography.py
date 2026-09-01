import os
import glob
from bs4 import BeautifulSoup
import re

def process_theme(theme_path):
    map_path = os.path.join(theme_path, 'sections', 'map.html')
    newsletter_path = os.path.join(theme_path, 'sections', 'newsletter.html')
    
    if not os.path.exists(map_path) or not os.path.exists(newsletter_path):
        return

    # Extract styling from map.html
    with open(map_path, 'r') as f:
        map_html = f.read()
    map_soup = BeautifulSoup(map_html, 'html.parser')
    
    # 1. Section wrapper class
    # usually the first div or section in the file
    map_root = map_soup.find(lambda tag: tag.name in ['div', 'section'] and not tag.find_parent())
    if not map_root: map_root = map_soup.div
    section_classes = map_root.get('class', []) if map_root else []
    if isinstance(section_classes, list):
        section_classes = ' '.join(section_classes)

    # 2. Heading class
    h2 = map_soup.find('h2')
    h2_classes = h2.get('class', []) if h2 else []
    if isinstance(h2_classes, list):
        h2_classes = ' '.join(h2_classes)

    # 3. Subheading class
    p = map_soup.find('p')
    p_classes = p.get('class', []) if p else []
    if isinstance(p_classes, list):
        p_classes = ' '.join(p_classes)

    # Now apply to newsletter.html
    with open(newsletter_path, 'r') as f:
        news_html = f.read()
    news_soup = BeautifulSoup(news_html, 'html.parser')

    news_root = news_soup.find(lambda tag: tag.name in ['div', 'section'] and not tag.find_parent())
    if not news_root: news_root = news_soup.section
    
    # Replace root classes but ensure we keep flex/centering if we need it, actually we'll just 
    # keep the padding and background from map_root, and apply flex centering
    if section_classes:
        news_root['class'] = section_classes + " flex flex-col items-center justify-center"
        # We also need to preserve the inline style for user override
        news_root['style'] = "{{ settings.bgColor|default:'transparent' }}"
        
        # Replace background-color in inline style correctly without messing up django
        # Actually bs4 will escape it. Better to do it via regex after.

    news_h2 = news_soup.find('h2')
    if news_h2 and h2_classes:
        news_h2['class'] = h2_classes

    news_p = news_soup.find('p')
    if news_p and p_classes:
        news_p['class'] = p_classes

    final_html = str(news_soup)
    # Unescape Django tags
    final_html = final_html.replace('&lt;', '<').replace('&gt;', '>')
    final_html = final_html.replace('style="{{ settings.bgColor|default:\'transparent\' }}"', 'style="background-color: {{ settings.bgColor|default:\'transparent\' }};"')

    with open(newsletter_path, 'w') as f:
        f.write(final_html)

    print(f"Fixed typography for {os.path.basename(theme_path)}")

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)
