import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.core.email_utils import dispatch_async_email
from apps.core.utils import get_brand_url
from apps.billing.models import BrandSubscription

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=BrandSubscription)
def capture_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = BrandSubscription.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except BrandSubscription.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=BrandSubscription)
def trigger_subscription_emails(sender, instance, created, **kwargs):
    old_status = getattr(instance, '_old_status', None)
    current_status = instance.status

    if current_status != old_status:
        owner_email = instance.brand.owner.email if instance.brand.owner else None
        if not owner_email:
            return

        if current_status == 'active' and (old_status != 'active' or created):
            # Subscription Success
            try:
                context = {
                    'brand_name': instance.brand.name,
                    'plan_name': instance.plan.name if instance.plan else 'Custom Plan',
                    'billing_cycle': 'Monthly',  # Simplified
                    'amount': str(instance.plan.monthly_price) if instance.plan else '0.00'
                }
                dispatch_async_email('subscription_success', context, [owner_email], instance.brand)
                logger.info(f"Dispatched subscription_success for {instance.brand.name}")
            except Exception as e:
                logger.error(f"Failed to dispatch subscription_success: {e}")

        elif current_status == 'canceled' and old_status != 'canceled':
            # Subscription Canceled
            try:
                context = {
                    'brand_name': instance.brand.name,
                    'plan_name': instance.plan.name if instance.plan else 'Custom Plan',
                    'end_date': instance.current_period_end.strftime("%B %d, %Y") if instance.current_period_end else 'Immediately'
                }
                dispatch_async_email('subscription_canceled', context, [owner_email], instance.brand)
                logger.info(f"Dispatched subscription_canceled for {instance.brand.name}")
            except Exception as e:
                logger.error(f"Failed to dispatch subscription_canceled: {e}")

        elif current_status == 'past_due' and old_status != 'past_due':
            # Payment Failed
            try:
                base_url = get_brand_url(instance.brand)
                context = {
                    'brand_name': instance.brand.name,
                    'amount_due': str(instance.plan.monthly_price) if instance.plan else '0.00',
                    'retry_date': 'in 3 days',  # Hardcoded for example
                    'update_billing_url': f"{base_url}/admin/settings/billing/"
                }
                dispatch_async_email('payment_failed', context, [owner_email], instance.brand)
                logger.info(f"Dispatched payment_failed for {instance.brand.name}")
            except Exception as e:
                logger.error(f"Failed to dispatch payment_failed: {e}")
