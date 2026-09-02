import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

import stripe
from apps.core.models import GlobalSettings
from apps.billing.models import BrandSubscription, SubscriptionHistory, SubscriptionPlan
from apps.brands.models import Brand

settings = GlobalSettings.get_settings()
stripe.api_key = settings.get_stripe_secret_key

# Get all successful checkout sessions
sessions = stripe.checkout.Session.list(limit=100)
for session in sessions.data:
    if session.payment_status == 'paid' and session.client_reference_id:
        brand_id = session.client_reference_id
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            continue
            
        metadata = session.metadata
        if getattr(session, 'metadata', None) and isinstance(session.metadata, dict):
            pass
        elif getattr(session, 'metadata', None):
            metadata = session.metadata.to_dict()
        else:
            metadata = {}
            
        if metadata.get('type') == 'subscription_payment':
            plan_id = metadata.get('plan_id')
            if plan_id:
                try:
                    plan = SubscriptionPlan.objects.get(id=plan_id)
                except SubscriptionPlan.DoesNotExist:
                    plan = None
                    
                if plan:
                    # Check if we already have this in history
                    pi_id = getattr(session, 'payment_intent', session.id)
                    if not SubscriptionHistory.objects.filter(transaction_id=pi_id).exists():
                        payment_details = {}
                        if getattr(session, 'payment_intent', None):
                            try:
                                pi = stripe.PaymentIntent.retrieve(session.payment_intent, expand=['payment_method'])
                                if getattr(pi, 'payment_method', None) and pi.payment_method.type == 'card':
                                    card = pi.payment_method.card
                                    payment_details = {
                                        'brand': card.brand,
                                        'last4': card.last4,
                                        'wallet': getattr(card.wallet, 'type', None) if getattr(card, 'wallet', None) else None
                                    }
                            except Exception as e:
                                print(f"Error fetching PI {session.payment_intent}: {e}")
                                
                        import datetime
                        created_at = datetime.datetime.fromtimestamp(session.created)
                        
                        history = SubscriptionHistory.objects.create(
                            brand=brand,
                            action='renewed',
                            previous_plan_name="Unknown",
                            new_plan_name=plan.name,
                            amount_paid=plan.monthly_price,
                            transaction_id=pi_id,
                            payment_details=payment_details
                        )
                        # Override auto_now_add
                        history.created_at = created_at
                        history.save(update_fields=['created_at'])
                        print(f"Backfilled: {plan.name} for {brand.name} at {created_at}")

print("Done backfilling!")
