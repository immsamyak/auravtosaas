filepath = 'apps/orders/views.py'
with open(filepath, 'r') as f:
    content = f.read()

target1 = """        if not cart_items:
            return HttpResponse("Cart is empty", status=400)"""

replacement1 = """        if not cart_items:
            from django.contrib import messages
            messages.error(request, "Your cart is empty.")
            return redirect('storefront_checkout', brand_slug=brand.slug)"""

target2 = """                if item_variant.total_stock < qty:
                    return HttpResponse(f"Insufficient stock for {item_variant.product.name}", status=400)"""

replacement2 = """                if item_variant.total_stock < qty:
                    from django.contrib import messages
                    messages.error(request, f"Insufficient stock for {item_variant.product.name} ({item_variant.size.code}). Only {item_variant.total_stock} left.")
                    return redirect('storefront_checkout', brand_slug=brand.slug)"""

target3 = """        if not validated_items:
            return HttpResponse("Invalid items in cart", status=400)"""

replacement3 = """        if not validated_items:
            from django.contrib import messages
            messages.error(request, "Invalid items in cart.")
            return redirect('storefront_checkout', brand_slug=brand.slug)"""


if target1 in content:
    content = content.replace(target1, replacement1)
if target2 in content:
    content = content.replace(target2, replacement2)
if target3 in content:
    content = content.replace(target3, replacement3)

with open(filepath, 'w') as f:
    f.write(content)
