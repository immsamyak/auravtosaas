import re

with open("backend/apps/orders/views.py", "r") as f:
    content = f.read()

# Add import at the top
if "NotificationDispatcher" not in content:
    content = content.replace(
        "from django.shortcuts import render",
        "from django.shortcuts import render\nfrom apps.orders.services.notifications import NotificationDispatcher"
    )

# Hook into esewa
content = re.sub(
    r"(order\.save\(\)\n\s*)(return redirect\('order_success', order_id=order\.id\))",
    r"\1NotificationDispatcher.dispatch_order_success(order)\n            \2",
    content
)

# Also for Khalti, Stripe, Paypal, Razorpay where the cart is cleared
content = re.sub(
    r"(Cart\.objects\.filter\(user=order\.user, brand=order\.brand\)\.delete\(\)\n\s*)(return redirect\('order_success', order_id=order\.id\))",
    r"\1NotificationDispatcher.dispatch_order_success(order)\n        \2",
    content
)

# Append Klarna and Afterpay verify views
if "def checkout_klarna_verify" not in content:
    content += """

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
"""

with open("backend/apps/orders/views.py", "w") as f:
    f.write(content)
