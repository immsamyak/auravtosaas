from django.shortcuts import render, redirect, get_object_or_404
from apps.orders.services.notifications import NotificationDispatcher
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from apps.brands.models import Brand, BrandIntegration
from apps.orders.models import Order, ReturnRequest
from apps.orders.services.payment_gateways import EsewaService, KhaltiService
import json
import base64
from decimal import Decimal
from django.urls import reverse

@login_required(login_url='/login/')
def manage_orders_view(request):
    """
    Brand Owner view to manage orders.
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

    if request.method == 'POST':
        action = request.POST.get('action')
        order_id = request.POST.get('order_id')
        order = get_object_or_404(Order, id=order_id, brand=brand)

        if action == 'verify_payment':
            order.status = 'PAID'
            order.save()
            messages.success(request, f"Payment for Order #{str(order.id)[:8]} verified successfully.")
        elif action == 'update_status':
            new_status = request.POST.get('new_status')
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                if new_status == 'SENT_TO_COURIER':
                    manual_tracking = request.POST.get('manual_tracking_number')
                    manual_courier = request.POST.get('manual_courier')
                    if manual_tracking:
                        order.tracking_number = manual_tracking
                    if manual_courier:
                        order.shipping_provider = manual_courier
                order.save()
                messages.success(request, f"Order #{str(order.id)[:8]} status updated to {dict(Order.STATUS_CHOICES).get(new_status)}.")
            else:
                messages.error(request, "Invalid status selected.")
        elif action == 'dispatch_order':
            shipping_provider_code = request.POST.get('shipping_provider')
            if shipping_provider_code:
                # Dispatch the order through the selected logistics integration
                bi = BrandIntegration.objects.filter(brand=brand, integration__provider_code=shipping_provider_code, is_active=True).first()
                if bi:
                    from apps.orders.services.shipping_providers import LogisticsService
                    result = LogisticsService.dispatch_order(order, bi)
                    if result.get('success'):
                        order.status = 'SENT_TO_COURIER'
                        order.shipping_provider = shipping_provider_code
                        order.tracking_number = result.get('tracking_number')
                        order.save()
                        messages.success(request, f"Order #{str(order.id)[:8]} dispatched via {bi.integration.name}. Tracking ID: {order.tracking_number}")
                    else:
                        messages.error(request, f"Dispatch failed: {result.get('error')}")
                else:
                    messages.error(request, "Selected shipping provider is not active.")
            else:
                messages.error(request, "No shipping provider selected.")
        elif action == 'cancel_order':
            if order.status in ['PENDING', 'PAID', 'PROCESSING']:
                order.status = 'CANCELLED'
                order.save()
                messages.success(request, f"Order #{str(order.id)[:8]} has been cancelled successfully.")
            else:
                messages.error(request, f"Order #{str(order.id)[:8]} cannot be cancelled as it is already {order.status.lower()}.")
                
        return redirect('manage_orders')

    orders_qs = Order.objects.filter(brand=brand).order_by('-created_at')
    
    # --- Stat cards ---
    from django.db.models import Count
    total_count = orders_qs.count()
    pending_count = orders_qs.filter(status='PENDING').count()
    paid_count = orders_qs.filter(status='PAID').count()
    shipped_count = orders_qs.filter(status='SHIPPED').count()
    delivered_count = orders_qs.filter(status='DELIVERED').count()
    
    # --- Filtering ---
    filter_status = request.GET.get('status', '')
    filter_search = request.GET.get('q', '')
    
    filtered_qs = orders_qs
    if filter_status:
        filtered_qs = filtered_qs.filter(status=filter_status)
    if filter_search:
        from django.db.models import Q
        filtered_qs = filtered_qs.filter(
            Q(customer_name__icontains=filter_search) |
            Q(customer_phone__icontains=filter_search) |
            Q(id__icontains=filter_search)
        )
    
    # --- Pagination ---
    from django.core.paginator import Paginator
    paginator = Paginator(filtered_qs, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Get active shipping integrations
    active_shipping_methods = BrandIntegration.objects.filter(
        brand=brand, 
        integration__category='SHIPPING', 
        is_active=True
    ).select_related('integration')
    
    return render(request, 'orders/manage_orders.html', {
        'brand': brand,
        'orders': page_obj,
        'page_obj': page_obj,
        'active_shipping_methods': active_shipping_methods,
        'total_count': total_count,
        'pending_count': pending_count,
        'paid_count': paid_count,
        'shipped_count': shipped_count,
        'delivered_count': delivered_count,
        'filter_status': filter_status,
        'filter_search': filter_search,
    })

@login_required(login_url='/login/')
def returns_list_view(request):
    """
    Brand Owner view to manage Return Requests (RMA).
    """
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')

    if request.method == 'POST':
        return_id = request.POST.get('return_id')
        new_status = request.POST.get('status')
        if return_id and new_status:
            try:
                ret = ReturnRequest.objects.get(id=return_id, brand=brand)
                ret.status = new_status
                ret.save()
                messages.success(request, f"Return RMA-{ret.id} status updated to {ret.get_status_display()}.")
            except ReturnRequest.DoesNotExist:
                messages.error(request, "Return request not found.")
        return redirect('returns_list')

    returns = ReturnRequest.objects.filter(brand=brand).order_by('-created_at')
    
    return render(request, 'orders/returns_list.html', {
        'brand': brand,
        'returns': returns,
        'status_choices': ReturnRequest.STATUS_CHOICES
    })

@login_required(login_url='/login/')
def abandoned_carts_view(request):
    """
    Brand Owner view to manage Abandoned Carts.
    """
    brand = None
    if hasattr(request.user, 'owned_brand') and request.user.owned_brand:
        brand = request.user.owned_brand
    else:
        staff = request.user.brand_roles.select_related('brand').first()
        if staff:
            brand = staff.brand
            
    if not brand:
        return redirect('index')

    from datetime import timedelta
    from django.utils import timezone
    from apps.orders.models import Cart
    
    # Consider carts abandoned if they are older than 2 hours and have items
    threshold_time = timezone.now() - timedelta(hours=2)
    carts = Cart.objects.filter(brand=brand, updated_at__lte=threshold_time).exclude(items__isnull=True).order_by('-updated_at').prefetch_related('items', 'items__product_variant')
    
    return render(request, 'orders/abandoned_carts.html', {
        'brand': brand,
        'carts': carts,
    })

from apps.catalog.models import ProductVariant
from apps.orders.models import OrderItem
from apps.orders.services.shipping_providers import LogisticsService

def storefront_checkout_view(request, brand_slug):
    """
    Consumer facing checkout view.
    """
    brand = get_object_or_404(Brand, slug=brand_slug)
    
    if brand.status == 'MAINTENANCE':
        return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE':
        return render(request, 'brands/store_inactive.html', {'brand': brand})
    
    # Get active integrations for this brand
    active_integrations = BrandIntegration.objects.filter(brand=brand, is_active=True).select_related('integration')
    payment_methods = [bi for bi in active_integrations if bi.integration.category == 'PAYMENT']
    shipping_methods = [bi for bi in active_integrations if bi.integration.category == 'SHIPPING']
    
    # Get owner-configured delivery hierarchy
    from apps.orders.models import DeliveryProvince
    provinces = DeliveryProvince.objects.filter(brand=brand).prefetch_related('districts__cities')
    
    # Build JSON for Alpine.js dynamic pricing
    import json as json_module
    
    hierarchy_data = []
    for prov in provinces:
        prov_data = {
            'id': prov.id,
            'name': prov.name,
            'districts': []
        }
        for dist in prov.districts.all():
            dist_data = {
                'id': dist.id,
                'name': dist.name,
                'cities': []
            }
            for city in dist.cities.filter(is_active=True):
                dist_data['cities'].append({
                    'id': city.id,
                    'name': city.name,
                    'rate': str(city.rate),
                    'estimated_days': city.estimated_days or '',
                    'is_free_above': str(city.is_free_above) if city.is_free_above else None,
                })
            prov_data['districts'].append(dist_data)
        hierarchy_data.append(prov_data)
        
    locations_json = json_module.dumps(hierarchy_data)
    
    if request.method == 'POST' and 'customer_name' in request.POST:
        customer_name = request.POST.get('customer_name')
        customer_email = request.POST.get('customer_email', '')
        customer_phone = request.POST.get('customer_phone')
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method') # provider_code
        shipping_method = request.POST.get('shipping_method') # provider_code
        delivery_city_id = request.POST.get('delivery_city')
        
        # Handle Cart Data
        cart_data_str = request.POST.get('cart_data', '[]')
        try:
            cart_items = json_module.loads(cart_data_str)
        except json_module.JSONDecodeError:
            cart_items = []
            
        if not cart_items:
            from django.contrib import messages
            messages.error(request, "Your cart is empty.")
            return redirect('storefront_checkout', brand_slug=brand.slug)
            
        # Validate variants and calculate base total
        total_items_price = 0
        validated_items = []
        for item in cart_items:
            try:
                item_variant = ProductVariant.objects.get(id=item.get('id'), product__brand=brand)
                qty = int(item.get('quantity', 1))
                
                # STOCK VALIDATION
                if item_variant.total_stock < qty:
                    from django.contrib import messages
                    messages.error(request, f"Insufficient stock for {item_variant.product.name} ({item_variant.size.code}). Only {item_variant.total_stock} left.")
                    return redirect('storefront_checkout', brand_slug=brand.slug)
                    
                total_items_price += item_variant.product.price * qty
                validated_items.append({
                    'variant': item_variant,
                    'quantity': qty,
                    'price': item_variant.product.price
                })
            except (ProductVariant.DoesNotExist, ValueError, TypeError):
                continue
                
        if not validated_items:
            from django.contrib import messages
            messages.error(request, "Invalid items in cart.")
            return redirect('storefront_checkout', brand_slug=brand.slug)

        # Calculate shipping cost from city
        shipping_cost = 0
        selected_city = None
        if delivery_city_id:
            try:
                from apps.orders.models import DeliveryCity
                selected_city = DeliveryCity.objects.get(id=delivery_city_id, district__province__brand=brand)
                shipping_cost = selected_city.rate
                # Check free shipping threshold
                if selected_city.is_free_above and total_items_price >= selected_city.is_free_above:
                    shipping_cost = 0
            except DeliveryCity.DoesNotExist:
                pass
        
        from django.contrib.auth.models import User
        from django.contrib.auth import login
        from apps.accounts.models import ConsumerProfile
        import uuid

        checkout_user = request.user if request.user.is_authenticated else None

        if not checkout_user and customer_email:
            # Auto-create or login customer
            user, created = User.objects.get_or_create(
                email=customer_email,
                defaults={
                    'username': customer_email.split('@')[0] + str(uuid.uuid4())[:8],
                    'first_name': customer_name
                }
            )
            if created:
                user.set_password(User.objects.make_random_password())
                user.save()
                ConsumerProfile.objects.create(user=user)
            
            # Automatically log the user in to associate them with the session
            checkout_user = user
            login(request, user)
            
        # Ensure BrandCustomer exists
        b2b_customer_record = None
        if checkout_user:
            from apps.brands.models import BrandCustomer
            b2b_customer_record, _ = BrandCustomer.objects.get_or_create(brand=brand, user=checkout_user)

        # Base Discount Initialization
        discount_amount = Decimal('0.00')

        # Handle B2B Wholesale Discount
        if b2b_customer_record and b2b_customer_record.is_b2b:
            if brand.subscription and brand.subscription.plan and brand.subscription.plan.allow_b2b_wholesale:
                if brand.b2b_discount_percent > 0:
                    b2b_discount = (total_items_price * brand.b2b_discount_percent) / Decimal('100.00')
                    discount_amount += b2b_discount

        # Handle Coupon
        coupon_code = request.POST.get('applied_coupon')
        applied_coupon = None
        
        if coupon_code:
            from apps.brands.models import Coupon
            try:
                c = Coupon.objects.get(brand=brand, code=coupon_code, is_active=True)
                if c.max_uses == 0 or c.times_used < c.max_uses:
                    if c.min_order_value <= total_items_price:
                        # Apply coupon
                        if c.discount_type == 'PERCENTAGE':
                            discount_amount += (total_items_price * c.discount_value) / Decimal('100.00')
                        else:
                            discount_amount += c.discount_value
                        
                        applied_coupon = c
                        c.times_used += 1
                        c.save()
            except Coupon.DoesNotExist:
                pass

        # 1. Create Order
        order = Order.objects.create(
            brand=brand,
            user=checkout_user,
            customer_name=customer_name,
            customer_phone=customer_phone,
            shipping_address=shipping_address,
            total_amount=total_items_price,
            shipping_cost=shipping_cost,
            delivery_city=selected_city,
            coupon=applied_coupon,
            discount_amount=discount_amount,
            payment_provider=payment_method,
            shipping_provider=shipping_method
        )
        
        # 2. Create Order Items & Deduct Stock
        from apps.inventory.models import StockLevel
        from apps.core.utils import notify
        
        for item in validated_items:
            v = item['variant']
            q = item['quantity']
            
            OrderItem.objects.create(
                order=order,
                product_variant=v,
                quantity=q,
                price_at_purchase=item['price']
            )
            
            # Decrement stock and audit log
            # We decrement from the first location that has enough stock, or split it if necessary.
            # For simplicity, we just decrement from the primary location with stock.
            remaining_q = q
            stocks = StockLevel.objects.filter(product_variant=v, location__brand=brand, quantity__gt=0).order_by('-quantity')
            for stock in stocks:
                if remaining_q <= 0:
                    break
                deduct = min(stock.quantity, remaining_q)
                stock._audit_action = 'ORDER'
                stock._audit_reference = str(order.id)
                stock._audit_notes = f"Order Fulfillment for {order.customer_name}"
                stock.quantity -= deduct
                stock.save()
                remaining_q -= deduct
                
                if stock.quantity < 5 and brand.owner:
                    notify(
                        user=brand.owner,
                        title="Low Stock Alert",
                        message=f"{v.product.name} ({v.size.code}) is running low! Only {stock.quantity} left in {stock.location.name}.",
                        icon_class="fa-solid fa-triangle-exclamation text-rose-500",
                        action_url=f"/dashboard/products/{v.product.id}/"
                    )
        
        # Notify owner of new order
        if brand.owner:
            notify(
                user=brand.owner,
                title="New Order Received!",
                message=f"Order #{order.id} for {brand.currency_symbol or '$'}{order.total_amount + order.shipping_cost} from {order.customer_name}.",
                icon_class="fa-solid fa-cart-shopping text-emerald-500",
                action_url="/dashboard/orders/"
            )
        
        # 3. Dispatch Logistics if automatic fulfillment is configured for this shipping method
        if shipping_method:
            shipping_bi = next((bi for bi in shipping_methods if bi.integration.provider_code == shipping_method), None)
            if shipping_bi:
                logistics_result = LogisticsService.dispatch_order(order, shipping_bi)
                if logistics_result.get('success'):
                    order.tracking_number = logistics_result.get('tracking_number')
                    order.save()
                    
        # 4. Route to Payment
        if payment_method == 'ESEWA':
            esewa_bi = next((bi for bi in payment_methods if bi.integration.provider_code == 'ESEWA'), None)
            # Create form logic for eSewa
            return EsewaService.initiate_payment(order, esewa_bi, request)
        elif payment_method == 'KHALTI':
            khalti_bi = next((bi for bi in payment_methods if bi.integration.provider_code == 'KHALTI'), None)
            response = KhaltiService.initiate_payment(order, khalti_bi, request)
            if response.get('success'):
                return redirect(response.get('payment_url'))
            else:
                return HttpResponse(f"Khalti Error: {response.get('error')}", status=400)
        elif payment_method == 'STRIPE':
            stripe_bi = next((bi for bi in payment_methods if bi.integration.provider_code == 'STRIPE'), None)
            from apps.orders.services.payment_gateways import StripeService
            response = StripeService.initiate_payment(order, stripe_bi, request)
            if response.get('success'):
                return redirect(response.get('payment_url'))
            else:
                return HttpResponse(f"Stripe Error: {response.get('error')}", status=400)
        elif payment_method == 'PAYPAL':
            paypal_bi = next((bi for bi in payment_methods if bi.integration.provider_code == 'PAYPAL'), None)
            from apps.orders.services.payment_gateways import PayPalService
            response = PayPalService.initiate_payment(order, paypal_bi, request)
            if response.get('success'):
                return redirect(response.get('payment_url'))
            else:
                return HttpResponse(f"PayPal Error: {response.get('error')}", status=400)
        elif payment_method == 'RAZORPAY':
            razorpay_bi = next((bi for bi in payment_methods if bi.integration.provider_code == 'RAZORPAY'), None)
            from apps.orders.services.payment_gateways import RazorpayService
            response = RazorpayService.initiate_payment(order, razorpay_bi, request)
            if response.get('success'):
                return redirect(response.get('payment_url'))
            else:
                return HttpResponse(f"Razorpay Error: {response.get('error')}", status=400)
        else:
            # Custom/Manual or unknown
            return redirect('order_success', order_id=order.id)
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    template_name = f"storefront/{brand.theme.template_folder}/checkout.html" if brand.theme and brand.theme.is_active else 'orders/checkout.html'
    
    import json
    stock_dict = {str(v.id): v.total_stock for v in ProductVariant.objects.filter(product__brand=brand)}
    stock_json = json.dumps(stock_dict)

    return render(request, template_name, {
        'brand': brand,
        'payment_methods': payment_methods,
        'shipping_methods': shipping_methods,
        'locations_json': locations_json,
        'stock_json': stock_json,
        'theme_base': theme_base
    })

def order_success_view(request, order_id):
    """
    Consumer facing success page.
    """
    order = get_object_or_404(Order, id=order_id)
    brand = order.brand
    
    # SECURITY FIX: Ensure the person viewing the success page is the one who placed the order
    if order.user and request.user != order.user:
        from django.http import Http404
        raise Http404("You do not have permission to view this order.")
    
    if request.method == 'POST' and 'payment_proof' in request.FILES:
        order.payment_proof = request.FILES['payment_proof']
        order.save()
        messages.success(request, "Payment proof uploaded successfully!")
        return redirect('order_success', order_id=order.id)
    
    # If custom payment, fetch the integration to show instructions again
    custom_instructions = None
    qr_code_url = None
    if order.payment_provider == 'CUSTOM_MANUAL':
        bi = BrandIntegration.objects.filter(brand=brand, integration__provider_code='CUSTOM_MANUAL').first()
        if bi and bi.credentials:
            custom_instructions = bi.credentials.get('instructions')
            qr_code_url = bi.credentials.get('qr_code_url')
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    template_name = f"storefront/{brand.theme.template_folder}/order_success.html" if brand.theme and brand.theme.is_active else 'orders/order_success.html'
            
    return render(request, template_name, {
        'brand': brand,
        'order': order,
        'custom_instructions': custom_instructions,
        'qr_code_url': qr_code_url,
        'theme_base': theme_base,
    })

def track_order_view(request, brand_slug):
    """
    Consumer facing track order view.
    """
    brand = get_object_or_404(Brand, slug=brand_slug)
    
    if brand.status == 'MAINTENANCE':
        return render(request, 'brands/store_maintenance.html', {'brand': brand})
    elif brand.status == 'INACTIVE':
        return render(request, 'brands/store_inactive.html', {'brand': brand})
        
    order = None
    error = None
    
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
    else:
        order_id = request.GET.get('order_id')
        
    if order_id:
        try:
            order = Order.objects.get(id=order_id, brand=brand)
        except (Order.DoesNotExist, ValueError):
            error = "Order not found. Please check your Order ID."
    theme_base = f"storefront/{brand.theme.template_folder}/base.html" if brand.theme and brand.theme.is_active else "brands/store_base.html"
    template_name = f"storefront/{brand.theme.template_folder}/track_order.html" if brand.theme and brand.theme.is_active else 'orders/track_order.html'
            
    return render(request, template_name, {
        'brand': brand,
        'order': order,
        'error': error,
        'theme_base': theme_base,
    })

def checkout_esewa_verify(request):
    """
    Callback URL for eSewa success.
    """
    encoded_data = request.GET.get('data')
    if not encoded_data:
        return HttpResponse("Missing eSewa payload.", status=400)
        
    try:
        decoded_bytes = base64.b64decode(encoded_data)
        data = json.loads(decoded_bytes.decode('utf-8'))
        transaction_uuid = data.get('transaction_uuid')
        
        order = get_object_or_404(Order, id=transaction_uuid)
        brand_integration = BrandIntegration.objects.filter(brand=order.brand, integration__provider_code='ESEWA').first()
        
        verification = EsewaService.verify_payment(encoded_data, brand_integration)
        
        if verification.get('success'):
            order.status = 'PAID'
            order.payment_provider = 'ESEWA'
            order.payment_reference_id = verification.get('transaction_code')
            order.save()
            NotificationDispatcher.dispatch_order_success(order)
            return redirect('order_success', order_id=order.id)
        else:
            return HttpResponse(f"Payment verification failed: {verification.get('error')}", status=400)
    except Exception as e:
        return HttpResponse(f"Error processing eSewa verification: {str(e)}", status=500)


def checkout_khalti_verify(request):
    """
    Callback URL for Khalti success.
    """
    pidx = request.GET.get('pidx')
    purchase_order_id = request.GET.get('purchase_order_id')
    
    if not pidx or not purchase_order_id:
        return HttpResponse("Missing Khalti payload.", status=400)
        
    order = get_object_or_404(Order, id=purchase_order_id)
    brand_integration = BrandIntegration.objects.filter(brand=order.brand, integration__provider_code='KHALTI').first()
    
    verification = KhaltiService.verify_payment(pidx, brand_integration)
    
    if verification.get('success'):
        order.status = 'PAID'
        order.payment_provider = 'KHALTI'
        order.payment_reference_id = verification.get('transaction_id')
        order.save()
        
        # Clear cart for the user
        from apps.orders.models import Cart
        Cart.objects.filter(user=order.user, brand=order.brand).delete()
        
        NotificationDispatcher.dispatch_order_success(order)
        return redirect('order_success', order_id=order.id)
    else:
        return HttpResponse(f"Khalti Verification Failed: {verification.get('error')}", status=400)

def checkout_stripe_verify(request):
    """
    Callback URL for Stripe success.
    """
    session_id = request.GET.get('session_id')
    order_id = request.GET.get('order_id')
    
    if not session_id or not order_id:
        return HttpResponse("Missing Stripe session or order data.", status=400)
        
    order = get_object_or_404(Order, id=order_id)
    brand_integration = BrandIntegration.objects.filter(brand=order.brand, integration__provider_code='STRIPE').first()
    
    if not brand_integration:
        return HttpResponse("Stripe integration not found for this brand.", status=400)
        
    from apps.orders.services.payment_gateways import StripeService
    verification = StripeService.verify_payment(session_id, brand_integration)
    
    if verification.get('success'):
        order.status = 'PAID'
        order.payment_provider = 'STRIPE'
        order.payment_reference_id = verification.get('transaction_id')
        order.save()
        
        # Clear cart for the user
        from apps.orders.models import Cart
        Cart.objects.filter(user=order.user, brand=order.brand).delete()
        
        NotificationDispatcher.dispatch_order_success(order)
        return redirect('order_success', order_id=order.id)
    else:
        return HttpResponse(f"Stripe Verification Failed: {verification.get('error')}", status=400)

@login_required(login_url='/login/')
def shipping_settings_view(request):
    """
    Owner dashboard view to manage shipping zones and rates.
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
    
    from apps.orders.models import DeliveryProvince, DeliveryDistrict, DeliveryCity
    import json
    import urllib.request
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'load_default_data':
            country_iso2 = request.POST.get('country_iso2')
            if country_iso2:
                try:
                    # Fetch combined data (countries + states + cities)
                    req = urllib.request.Request(
                        "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/json/countries%2Bstates%2Bcities.json",
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req) as url:
                        all_data = json.loads(url.read().decode())
                        
                    prov_created = 0
                    dist_created = 0
                    
                    country_data = next((c for c in all_data if c.get('iso2') == country_iso2), None)
                    if country_data:
                        for state in country_data.get('states', []):
                            prov, created = DeliveryProvince.objects.get_or_create(
                                brand=brand,
                                name=state.get('name')
                            )
                            if created: prov_created += 1
                            
                            for city in state.get('cities', []):
                                dist, d_created = DeliveryDistrict.objects.get_or_create(
                                    province=prov,
                                    name=city.get('name')
                                )
                                if d_created: dist_created += 1
                                
                    messages.success(request, f"Successfully loaded {prov_created} provinces and {dist_created} districts for {country_iso2}.")
                except Exception as e:
                    messages.error(request, f"Failed to load data: {str(e)}")
            return redirect('shipping_settings')

        
        # Province Actions
        if action == 'add_province':
            name = request.POST.get('name', '').strip()
            if name:
                DeliveryProvince.objects.create(brand=brand, name=name)
                messages.success(request, f'Province "{name}" added.')
                
        elif action == 'edit_province':
            prov_id = request.POST.get('province_id')
            prov = get_object_or_404(DeliveryProvince, id=prov_id, brand=brand)
            prov.name = request.POST.get('name', prov.name).strip()
            prov.save()
            messages.success(request, 'Province updated.')
            
        elif action == 'delete_province':
            prov_id = request.POST.get('province_id')
            prov = get_object_or_404(DeliveryProvince, id=prov_id, brand=brand)
            prov.delete()
            messages.success(request, 'Province deleted.')
            
        # District Actions
        elif action == 'add_district':
            prov_id = request.POST.get('province_id')
            name = request.POST.get('name', '').strip()
            if name and prov_id:
                prov = get_object_or_404(DeliveryProvince, id=prov_id, brand=brand)
                DeliveryDistrict.objects.create(province=prov, name=name)
                messages.success(request, f'District "{name}" added.')
                
        elif action == 'edit_district':
            dist_id = request.POST.get('district_id')
            dist = get_object_or_404(DeliveryDistrict, id=dist_id, province__brand=brand)
            dist.name = request.POST.get('name', dist.name).strip()
            dist.save()
            messages.success(request, 'District updated.')
            
        elif action == 'delete_district':
            dist_id = request.POST.get('district_id')
            dist = get_object_or_404(DeliveryDistrict, id=dist_id, province__brand=brand)
            dist.delete()
            messages.success(request, 'District deleted.')
            
        # City Actions
        elif action == 'add_city':
            dist_id = request.POST.get('district_id')
            name = request.POST.get('name', '').strip()
            rate = request.POST.get('rate', '0')
            estimated_days = request.POST.get('estimated_days', '').strip()
            is_free_above = request.POST.get('is_free_above', '').strip()
            
            if name and dist_id:
                dist = get_object_or_404(DeliveryDistrict, id=dist_id, province__brand=brand)
                DeliveryCity.objects.create(
                    district=dist,
                    name=name,
                    rate=rate,
                    estimated_days=estimated_days or None,
                    is_free_above=is_free_above if is_free_above else None,
                    is_active=True
                )
                messages.success(request, f'City "{name}" added with pricing.')
                
        elif action == 'edit_city':
            city_id = request.POST.get('city_id')
            city = get_object_or_404(DeliveryCity, id=city_id, district__province__brand=brand)
            city.name = request.POST.get('name', city.name).strip()
            city.rate = request.POST.get('rate', city.rate)
            city.estimated_days = request.POST.get('estimated_days', '').strip() or None
            is_free_above = request.POST.get('is_free_above', '').strip()
            city.is_free_above = is_free_above if is_free_above else None
            city.is_active = request.POST.get('is_active') == 'on'
            city.save()
            messages.success(request, 'City delivery pricing updated.')
            
        elif action == 'delete_city':
            city_id = request.POST.get('city_id')
            city = get_object_or_404(DeliveryCity, id=city_id, district__province__brand=brand)
            city.delete()
            messages.success(request, 'City deleted.')
            
        return redirect('shipping_settings')
        
    provinces = DeliveryProvince.objects.filter(brand=brand).prefetch_related('districts__cities')
    return render(request, 'orders/shipping_settings.html', {
        'brand': brand,
        'provinces': provinces
    })

