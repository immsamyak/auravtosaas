import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from apps.brands.models import Brand, Coupon, PopupBanner

User = get_user_model()

try:
    user = User.objects.get(username='alvics')
    brand = user.owned_brand
    
    # Create Coupon
    coupon, created = Coupon.objects.get_or_create(
        brand=brand,
        code='SUMMER26',
        defaults={
            'discount_type': 'PERCENTAGE',
            'discount_value': 20.00,
            'condition': 'NONE',
            'min_order_value': 0,
            'max_uses': 100,
            'is_active': True
        }
    )
    if created:
        print("Created coupon SUMMER26")
    else:
        print("Coupon SUMMER26 already exists")

    # Create Popup Banner
    popup, created = PopupBanner.objects.get_or_create(
        brand=brand,
        title='Summer Sale 2026 Promo',
        defaults={
            'banner_type': 'TOP_BAR',
            'display_rule': 'ALL_PAGES',
            'description': 'Summer sale promo popup',
            'cta_text': 'Shop Now',
            'cta_link': '/products/',
            'open_in_new_tab': False,
            'delay_seconds': 0,
            'is_active': True
        }
    )
    if created:
        print("Created popup banner: Summer Sale 2026 Promo")
    else:
        print("Popup banner already exists")

except User.DoesNotExist:
    print("User 'alvics' does not exist")
except Exception as e:
    print(f"Error: {e}")
