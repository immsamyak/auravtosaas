import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from apps.brands.models import Brand
from apps.catalog.models import Product, ProductVariant
from apps.inventory.models import StockLevel, Location
from apps.orders.models import Order, OrderItem
from apps.core.utils import notify

@login_required
def pos_terminal_view(request):
    """
    Main full-screen POS cashier interface.
    """
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
    from apps.catalog.models import Category
    from apps.brands.models import BrandIntegration
    
    categories = Category.objects.filter(brand=brand)
    
    # Get Custom Manual Payment QR code if active
    qr_code_url = None
    custom_payment = BrandIntegration.objects.filter(brand=brand, integration__provider_code='CUSTOM_MANUAL', is_active=True).first()
    if custom_payment:
        qr_code_url = custom_payment.credentials.get('qr_code_url')
        
    has_review_qr = True
    has_wifi_qr = True
    
    return render(request, 'pos/terminal.html', {
        'brand': brand,
        'currency_symbol': brand.get_currency_symbol,
        'categories': categories,
        'qr_code_url': qr_code_url,
        'has_review_qr': has_review_qr,
        'has_wifi_qr': has_wifi_qr,
    })

@login_required
def pos_customer_display_view(request):
    """
    Customer Facing Display (CFD) synced via localStorage.
    """
    # Multi-tenant Team Management Check
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')
        
    from apps.brands.models import BrandIntegration
    from django.urls import reverse
    import urllib.parse
    
    # Get Custom Manual Payment QR code if active
    payment_qr_url = None
    custom_payment = BrandIntegration.objects.filter(brand=brand, integration__provider_code='CUSTOM_MANUAL', is_active=True).first()
    if custom_payment:
        payment_qr_url = custom_payment.credentials.get('qr_code_url')
        
    # Generate Store QR Code
    store_url = request.build_absolute_uri(reverse('store', kwargs={'brand_slug': brand.slug}))
    store_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(store_url)}"
    
    # Check Settings for Review and WiFi
    review_qr_url = None
    wifi_qr_url = None
    settings = getattr(brand, 'settings', None)
    
    review_link = settings.google_review_url if (settings and settings.google_review_url) else "https://g.page/review"
    review_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(review_link)}"
    
    wifi_ssid = settings.wifi_network_name if (settings and settings.wifi_network_name) else "Guest_WiFi"
    wifi_pass = settings.wifi_password if (settings and settings.wifi_password) else "password"
    wifi_str = f"WIFI:S:{wifi_ssid};T:WPA;P:{wifi_pass};;"
    wifi_qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={urllib.parse.quote(wifi_str)}"
        
    return render(request, 'pos/customer_display.html', {
        'brand': brand,
        'currency_symbol': brand.get_currency_symbol,
        'payment_qr_url': payment_qr_url,
        'store_qr_url': store_qr_url,
        'review_qr_url': review_qr_url,
        'wifi_qr_url': wifi_qr_url,
    })

@login_required
def pos_api_products(request):
    """
    API endpoint for the POS to fetch products/variants instantly.
    """
    try:
        brand = request.user.owned_brand
    except Brand.DoesNotExist:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category_id')
    
    from apps.catalog.models import Product
    products_qs = Product.objects.filter(brand=brand, is_active=True).prefetch_related('variants__color', 'variants__size', 'images')
    
    if query:
        products_qs = products_qs.filter(
            Q(name__icontains=query)
        ).distinct()
    elif category_id:
        products_qs = products_qs.filter(category_id=category_id)
        
    products_qs = products_qs[:50]
    
    results = []
    for p in products_qs:
        # Get product image
        primary_img = p.images.filter(is_primary=True).first() or p.images.first()
        prod_img_url = primary_img.image.url if (primary_img and getattr(primary_img, 'image', None) and primary_img.image.name) else None
        
        if not prod_img_url:
            # Fallback to the first variant's image if the main product has no image
            first_v = p.variants.exclude(image='').first()
            if first_v and first_v.image and first_v.image.name:
                prod_img_url = first_v.image.url
                
        variant_list = []
        total_stock = 0
        
        for v in p.variants.all():
            stock = StockLevel.objects.filter(product_variant=v, location__brand=brand).first()
            stock_qty = stock.quantity if stock else 0
            total_stock += stock_qty
            
            v_img = v.image.url if (v.image and v.image.name) else prod_img_url
            
            variant_list.append({
                'id': v.id,
                'name': f"{v.size.code} - {v.color.name}",
                'sku': f"{p.id}-{v.id}",
                'price': float(p.price),
                'stock': stock_qty,
                'image': v_img,
                'size': v.size.code,
                'color': v.color.name,
                'hex': v.color.hex_code
            })
            
        results.append({
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'image': prod_img_url,
            'total_stock': total_stock,
            'variants': variant_list
        })
        
    return JsonResponse({'products': results})

from django.contrib.auth.models import User

@login_required
def pos_lookup_customer_api(request):
    """
    Looks up a customer by phone or email globally to link to the POS order.
    """
    try:
        brand = request.user.owned_brand
    except Brand.DoesNotExist:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    query = request.GET.get('q', '').strip()
    if not query or len(query) < 4:
        return JsonResponse({'error': 'Query too short'}, status=400)
        
    # Search by email or phone
    from apps.accounts.models import ConsumerProfile
    
    users = User.objects.filter(Q(email__iexact=query) | Q(username__iexact=query))
    if not users.exists():
        profiles = ConsumerProfile.objects.filter(phone_number=query)
        if profiles.exists():
            users = [profiles.first().user]
            
    if users:
        user = users[0] if isinstance(users, list) else users.first()
        profile = getattr(user, 'profile', None)
        return JsonResponse({
            'success': True,
            'customer': {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'email': user.email,
                'phone': profile.phone_number if profile else None
            }
        })
        
    return JsonResponse({'success': False, 'message': 'Customer not found'})

