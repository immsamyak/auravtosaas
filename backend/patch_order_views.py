import re

filepath = 'apps/orders/views.py'
with open(filepath, 'r') as f:
    content = f.read()

# Storefront Checkout View
checkout_pattern = re.compile(r"    theme_base = f\"storefront/\{brand\.theme\.template_folder\}/base\.html\" if brand\.theme and brand\.theme\.is_active else \"brands/store_base\.html\"\n\s+return render\(request, \'orders/checkout\.html\', \{")
checkout_replacement = """    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    template_name = f"storefront/{brand.theme.template_folder}/checkout.html" if brand.theme and brand.theme.is_active else 'orders/checkout.html'
            
    return render(request, template_name, {"""
content = checkout_pattern.sub(checkout_replacement, content)

# Order Success View
success_pattern = re.compile(r"    theme_base = f\"storefront/\{brand\.theme\.template_folder\}/base\.html\" if brand\.theme and brand\.theme\.is_active else \"brands/store_base\.html\"\n\s+return render\(request, \'orders/order_success\.html\', \{")
success_replacement = """    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    template_name = f"storefront/{brand.theme.template_folder}/order_success.html" if brand.theme and brand.theme.is_active else 'orders/order_success.html'
            
    return render(request, template_name, {"""
content = success_pattern.sub(success_replacement, content)

# Track Order View
track_pattern = re.compile(r"    theme_base = f\"storefront/\{brand\.theme\.template_folder\}/base\.html\" if brand\.theme and brand\.theme\.is_active else \"brands/store_base\.html\"\n\s+return render\(request, \'orders/track_order\.html\', \{")
track_replacement = """    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    template_name = f"storefront/{brand.theme.template_folder}/track_order.html" if brand.theme and brand.theme.is_active else 'orders/track_order.html'
            
    return render(request, template_name, {"""
content = track_pattern.sub(track_replacement, content)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated apps/orders/views.py")
