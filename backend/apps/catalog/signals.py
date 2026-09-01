import logging
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from apps.core.email_utils import dispatch_async_email
from apps.core.utils import get_brand_url
from apps.catalog.models import ProductVariant

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=ProductVariant)
def capture_old_stock(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = ProductVariant.objects.get(pk=instance.pk)
            instance._old_stock = old_instance.stock
        except ProductVariant.DoesNotExist:
            instance._old_stock = 0
    else:
        instance._old_stock = 0

@receiver(post_save, sender=ProductVariant)
def trigger_inventory_emails(sender, instance, created, **kwargs):
    """
    Trigger low_inventory_alert and back_in_stock emails based on stock changes.
    """
    old_stock = getattr(instance, '_old_stock', 0)
    current_stock = instance.stock
    low_stock_threshold = 5  # Example threshold, could be dynamic

    if current_stock != old_stock:
        # Check for Low Inventory
        if current_stock <= low_stock_threshold and old_stock > low_stock_threshold:
            try:
                context = {
                    'product_name': instance.product.name,
                    'variant_name': str(instance),
                    'stock_level': current_stock,
                }
                # Notify the brand owner
                dispatch_async_email('low_inventory_alert', context, [instance.product.brand.owner.email], instance.product.brand)
                logger.info(f"Dispatched low_inventory_alert for {instance}")
            except Exception as e:
                logger.error(f"Failed to dispatch low_inventory_alert: {e}")
                
        # Check for Back in Stock
        elif current_stock > 0 and old_stock <= 0:
            try:
                base_url = get_brand_url(instance.product.brand)
                context = {
                    'product_name': instance.product.name,
                    'variant_name': str(instance),
                    'product_url': f"{base_url}/product/{instance.product.slug}/"
                }
                # We would typically notify a list of users who subscribed to this back-in-stock alert.
                # For this implementation, we will dispatch the event. The actual recipients list would need 
                # to be pulled from a BackInStockSubscription model. We will skip sending for now if we don't have it.
                logger.info(f"Triggered back_in_stock for {instance}")
            except Exception as e:
                logger.error(f"Failed to trigger back_in_stock: {e}")
