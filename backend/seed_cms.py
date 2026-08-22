import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.core.models import LandingPageConfig, LandingPageFeature

def seed_cms():
    print("Seeding CMS data...")
    
    # Create config
    config, created = LandingPageConfig.objects.get_or_create(
        is_active=True,
        defaults={
            'hero_headline': 'The ultimate AI fitting room for modern fashion brands',
            'hero_subheadline': 'Stop dealing with returns due to poor sizing. Aura uses state-of-the-art Generative AI and Computer Vision to let your customers try on your entire catalog virtually.',
            'hero_primary_cta': 'Start your Store',
            'hero_secondary_cta': 'Brand Login',
            'demo_title': 'Experience it live',
            'demo_subtitle': 'Trusted Brands',
            'footer_text': '© 2026 Aura Virtual Try-On. All rights reserved.'
        }
    )
    
    if created:
        print("Created default LandingPageConfig.")
    else:
        print("LandingPageConfig already exists. Adding features if they are missing.")
        
    # Create Features
    features = [
        # Brand Features
        {
            'audience': 'BRAND',
            'title': 'Reduce Return Rates',
            'description': 'Customers who can visualize the fit are 40% less likely to return items due to sizing issues, saving you thousands in reverse logistics.',
            'icon_class': 'fa-solid fa-arrow-right-arrow-left',
            'display_order': 1,
        },
        {
            'audience': 'BRAND',
            'title': 'Boost Conversion',
            'description': 'Increase buyer confidence. Shoppers who use virtual try-on are 3x more likely to complete their purchase.',
            'icon_class': 'fa-solid fa-chart-line',
            'display_order': 2,
        },
        {
            'audience': 'BRAND',
            'title': 'Plug & Play Storefront',
            'description': 'Launch your own virtual storefront in minutes without writing a single line of code. Simply upload your catalog and go.',
            'icon_class': 'fa-solid fa-store',
            'display_order': 3,
        },
        
        # Shopper Features
        {
            'audience': 'SHOPPER',
            'title': 'Frictionless Guest Mode',
            'description': 'No account required. Upload a photo and see yourself in any outfit instantly. Your privacy is protected.',
            'icon_class': 'fa-solid fa-bolt',
            'display_order': 1,
        },
        {
            'audience': 'SHOPPER',
            'title': 'Personalized Fit',
            'description': 'Our AI analyzes your body proportions to recommend the absolute perfect size for your unique body type.',
            'icon_class': 'fa-solid fa-ruler',
            'display_order': 2,
        },
        {
            'audience': 'SHOPPER',
            'title': 'Hyper-Realistic AI',
            'description': 'We use state of the art diffusion models to ensure the lighting, drape, and texture of the clothes look real.',
            'icon_class': 'fa-solid fa-wand-magic-sparkles',
            'display_order': 3,
        }
    ]
    
    for feat in features:
        LandingPageFeature.objects.get_or_create(
            config=config,
            title=feat['title'],
            defaults={
                'audience': feat['audience'],
                'description': feat['description'],
                'icon_class': feat['icon_class'],
                'display_order': feat['display_order']
            }
        )
        
    print("Seed complete.")

if __name__ == '__main__':
    seed_cms()