def validate_coupon_api(request, brand_slug):
    from django.http import JsonResponse
    from apps.brands.models import Brand, Coupon
    
    brand = get_object_or_404(Brand, slug=brand_slug)
    code = request.GET.get('code', '').upper()
    total = float(request.GET.get('total', 0))
    
    try:
        c = Coupon.objects.get(brand=brand, code=code, is_active=True)
        
        if c.max_uses > 0 and c.times_used >= c.max_uses:
            return JsonResponse({'valid': False, 'error': 'Coupon usage limit reached.'})
            
        if c.min_order_value > total:
            return JsonResponse({'valid': False, 'error': f'Minimum order value is {c.min_order_value}.'})
            
        if c.condition == 'FIRST_PURCHASE':
            # Check if user is logged in and has past orders
            if request.user.is_authenticated:
                if request.user.orders.filter(brand=brand, status__in=['PAID', 'SHIPPED', 'DELIVERED']).exists():
                    return JsonResponse({'valid': False, 'error': 'Coupon valid for first purchase only.'})
            else:
                # If guest, we can't reliably verify first purchase yet, but we allow it or block it. Let's allow for now.
                pass
                
        # Calculate discount
        discount_amount = 0
        if c.discount_type == 'PERCENTAGE':
            discount_amount = (total * float(c.discount_value)) / 100
        else:
            discount_amount = float(c.discount_value)
            
        # Ensure discount doesn't exceed total
        discount_amount = min(discount_amount, total)
        
        return JsonResponse({
            'valid': True,
            'discount': round(discount_amount, 2)
        })
        
    except Coupon.DoesNotExist:
        return JsonResponse({'valid': False, 'error': 'Invalid coupon code.'})


