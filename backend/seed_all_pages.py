import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.core.models import FooterSection, FooterLink, Page
from django.utils.text import slugify

# Helper to create page
def create_page(title, content):
    page, _ = Page.objects.get_or_create(
        title=title,
        slug=slugify(title),
        defaults={
            "content": f"<h2>{title}</h2><p>{content}</p>"
        }
    )
    return page

# Delete existing to prevent duplicates during seeding
FooterSection.objects.all().delete()
FooterLink.objects.all().delete()
Page.objects.all().delete()

# Content definitions
pages_data = {
    # Product
    "Features": "Explore the powerful features of Aura, designed to decimate return rates.",
    "Pricing": "Flexible pricing plans for fashion brands of all sizes.",
    "Integration API": "Documentation and endpoints for integrating Aura into your storefront.",
    "Webhooks": "Real-time event notifications for your applications.",
    "Case Studies": "See how leading brands have increased conversions with Aura.",
    
    # Company
    "About Us": "Aura is on a mission to revolutionize fashion e-commerce with Generative AI.",
    "Careers": "Join our team of AI researchers and engineers.",
    "Blog": "The latest news and insights on AI and fashion tech.",
    "Contact Sales": "Get in touch with our enterprise sales team.",
    "Partners": "Discover our network of technology and agency partners.",
    
    # Legal
    "Privacy Policy": "How we collect, use, and protect your personal information.",
    "Terms of Service": "The rules and regulations for the use of Aura's services.",
    "Cookie Policy": "Information about how we use cookies on our website.",
    "Security Audit": "Details on our security practices and compliance.",
    "GDPR Compliance": "How Aura complies with the General Data Protection Regulation."
}

# Create all pages
pages = {}
for title, content in pages_data.items():
    pages[title] = create_page(title, content)

# 1. Product Section
product_sec = FooterSection.objects.create(title="Product", display_order=1)
FooterLink.objects.create(section=product_sec, title="Features", page=pages["Features"], display_order=1)
FooterLink.objects.create(section=product_sec, title="Pricing", page=pages["Pricing"], display_order=2)
FooterLink.objects.create(section=product_sec, title="Integration API", page=pages["Integration API"], display_order=3)
FooterLink.objects.create(section=product_sec, title="Webhooks", page=pages["Webhooks"], show_new_badge=True, display_order=4)
FooterLink.objects.create(section=product_sec, title="Case Studies", page=pages["Case Studies"], display_order=5)

# 2. Company Section
company_sec = FooterSection.objects.create(title="Company", display_order=2)
FooterLink.objects.create(section=company_sec, title="About Us", page=pages["About Us"], display_order=1)
FooterLink.objects.create(section=company_sec, title="Careers", page=pages["Careers"], display_order=2)
FooterLink.objects.create(section=company_sec, title="Blog", page=pages["Blog"], display_order=3)
FooterLink.objects.create(section=company_sec, title="Contact Sales", page=pages["Contact Sales"], display_order=4)
FooterLink.objects.create(section=company_sec, title="Partners", page=pages["Partners"], display_order=5)

# 3. Legal Section
legal_sec = FooterSection.objects.create(title="Legal", display_order=3)
FooterLink.objects.create(section=legal_sec, title="Privacy Policy", page=pages["Privacy Policy"], display_order=1)
FooterLink.objects.create(section=legal_sec, title="Terms of Service", page=pages["Terms of Service"], display_order=2)
FooterLink.objects.create(section=legal_sec, title="Cookie Policy", page=pages["Cookie Policy"], display_order=3)
FooterLink.objects.create(section=legal_sec, title="Security Audit", page=pages["Security Audit"], display_order=4)
FooterLink.objects.create(section=legal_sec, title="GDPR Compliance", page=pages["GDPR Compliance"], display_order=5)

print("All pages and links seeded successfully!")
