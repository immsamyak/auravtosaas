import re

filepath = 'apps/brands/views.py'
with open(filepath, 'r') as f:
    content = f.read()

replacement = """    from apps.catalog.models import ProductImage, ProductVariant
    product_images = ProductImage.objects.filter(product__brand=brand).order_by('-id')
    product_variants = ProductVariant.objects.filter(product__brand=brand).exclude(image='').order_by('-id')
    
    return render(request, 'brands/media_gallery.html', {
        'brand': brand,
        'assets': assets,
        'product_images': product_images,
        'product_variants': product_variants,
    })"""

pattern = re.compile(r'    from apps\.catalog\.models import ProductImage\n    product_images = ProductImage\.objects\.filter\(product__brand=brand\)\.order_by\(\'-id\'\)\n\s+return render\(request, \'brands/media_gallery\.html\', \{\n        \'brand\': brand,\n        \'assets\': assets,\n        \'product_images\': product_images,\n    \}\)')

if pattern.search(content):
    content = pattern.sub(replacement, content)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched apps/brands/views.py successfully.")
else:
    print("Pattern not found in apps/brands/views.py!")