@login_required
def manage_customers_view(request):
    """
    CRM Dashboard: Displays all unique customers who have ordered from this brand.
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
        
    from django.db.models import Sum, Count
    from apps.orders.models import Order
    from django.contrib.auth.models import User
    
    # Get all orders for this brand that have a user attached
    orders_with_users = Order.objects.filter(brand=brand, user__isnull=False)
    
    # Get unique user IDs
    user_ids = orders_with_users.values_list('user_id', flat=True).distinct()
    
    customers = []
    for uid in user_ids:
        user = User.objects.get(id=uid)
        stats = orders_with_users.filter(user=user).aggregate(
            total_spend=Sum('total_amount'),
            order_count=Count('id')
        )
        
        phone = None
        if hasattr(user, 'profile') and user.profile and user.profile.phone_number:
            phone = user.profile.phone_number
            
        # Get the latest order date and phone if missing
        last_order = orders_with_users.filter(user=user).order_by('-created_at').first()
        
        if not phone and last_order and last_order.customer_phone:
            phone = last_order.customer_phone
            
        customers.append({
            'id': user.id,
            'name': user.get_full_name() or user.username,
            'email': user.email,
            'phone': phone,
            'total_spend': stats['total_spend'] or 0,
            'order_count': stats['order_count'] or 0,
            'last_order_date': last_order.created_at if last_order else None
        })
        
    # Sort by total spend descending
    customers.sort(key=lambda x: x['total_spend'], reverse=True)
        
    return render(request, 'orders/manage_customers.html', {
        'brand': brand,
        'customers': customers
    })

@login_required
def customer_detail_view(request, customer_id):
    """
    Shows the detail of a specific customer including their order history with this brand.
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
        
    from django.contrib.auth.models import User
    from apps.orders.models import Order
    from django.shortcuts import get_object_or_404
    from django.db.models import Sum
    
    customer_user = get_object_or_404(User, id=customer_id)
    
    # Ensure they have actually ordered from this brand or are registered as a brand customer
    orders = Order.objects.filter(brand=brand, user=customer_user).order_by('-created_at')
    from apps.brands.models import BrandCustomer
    is_brand_customer = BrandCustomer.objects.filter(brand=brand, user=customer_user).exists()
    
    if not orders.exists() and not is_brand_customer:
        messages.error(request, "This customer has not placed any orders and is not registered with your brand.")
        return redirect('customers_management')
        
    stats = orders.aggregate(total_spend=Sum('total_amount'))
    total_spend = stats['total_spend'] or 0
    
    phone = None
    if hasattr(customer_user, 'profile') and customer_user.profile:
        phone = customer_user.profile.phone_number
        
    context = {
        'brand': brand,
        'customer': customer_user,
        'phone': phone,
        'orders': orders,
        'total_spend': total_spend,
        'order_count': orders.count()
    }
    
    return render(request, 'orders/customer_detail.html', context)

