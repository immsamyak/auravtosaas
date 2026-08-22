import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.brands.models import StoreTheme

themes = [
    {
        "name": "Lumina",
        "business_type": "Fashion & Apparel",
        "description": "Minimalist, large imagery, sleek typography perfect for clothing and accessories.",
        "template_folder": "theme_fashion"
    },
    {
        "name": "ElectroPro",
        "business_type": "Electronics & Tech",
        "description": "Clean, high-contrast, structured grid ideal for gadgets and tech products.",
        "template_folder": "theme_electronics"
    },
    {
        "name": "Glow",
        "business_type": "Beauty & Cosmetics",
        "description": "Soft color palettes, elegant fonts, and whitespace-heavy for makeup and skincare.",
        "template_folder": "theme_beauty"
    },
    {
        "name": "Habitat",
        "business_type": "Home & Decor",
        "description": "Earthy tones, lifestyle focus, masonry layouts for furniture and decor.",
        "template_folder": "theme_home"
    },
    {
        "name": "Velocity",
        "business_type": "Fitness & Sports",
        "description": "High energy, bold typography, vibrant accents for sports gear and activewear.",
        "template_folder": "theme_fitness"
    }
]

def seed_themes():
    print("Seeding themes...")
    for theme_data in themes:
        theme, created = StoreTheme.objects.get_or_create(
            template_folder=theme_data["template_folder"],
            defaults=theme_data
        )
        if created:
            print(f"Created theme: {theme.name}")
        else:
            print(f"Theme already exists: {theme.name}")
            
    print("Themes seeded successfully!")

if __name__ == '__main__':
    seed_themes()
