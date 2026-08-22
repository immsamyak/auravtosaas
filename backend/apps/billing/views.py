import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from apps.brands.models import Brand
from .models import SubscriptionPlan, BrandSubscription
from django.urls import reverse

from apps.core.models import GlobalSettings

@login_required
def owner_billing_view(request):
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

    subscription, created = BrandSubscription.objects.get_or_create(brand=brand)
    plans = SubscriptionPlan.objects.all().order_by('monthly_price')
    
    return render(request, 'billing/dashboard_billing.html', {
        'brand': brand,
        'subscription': subscription,
        'plans': plans,
    })

@login_required
def create_checkout_session(request, plan_id):
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

    plan = get_object_or_404(SubscriptionPlan, id=plan_id)
    settings_obj = GlobalSettings.get_settings()
    
    if not settings_obj.get_stripe_secret_key:
        from django.contrib import messages
        messages.error(request, f"Stripe {settings_obj.stripe_environment} secret key is not configured in Platform Settings.")
        return redirect('owner_billing')
        
    stripe.api_key = settings_obj.get_stripe_secret_key
    
    # Auto-provision Stripe Price ID if missing
    if not plan.stripe_price_id:
        try:
            # Create the Product in Stripe
            stripe_product = stripe.Product.create(
                name=f"Aura {plan.name} Plan",
                description=f"Monthly subscription for Aura ({plan.try_on_quota} try-ons/mo)"
            )
            # Create the Price in Stripe
            stripe_price = stripe.Price.create(
                product=stripe_product.id,
                unit_amount=int(plan.monthly_price * 100), # Convert to cents
                currency=getattr(settings_obj, 'currency', 'usd').lower(),
                recurring={"interval": "month"}
            )
            # Save the new Price ID to the database
            plan.stripe_price_id = stripe_price.id
            plan.save()
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Failed to auto-provision Stripe plan: {str(e)}")
            return redirect('owner_billing')

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': plan.stripe_price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri(reverse('owner_billing')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('owner_billing')) + "?cancel=1",
            client_reference_id=str(brand.id),
        )
        return redirect(checkout_session.url)
    except Exception as e:
        from django.contrib import messages
        messages.error(request, str(e))
        return redirect('owner_billing')

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    event = None
    settings_obj = GlobalSettings.get_settings()

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings_obj.stripe_webhook_secret
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        brand_id = session.get('client_reference_id')
        if brand_id:
            brand = Brand.objects.get(id=brand_id)
            sub = brand.subscription
            sub.stripe_customer_id = session.get('customer')
            sub.stripe_subscription_id = session.get('subscription')
            sub.status = 'active'
            sub.save()
            
    elif event['type'] == 'invoice.payment_succeeded':
        # Reset usage limits at the start of billing cycle
        subscription_id = event['data']['object'].get('subscription')
        if subscription_id:
            try:
                sub = BrandSubscription.objects.get(stripe_subscription_id=subscription_id)
                sub.try_ons_used = 0
                sub.status = 'active'
                sub.save()
            except BrandSubscription.DoesNotExist:
                pass

    elif event['type'] == 'customer.subscription.deleted':
        subscription_id = event['data']['object'].get('id')
        if subscription_id:
            try:
                sub = BrandSubscription.objects.get(stripe_subscription_id=subscription_id)
                sub.status = 'canceled'
                sub.save()
            except BrandSubscription.DoesNotExist:
                pass

    return HttpResponse(status=200)