def request_return_view(request, order_id):
    """
    Consumer facing view to request a return for a delivered order.
    """
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        
        # Verify ownership if logged in
        if order.user:
            if not request.user.is_authenticated or request.user != order.user:
                messages.error(request, "You do not have permission to return this order.")
                return redirect(f"{reverse('track_order', args=[order.brand.slug])}?order_id={order.id}")
        else:
            # Verify guest email
            provided_email = request.POST.get('email', '').strip().lower()
            if provided_email != order.customer_email.lower():
                messages.error(request, "Email does not match the order records.")
                return redirect(f"{reverse('track_order', args=[order.brand.slug])}?order_id={order.id}")
        if order.status not in ['DELIVERED', 'SHIPPED']:
            messages.error(request, "This order is not eligible for return yet.")
            return redirect(f"{reverse('track_order', args=[order.brand.slug])}?order_id={order.id}")
            
        if order.returns.exists():
            messages.error(request, "A return request has already been submitted for this order.")
            return redirect(f"{reverse('track_order', args=[order.brand.slug])}?order_id={order.id}")
            
        reason = request.POST.get('reason', '').strip()
        if not reason:
            messages.error(request, "Please provide a reason for the return.")
            return redirect(f"{reverse('track_order', args=[order.brand.slug])}?order_id={order.id}")
            
        ReturnRequest.objects.create(
            order=order,
            brand=order.brand,
            customer_email=order.user.email if order.user else request.POST.get('email', ''),
            reason=reason
        )
        
        messages.success(request, "Your return request has been submitted successfully.")
        
        return redirect(f"{reverse('track_order', args=[order.brand.slug])}?order_id={order.id}")
        
    return redirect('index')

