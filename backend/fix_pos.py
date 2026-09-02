filepath = 'apps/orders/views_pos.py'
with open(filepath, 'r') as f:
    content = f.read()

target_validation = """        # 2. Validate Items & Calculate Totals
        for item in cart_items:
            try:
                variant = ProductVariant.objects.get(id=item.get('id'), product__brand=brand)
                qty = int(item.get('quantity', 1))
                
                # Fetch stock to ensure it's recorded properly (optional strict check)
                stock = StockLevel.objects.filter(product_variant=variant, location__brand=brand).first()"""

replacement_validation = """        # 2. Validate Items & Calculate Totals
        for item in cart_items:
            try:
                variant = ProductVariant.objects.get(id=item.get('id'), product__brand=brand)
                qty = int(item.get('quantity', 1))
                
                # STOCK VALIDATION
                if variant.total_stock < qty:
                    return JsonResponse({'success': False, 'error': f"Insufficient stock for {variant.product.name}"}, status=400)
                    
                # Fetch stock to ensure it's recorded properly (optional strict check)
                stock = StockLevel.objects.filter(product_variant=variant, location__brand=brand).first()"""

target_creation = """            stock = StockLevel.objects.filter(product_variant=v, location__brand=brand).first()
            if stock and stock.quantity >= q:
                stock.quantity -= q
                stock.save()"""

replacement_creation = """            remaining_q = q
            stocks = StockLevel.objects.filter(product_variant=v, location__brand=brand, quantity__gt=0).order_by('-quantity')
            for stock in stocks:
                if remaining_q <= 0:
                    break
                deduct = min(stock.quantity, remaining_q)
                stock._audit_action = 'POS'
                stock._audit_reference = str(order.id)
                stock._audit_notes = "POS Terminal Sale"
                stock.quantity -= deduct
                stock.save()
                remaining_q -= deduct"""


if target_validation in content:
    content = content.replace(target_validation, replacement_validation)
if target_creation in content:
    content = content.replace(target_creation, replacement_creation)

with open(filepath, 'w') as f:
    f.write(content)