@login_required
def pos_checkout_api(request):
    """
    Finalizes the POS order, deducts stock.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=405)
        
    try:
        brand = request.user.owned_brand
    except Brand.DoesNotExist:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    try:
        data = json.loads(request.body)
        cart_items = data.get('items', [])
        payment_method = data.get('payment_method', 'CASH')
        customer_name = data.get('customer_name', 'Walk-in Customer')
        customer_phone = data.get('customer_phone', '')
        customer_id = data.get('customer_id', None)
        discount = float(data.get('discount', 0))
        
        if not cart_items:
            return JsonResponse({'error': 'Cart is empty'}, status=400)
            
        # Optional: create or link user
        linked_user = None
        if customer_id:
            linked_user = User.objects.filter(id=customer_id).first()
            if linked_user:
                customer_name = linked_user.get_full_name() or linked_user.username
            
        # Create Order
        total_amount = 0
        order_status = 'DRAFT' if payment_method == 'DRAFT' else 'COMPLETED'
        payment_prov = 'NONE' if payment_method == 'DRAFT' else payment_method
        
        # If they are replacing an old draft, delete it first
        draft_id = data.get('draft_id')
        if draft_id:
            old_draft = Order.objects.filter(id=draft_id, brand=brand, status='DRAFT').first()
            if old_draft:
                old_draft.delete()
        
        coupon = None
        coupon_code = data.get('coupon_code')
        if coupon_code:
            from apps.brands.models import Coupon
            coupon = Coupon.objects.filter(brand=brand, code__iexact=coupon_code, is_active=True).first()
            if coupon:
                coupon.times_used += 1
                coupon.save()
                    
        order = Order.objects.create(
            brand=brand,
            user=linked_user,
            customer_name=customer_name,
            customer_phone=customer_phone,
            payment_provider=payment_prov,
            status=order_status,
            coupon=coupon,
            shipping_cost=0,
            total_amount=0
        )
        
        primary_location = Location.objects.filter(brand=brand).first()
        
        for item in cart_items:
            variant_id = item.get('id')
            quantity = int(item.get('quantity', 1))
            price = float(item.get('price', 0))
            
            variant = ProductVariant.objects.get(id=variant_id, product__brand=brand)
            
            # 1. Add item
            OrderItem.objects.create(
                order=order,
                product_variant=variant,
                quantity=quantity,
                price_at_purchase=price
            )
            total_amount += (price * quantity)
            
            # 2. Deduct stock instantly (only if not draft)
            if order_status == 'COMPLETED' and primary_location:
                stock, _ = StockLevel.objects.get_or_create(product_variant=variant, location=primary_location, defaults={'quantity': 0})
                stock.quantity = max(0, stock.quantity - quantity)
                stock.save()
                
                # Low stock alert
                if stock.quantity < 5:
                    notify(
                        user=brand.owner,
                        title="Low Stock Alert (POS)",
                        message=f"{variant.product.name} ({variant.size.code}) dropped to {stock.quantity} after POS sale.",
                        icon_class="fa-solid fa-triangle-exclamation text-rose-500",
                        action_url=f"/dashboard/products/{variant.product.id}/"
                    )
                    
        # Apply discount and Tax
        subtotal = max(0, total_amount - discount)
        
        tax_rate = getattr(brand.settings, 'tax_rate', 0.00)
        tax_amount = round(subtotal * (float(tax_rate) / 100.0), 2)
        
        order.total_amount = total_amount
        order.discount_amount = discount
        order.tax_rate = tax_rate
        order.tax_amount = tax_amount
        order.save()
        
        return JsonResponse({
            'success': True,
            'order_id': order.id,
            'message': 'Transaction complete!' if order_status == 'COMPLETED' else 'Draft saved!'
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def pos_api_drafts(request):
    """
    GET: Returns list of drafted orders
    DELETE: Deletes a drafted order
    """
    try:
        brand = request.user.owned_brand
    except Brand.DoesNotExist:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
        
    if request.method == 'GET':
        drafts = Order.objects.filter(brand=brand, status='DRAFT').order_by('-created_at')
        draft_list = []
        for d in drafts:
            items = []
            for item in d.items.all():
                items.append({
                    'id': item.product_variant.id,
                    'product_name': item.product_variant.product.name,
                    'color_name': item.product_variant.color.name if item.product_variant.color else '',
                    'size_code': item.product_variant.size.code if item.product_variant.size else '',
                    'price': float(item.price_at_purchase),
                    'quantity': item.quantity,
                    'image': item.product_variant.product.images.first().image.url if item.product_variant.product.images.exists() else None
                })
            
            # Simple discount deduction (total_amount is already discounted)
            subtotal = sum(i['price'] * i['quantity'] for i in items)
            discount = float(subtotal) - float(d.total_amount)
            if discount < 0: discount = 0
            
            draft_list.append({
                'id': d.id,
                'customer_name': d.customer_name,
                'customer_phone': d.customer_phone,
                'customer_id': d.user.id if d.user else None,
                'total_amount': float(d.total_amount),
                'discount': discount,
                'items': items,
                'created_at': d.created_at.strftime('%I:%M %p')
            })
        return JsonResponse({'drafts': draft_list})
        
    elif request.method == 'DELETE':
        try:
            data = json.loads(request.body)
            draft_id = data.get('id')
            draft = Order.objects.filter(id=draft_id, brand=brand, status='DRAFT').first()
            if draft:
                draft.delete()
                return JsonResponse({'success': True})
            return JsonResponse({'error': 'Draft not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Method not allowed'}, status=405)
