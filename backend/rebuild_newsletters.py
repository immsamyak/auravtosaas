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
    
    if not form:
        print(f"No form found in {theme_path}")
        return

    # Extract classes from the form
    form_classes = form.get('class', [])
    if isinstance(form_classes, list):
        form_classes = ' '.join(form_classes)
        
    input_field = form.find('input', type='email')
    input_classes = input_field.get('class', []) if input_field else []
    if isinstance(input_classes, list):
        input_classes = ' '.join(input_classes)
        
    button = form.find('button', type='submit')
    button_classes = button.get('class', []) if button else []
    if isinstance(button_classes, list):
        button_classes = ' '.join(button_classes)
    button_text = button.text.strip() if button else "Subscribe"

    # Identify theme name to apply generic typography if needed
    theme_name = os.path.basename(theme_path)

    # Some themes need flex-col on mobile, but let's trust the form_classes if they have flex
    if 'max-w-md' not in form_classes and 'w-full' not in form_classes:
        form_classes += ' max-w-md mx-auto w-full'
    if 'mx-auto' not in form_classes:
        form_classes += ' mx-auto'

    # Build a clean, guaranteed-to-work section
    new_html = f"""<section class="py-20 px-6 md:px-12 w-full flex flex-col items-center justify-center text-center" style="background-color: {{{{ settings.bgColor|default:'transparent' }}}};">
    <div class="max-w-3xl mx-auto w-full">
        <h2 class="text-3xl md:text-4xl font-bold mb-4">{{{{ settings.heading|default:'Subscribe to our Newsletter' }}}}</h2>
        <p class="text-lg opacity-80 mb-8">{{{{ settings.subheading|default:'Get the latest updates and offers directly in your inbox.' }}}}</p>
        
        <form action="{{% url 'newsletter_subscribe' brand.slug %}}" method="POST" id="newsletter-subscribe-form" class="{form_classes}">
            {{% csrf_token %}}
            <input type="email" name="email" required placeholder="Your email address" class="{input_classes}">
            <button type="submit" class="{button_classes}">{button_text}</button>
        </form>
    </div>
</section>
"""

    with open(newsletter_path, 'w') as f:
        f.write(new_html)
    print(f"Rebuilt {theme_name}")

for theme_path in glob.glob('templates/storefront/theme_*'):
    process_theme(theme_path)

