import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.models import PlatformIntegration

whatsapp, created = PlatformIntegration.objects.get_or_create(
    provider_code='WHATSAPP',
    defaults={
        'name': 'WhatsApp Chat',
        'category': 'MARKETING',
        'description': 'Add a floating WhatsApp chat button to your storefront to talk directly to your customers.',
        'icon_html': '<i class="fa-brands fa-whatsapp text-3xl"></i>',
        'icon_color_hex': '#25D366',
        'icon_bg_hex': '#E8F9EE',
        'requires_merchant_id': True, # We use merchant_id field for Phone Number
    }
)

if not created:
    whatsapp.name = 'WhatsApp Chat'
    whatsapp.category = 'MARKETING'
    whatsapp.description = 'Add a floating WhatsApp chat button to your storefront to talk directly to your customers.'
    whatsapp.icon_html = '<i class="fa-brands fa-whatsapp text-3xl"></i>'
    whatsapp.icon_color_hex = '#25D366'
    whatsapp.icon_bg_hex = '#E8F9EE'
    whatsapp.requires_merchant_id = True
    whatsapp.save()

print("WhatsApp Integration Seeded Successfully!")
