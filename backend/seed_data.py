import os
import django
import random
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.base")
django.setup()

from django.contrib.auth.models import User
from apps.brands.models import Brand
from apps.catalog.models import Category, ProductType, Size, Color, Product, ProductVariant
from apps.inventory.models import Location, StockLevel
from apps.core.models import SystemSetting, BrandSetting

def run():
    print("Seeding database with professional dummy data...")

    # Create Superuser if not exists
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin')

    owner, _ = User.objects.get_or_create(username='brand_owner', defaults={'email': 'owner@aura.ai'})
    if not owner.password:
        owner.set_password('password123')
        owner.save()

    owner2, _ = User.objects.get_or_create(username='brand_owner2', defaults={'email': 'owner2@aura.ai'})
    if not owner2.password:
        owner2.set_password('password123')
        owner2.save()

    # Create Brands
    brand1, _ = Brand.objects.get_or_create(
        name="Urban Threads", 
        defaults={'slug': 'urban-threads', 'owner': owner}
    )
    brand2, _ = Brand.objects.get_or_create(
        name="Luxe Apparel", 
        defaults={'slug': 'luxe-apparel', 'owner': owner2}
    )

    # Locations
    loc1, _ = Location.objects.get_or_create(brand=brand1, name="New York Flagship", defaults={'location_type': 'STORE', 'address': '123 Broadway, NY'})
    loc2, _ = Location.objects.get_or_create(brand=brand1, name="East Coast Warehouse", defaults={'location_type': 'WAREHOUSE'})
    loc3, _ = Location.objects.get_or_create(brand=brand2, name="Beverly Hills Boutique", defaults={'location_type': 'STORE'})

    # System Settings
    SystemSetting.objects.get_or_create(key='GLOBAL_AI_ENABLED', defaults={'value': 'True'})
    SystemSetting.objects.get_or_create(key='DEFAULT_CURRENCY', defaults={'value': 'USD'})
    
    # Brand Settings
    BrandSetting.objects.get_or_create(brand=brand1, defaults={'primary_color': '#1A202C'})
    BrandSetting.objects.get_or_create(brand=brand2, defaults={'primary_color': '#FFFFFF'})

    # Categories
    cat_men, _ = Category.objects.get_or_create(name="Men's Clothing", slug='mens', display_order=1)
    cat_women, _ = Category.objects.get_or_create(name="Women's Clothing", slug='womens', display_order=2)
    
    cat_tops, _ = Category.objects.get_or_create(name="Tops", slug='tops', parent=cat_men, display_order=1)
    cat_bottoms, _ = Category.objects.get_or_create(name="Bottoms", slug='bottoms', parent=cat_men, display_order=2)
    cat_dresses, _ = Category.objects.get_or_create(name="Dresses", slug='dresses', parent=cat_women, display_order=1)

    # Product Types
    pt_tshirt, _ = ProductType.objects.get_or_create(name="T-Shirt", slug='t-shirt')
    pt_jeans, _ = ProductType.objects.get_or_create(name="Jeans", slug='jeans')
    pt_dress, _ = ProductType.objects.get_or_create(name="Dress", slug='dress')
    pt_jacket, _ = ProductType.objects.get_or_create(name="Jacket", slug='jacket')

    # Sizes
    sizes = [
        ("XS", "XS", 1), ("Small", "S", 2), ("Medium", "M", 3), 
        ("Large", "L", 4), ("XL", "XL", 5), ("XXL", "XXL", 6)
    ]
    size_objs = []
    for name, code, order in sizes:
        s, _ = Size.objects.get_or_create(code=code, defaults={'name': name, 'display_order': order})
        size_objs.append(s)

    # Colors
    colors = [
        ("Black", "black", "#000000"), ("White", "white", "#FFFFFF"), 
        ("Navy Blue", "navy", "#000080"), ("Crimson Red", "red", "#DC143C"), 
        ("Charcoal Grey", "grey", "#36454F"), ("Olive Green", "olive", "#808000")
    ]
    color_objs = []
    for name, slug, hex_code in colors:
        c, _ = Color.objects.get_or_create(slug=slug, defaults={'name': name, 'hex_code': hex_code})
        color_objs.append(c)

    # Create dummy image
    image_content = b"fake_image_data"

    # Products
    products_data = [
        (brand1, "Essential Cotton Crewneck", "A soft, everyday cotton t-shirt.", cat_tops, pt_tshirt, "29.99"),
        (brand1, "Slim Fit Selvedge Denim", "Premium raw denim jeans.", cat_bottoms, pt_jeans, "89.50"),
        (brand2, "Elegant Evening Gown", "Silk blend maxi dress.", cat_dresses, pt_dress, "295.00"),
        (brand2, "Tailored Wool Blazer", "Modern fit wool suit jacket.", cat_tops, pt_jacket, "199.00"),
    ]

    for brand, name, desc, cat, p_type, price in products_data:
        prod, created = Product.objects.get_or_create(
            brand=brand,
            name=name,
            defaults={'description': desc, 'category': cat, 'product_type': p_type, 'price': Decimal(price)}
        )

        if created:
            # Create a few variants
            sampled_colors = random.sample(color_objs, 2)
            for color in sampled_colors:
                for size in size_objs[1:4]: # S, M, L
                    # Fake Image
                    img = SimpleUploadedFile(f"{prod.id}_{color.slug}.jpg", image_content, content_type="image/jpeg")
                    variant = ProductVariant.objects.create(
                        product=prod, color=color, size=size, image=img
                    )
                    
                    # Stock Levels
                    StockLevel.objects.create(
                        location=loc1 if brand == brand1 else loc3,
                        product_variant=variant,
                        quantity=random.randint(10, 100)
                    )
                    if brand == brand1:
                        StockLevel.objects.create(
                            location=loc2,
                            product_variant=variant,
                            quantity=random.randint(50, 500)
                        )

    print("Data seeded successfully!")

if __name__ == "__main__":
    run()