from django.views.decorators.csrf import csrf_exempt
import stripe

@csrf_exempt
def stripe_webhook(request, brand_slug):
    """
    Webhook endpoint for Stripe to notify us about asynchronous events (e.g., successful payment).
    """
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    if not sig_header:
        return HttpResponse("Missing Stripe signature.", status=400)

    brand = get_object_or_404(Brand, slug=brand_slug)
    brand_integration = BrandIntegration.objects.filter(brand=brand, integration__provider_code='STRIPE').first()

    if not brand_integration:
        return HttpResponse("Stripe integration not found for this brand.", status=400)

    webhook_secret = brand_integration.credentials.get('webhook_secret')
    
    if not webhook_secret:
        return HttpResponse("Webhook secret is not configured for this brand.", status=400)

    stripe.api_key = brand_integration.credentials.get('api_secret') or brand_integration.credentials.get('api_key')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse("Invalid payload", status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse("Invalid signature", status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Fulfill the purchase...
        order_id = session.get('client_reference_id')
        if order_id:
            try:
                order = Order.objects.get(id=order_id)
                if order.status != 'PAID':
                    order.status = 'PAID'
                    order.payment_provider = 'STRIPE'
                    order.payment_reference_id = session.get('payment_intent')
                    order.save()
                    
                    # Clear cart for the user
                    from apps.orders.models import Cart
                    Cart.objects.filter(user=order.user, brand=order.brand).delete()
            except Order.DoesNotExist:
                pass

    return HttpResponse(status=200)

def checkout_paypal_verify(request):
    token = request.GET.get('token')
    order_id = request.GET.get('order_id')
    if not token or not order_id: return HttpResponse("Missing token", status=400)
    
    order = get_object_or_404(Order, id=order_id)
    brand_integration = BrandIntegration.objects.filter(brand=order.brand, integration__provider_code='PAYPAL').first()
    
    from apps.orders.services.payment_gateways import PayPalService
    verification = PayPalService.verify_payment(token, brand_integration)
    
    if verification.get('success'):
        order.status = 'PAID'
        order.payment_provider = 'PAYPAL'
        order.payment_reference_id = verification.get('transaction_id')
        order.save()
        from apps.orders.models import Cart
        Cart.objects.filter(user=order.user, brand=order.brand).delete()
        NotificationDispatcher.dispatch_order_success(order)
        return redirect('order_success', order_id=order.id)
    return HttpResponse(f"PayPal Verification Failed", status=400)

def checkout_razorpay_verify(request):
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    if not payment_id or not order_id: return HttpResponse("Missing payment_id", status=400)
    
    order = get_object_or_404(Order, id=order_id)
    brand_integration = BrandIntegration.objects.filter(brand=order.brand, integration__provider_code='RAZORPAY').first()
    
    from apps.orders.services.payment_gateways import RazorpayService
    verification = RazorpayService.verify_payment(payment_id, brand_integration)
    
    if verification.get('success'):
        order.status = 'PAID'
        order.payment_provider = 'RAZORPAY'
        order.payment_reference_id = verification.get('transaction_id')
        order.save()
        from apps.orders.models import Cart
        Cart.objects.filter(user=order.user, brand=order.brand).delete()
        NotificationDispatcher.dispatch_order_success(order)
        return redirect('order_success', order_id=order.id)
    return HttpResponse(f"Razorpay Verification Failed", status=400)


def checkout_klarna_verify(request):
    order_id = request.GET.get('order_id')
    if not order_id: return HttpResponse("Missing order_id", status=400)
    
    order = get_object_or_404(Order, id=order_id)
    brand_integration = BrandIntegration.objects.filter(brand=order.brand, integration__provider_code='KLARNA').first()
    
    from apps.orders.services.payment_gateways import KlarnaService
    verification = KlarnaService.verify_payment(order_id, brand_integration)
    
    if verification.get('success'):
        order.status = 'PAID'
        order.payment_provider = 'KLARNA'
        order.payment_reference_id = verification.get('transaction_id')
        order.save()
        from apps.orders.models import Cart
        Cart.objects.filter(user=order.user, brand=order.brand).delete()
        NotificationDispatcher.dispatch_order_success(order)
        return redirect('order_success', order_id=order.id)
    return HttpResponse(f"Klarna Verification Failed", status=400)

def checkout_afterpay_verify(request):
    order_id = request.GET.get('order_id')
    if not order_id: return HttpResponse("Missing order_id", status=400)
    
    order = get_object_or_404(Order, id=order_id)
    brand_integration = BrandIntegration.objects.filter(brand=order.brand, integration__provider_code='AFTERPAY').first()
    
    from apps.orders.services.payment_gateways import AfterpayService
    verification = AfterpayService.verify_payment(order_id, brand_integration)
    
    if verification.get('success'):
        order.status = 'PAID'
        order.payment_provider = 'AFTERPAY'
        order.payment_reference_id = verification.get('transaction_id')
        order.save()
        from apps.orders.models import Cart
        Cart.objects.filter(user=order.user, brand=order.brand).delete()
        NotificationDispatcher.dispatch_order_success(order)
        return redirect('order_success', order_id=order.id)
    return HttpResponse(f"Afterpay Verification Failed", status=400)
