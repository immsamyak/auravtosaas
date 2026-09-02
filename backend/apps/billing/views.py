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
    
    # Process session_id if redirected from Stripe Checkout
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            settings_obj = GlobalSettings.get_settings()
            stripe.api_key = settings_obj.get_stripe_secret_key
            session = stripe.checkout.Session.retrieve(session_id)
            
            if session.payment_status == 'paid':
                metadata = session.metadata.to_dict() if getattr(session, 'metadata', None) else {}
                if metadata.get('type') == 'subscription_payment':
                    plan_id = metadata.get('plan_id')
                    if plan_id:
                        from django.utils import timezone
                        from datetime import timedelta
                        from apps.billing.models import SubscriptionHistory
                        
                        plan = SubscriptionPlan.objects.get(id=plan_id)
                        old_plan = subscription.plan
                        
                        action = 'renewed'
                        if old_plan:
                            if plan.monthly_price > old_plan.monthly_price:
                                action = 'upgraded'
                            elif plan.monthly_price < old_plan.monthly_price:
                                action = 'downgraded'
                        else:
                            action = 'upgraded'
                            
                        # Retrieve payment intent to get payment method
                        payment_details = {}
                        pi_id = getattr(session, 'payment_intent', None)
                        if pi_id:
                            try:
                                pi = stripe.PaymentIntent.retrieve(pi_id, expand=['payment_method'])
                                if pi.payment_method and pi.payment_method.type == 'card':
                                    card = pi.payment_method.card
                                    payment_details = {
                                        'brand': card.brand,
                                        'last4': card.last4,
                                        'wallet': card.wallet.type if card.wallet else None
                                    }
                            except Exception:
                                pass
                                
                        SubscriptionHistory.objects.create(
                            brand=brand,
                            action=action,
                            previous_plan_name=old_plan.name if old_plan else "None",
                            new_plan_name=plan.name,
                            amount_paid=plan.monthly_price,
                            transaction_id=pi_id or session.id,
                            payment_details=payment_details
                        )

                        subscription.plan = plan
                        subscription.status = 'active'
                        subscription.try_ons_used = 0
                        subscription.stripe_customer_id = getattr(session, 'customer', None)
                        subscription.stripe_subscription_id = pi_id or session.id
                        subscription.current_period_end = timezone.now() + timedelta(days=30)
                        subscription.save()
                        
                        from django.contrib import messages
                        messages.success(request, f"Successfully upgraded to {plan.name}!")
                        
                        # Redirect to clean the URL
                        return redirect('owner_billing')
        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"Failed to verify payment: {str(e)}")
            
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
    
    # Determine which environment we are using
    is_test_mode = (settings_obj.stripe_environment == 'test')
    
    # Get the correct Price ID
    current_price_id = plan.stripe_test_price_id if is_test_mode else plan.stripe_price_id
    
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': getattr(settings_obj, 'currency', 'usd').lower(),
                    'product_data': {
                        'name': f"Aura {plan.name} Plan (1 Month)",
                        'description': f"{plan.try_on_quota} try-ons/mo",
                    },
                    'unit_amount': int(plan.monthly_price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            customer_email=brand.owner.email if brand.owner else request.user.email,
            customer_creation='always',
            success_url=request.build_absolute_uri(reverse('owner_billing')) + "?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=request.build_absolute_uri(reverse('owner_billing')) + "?cancel=1",
            client_reference_id=str(brand.id),
            metadata={
                'plan_id': plan.id,
                'brand_id': brand.id,
                'type': 'subscription_payment'
            }
        )
        return redirect(checkout_session.url)
    except Exception as e:
        from django.contrib import messages
        messages.error(request, str(e))
        return redirect('owner_billing')

@login_required
def cancel_subscription(request):
    if request.method == 'POST':
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

        subscription = brand.subscription
        if subscription.status == 'active':
            from apps.billing.models import SubscriptionHistory
            SubscriptionHistory.objects.create(
                brand=brand,
                action='canceled',
                previous_plan_name=subscription.plan.name if subscription.plan else "None",
                new_plan_name="Canceled",
                amount_paid=0.00,
                transaction_id="N/A",
                payment_details={}
            )
            subscription.status = 'canceled'
            # We keep current_period_end so they have access until it expires
            subscription.save()
            from django.contrib import messages
            messages.success(request, "Your subscription has been canceled successfully.")
    
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
        session_dict = session.to_dict()
        brand_id = session_dict.get('client_reference_id')
        metadata = session_dict.get('metadata', {})
        
        if brand_id and metadata.get('type') == 'subscription_payment':
            plan_id = metadata.get('plan_id')
            if plan_id:
                from apps.billing.models import SubscriptionHistory
                from django.utils import timezone
                from datetime import timedelta
                
                brand = Brand.objects.get(id=brand_id)
                plan = SubscriptionPlan.objects.get(id=plan_id)
                sub = brand.subscription
                old_plan = sub.plan
                
                action = 'renewed'
                if old_plan:
                    if plan.monthly_price > old_plan.monthly_price:
                        action = 'upgraded'
                    elif plan.monthly_price < old_plan.monthly_price:
                        action = 'downgraded'
                else:
                    action = 'upgraded'
                    
                # Retrieve payment intent to get payment method
                payment_details = {}
                pi_id = session_dict.get('payment_intent')
                if pi_id:
                    try:
                        pi = stripe.PaymentIntent.retrieve(pi_id, expand=['payment_method'])
                        if getattr(pi, 'payment_method', None) and pi.payment_method.type == 'card':
                            card = pi.payment_method.card
                            payment_details = {
                                'brand': card.brand,
                                'last4': card.last4,
                                'wallet': getattr(card.wallet, 'type', None) if getattr(card, 'wallet', None) else None
                            }
                    except Exception:
                        pass
                        
                SubscriptionHistory.objects.create(
                    brand=brand,
                    action=action,
                    previous_plan_name=old_plan.name if old_plan else "None",
                    new_plan_name=plan.name,
                    amount_paid=plan.monthly_price,
                    transaction_id=pi_id or session_dict.get('id'),
                    payment_details=payment_details
                )
                
                # Update subscription locally (no Stripe recurring subscription)
                sub.plan = plan
                sub.status = 'active'
                sub.try_ons_used = 0
                sub.stripe_customer_id = session_dict.get('customer')
                sub.stripe_subscription_id = pi_id or session_dict.get('id')
                sub.current_period_end = timezone.now() + timedelta(days=30)
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
