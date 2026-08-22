import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.core.models import FooterSection, FooterLink, Page

# Create a sample page
page, _ = Page.objects.get_or_create(
    title="Privacy Policy",
    slug="privacy-policy",
    defaults={
        "content": "<h2>Your Privacy Matters</h2><p>This is a placeholder for the privacy policy.</p>"
    }
)

# Product Section
product_sec, _ = FooterSection.objects.get_or_create(title="Product", display_order=1)
FooterLink.objects.get_or_create(section=product_sec, title="Features", external_url="#", display_order=1)
FooterLink.objects.get_or_create(section=product_sec, title="Pricing", external_url="#", display_order=2)
FooterLink.objects.get_or_create(section=product_sec, title="Integration API", external_url="#", display_order=3)
FooterLink.objects.get_or_create(section=product_sec, title="Webhooks", external_url="#", show_new_badge=True, display_order=4)
FooterLink.objects.get_or_create(section=product_sec, title="Case Studies", external_url="#", display_order=5)

# Company Section
company_sec, _ = FooterSection.objects.get_or_create(title="Company", display_order=2)
FooterLink.objects.get_or_create(section=company_sec, title="About Us", external_url="#", display_order=1)
FooterLink.objects.get_or_create(section=company_sec, title="Careers", external_url="#", display_order=2)
FooterLink.objects.get_or_create(section=company_sec, title="Blog", external_url="#", display_order=3)
FooterLink.objects.get_or_create(section=company_sec, title="Contact Sales", external_url="#", display_order=4)
FooterLink.objects.get_or_create(section=company_sec, title="Partners", external_url="#", display_order=5)

# Legal Section
legal_sec, _ = FooterSection.objects.get_or_create(title="Legal", display_order=3)
FooterLink.objects.get_or_create(section=legal_sec, title="Privacy Policy", page=page, display_order=1)
FooterLink.objects.get_or_create(section=legal_sec, title="Terms of Service", external_url="#", display_order=2)
FooterLink.objects.get_or_create(section=legal_sec, title="Cookie Policy", external_url="#", display_order=3)
FooterLink.objects.get_or_create(section=legal_sec, title="Security Audit", external_url="#", display_order=4)
FooterLink.objects.get_or_create(section=legal_sec, title="GDPR Compliance", external_url="#", display_order=5)

print("Seeded footer data successfully!")
