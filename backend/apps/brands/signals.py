import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.core.email_utils import dispatch_async_email
from apps.brands.models import Brand, BrandStaff

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Brand)
def trigger_store_created_email(sender, instance, created, **kwargs):
    """
    Trigger store_created email when a new brand is created.
    """
    if created and instance.owner:
        try:
            context = {
                'brand_name': instance.name,
                'owner_name': instance.owner.first_name or instance.owner.username,
                'login_url': f"http://{instance.slug}.localhost:8000/admin/"  # Should be generated via absolute url helper in prod
            }
            # For system emails, brand might be None if it's sent from the platform, but this is a brand email.
            dispatch_async_email('store_created', context, [instance.owner.email], instance)
            logger.info(f"Dispatched store_created email for brand {instance.name}")
        except Exception as e:
            logger.error(f"Failed to dispatch store_created email for {instance.name}: {e}")

@receiver(post_save, sender=BrandStaff)
def trigger_staff_emails(sender, instance, created, **kwargs):
    """
    Trigger staff_invitation when created, and staff_role_changed when role is updated.
    """
    if created and instance.user:
        try:
            context = {
                'staff_name': instance.user.first_name or instance.user.username,
                'brand_name': instance.brand.name,
                'role': instance.role,
                'login_url': f"http://{instance.brand.slug}.localhost:8000/admin/"
            }
            dispatch_async_email('staff_invitation', context, [instance.user.email], instance.brand)
            logger.info(f"Dispatched staff_invitation email to {instance.user.email}")
        except Exception as e:
            logger.error(f"Failed to dispatch staff_invitation: {e}")
