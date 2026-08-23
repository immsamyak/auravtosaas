import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.models import PlatformIntegration

integration, created = PlatformIntegration.objects.get_or_create(
    provider_code='STRIPE',
    defaults={
        'name': 'Stripe Payments',
        'category': 'PAYMENT',
        'description': 'Accept credit cards and global payments securely via Stripe.',
        'is_active_globally': True,
        'requires_api_key': True,
        'requires_api_secret': True,
        'requires_merchant_id': False,
    }
)
print("Stripe created:" if created else "Stripe already exists:")
print(f"Name: {integration.name}, Category: {integration.category}")
