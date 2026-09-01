import logging
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from apps.core.email_utils import dispatch_async_email
from apps.core.utils import get_brand_url

logger = logging.getLogger(__name__)

@receiver(pre_delete, sender=User)
def trigger_account_deletion_email(sender, instance, **kwargs):
    """
    Trigger account_deletion email right before a user is deleted.
    """
    try:
        context = {
            'user': instance,
            # We don't have a retention period in our models currently, so use a static string for the MVP
            'retention_days': '30' 
        }
        dispatch_async_email('account_deletion', context, [instance.email])
        logger.info(f"Dispatched account_deletion email for user {instance.email}")
    except Exception as e:
        logger.error(f"Failed to dispatch account_deletion email for {instance.email}: {e}")

@receiver(post_save, sender=User)
def trigger_customer_welcome_email(sender, instance, created, **kwargs):
    """
    Trigger customer_welcome when a new User registers.
    """
    if created and instance.email:
        try:
            base_url = get_brand_url() # None brand defaults to platform URL
            context = {
                'user': instance,
                'login_url': f'{base_url}/accounts/login/' 
            }
            dispatch_async_email('customer_welcome', context, [instance.email])
            logger.info(f"Dispatched customer_welcome email to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to dispatch customer_welcome: {e}")
