from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order
from apps.core.utils import get_brand_url
from apps.core.email_utils import dispatch_async_email


@receiver(pre_save, sender=Order)
def capture_old_status(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Order.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Order.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Order)
def order_lifecycle_emails(sender, instance, created, **kwargs):
    # Determine the recipient email (user email or guest customer email)
    recipient_email = instance.user.email if instance.user else None
    customer_name = instance.customer_name or (instance.user.first_name if instance.user else "Customer")
    
    if not recipient_email:
        # If no email is available to send to, just return
        return

    # Use brand URL for dynamic routing
    base_url = get_brand_url(instance.brand) if instance.brand else "{{ platform_settings.site_url }}"

    # Prepare standard context for all order emails
    context = {
        'order_id': str(instance.id).split('-')[0].upper(), # short ID
        'customer_name': customer_name,
        'order_total': str(instance.total_amount),
        'shipping_address': instance.shipping_address or "N/A",
        'tracking_number': instance.tracking_number or "N/A",
        'courier_name': instance.shipping_provider or "N/A",
        'order_url': f"{base_url}/orders/{instance.id}/",
        'tracking_url': f"https://www.google.com/search?q={instance.tracking_number}" if instance.tracking_number else "#"
    }


    if created:
        # If order was just created, it might be PENDING or PAID immediately depending on gateway
        if instance.status in ['PENDING', 'PAID']:
            dispatch_async_email('order_confirmation', context, [recipient_email])
        return

    # If it's an update, check if status changed
    old_status = getattr(instance, '_old_status', None)
    if old_status and old_status != instance.status:
        # Status changed!
        
        if instance.status == 'PAID' and old_status == 'PENDING':
            # Send confirmation if it wasn't sent on creation
            dispatch_async_email('order_confirmation', context, [recipient_email])
            
        elif instance.status == 'SENT_TO_COURIER':
            dispatch_async_email('order_shipped', context, [recipient_email])
            
        elif instance.status == 'DELIVERED':
            dispatch_async_email('order_delivered', context, [recipient_email])
            
        elif instance.status == 'CANCELLED':
            dispatch_async_email('order_canceled', context, [recipient_email])
