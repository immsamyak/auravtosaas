import logging
from django.conf import settings
from apps.core.email_utils import send_dynamic_email

logger = logging.getLogger(__name__)

class NotificationManager:

    @staticmethod
    def send_custom_campaign(user, campaign):
        from .email_utils import dispatch_async_email
        context = {
            'user': user,
            'campaign': campaign,
            'body_html': campaign.body_html
        }
        dispatch_async_email('custom_campaign', context, [user.email])

    @staticmethod
    def send_welcome_email(user, brand=None):
        from .email_utils import dispatch_async_email
        context = {
            'user': user,
            'brand': brand,
        }
        dispatch_async_email('welcome', context, [user.email], brand=brand)

    @staticmethod
    def send_password_reset_email(user, reset_url):
        from .email_utils import dispatch_async_email
        context = {
            'user': user,
            'reset_url': reset_url,
        }
        dispatch_async_email('password_reset', context, [user.email])

    @staticmethod
    def send_order_confirmation(order):
        from .email_utils import dispatch_async_email
        context = {
            'order': order,
            'customer_name': order.customer_name or order.user.username,
        }
        email = order.user.email if order.user else getattr(order, 'customer_email', None)
        if email:
            dispatch_async_email('order_confirmation', context, [email])

    @staticmethod
    def send_subscription_success(brand, subscription):
        from .email_utils import dispatch_async_email
        context = {
            'brand': brand,
            'subscription': subscription,
        }
        if brand.owner:
            dispatch_async_email('subscription_success', context, [brand.owner.email], brand=brand)

    @staticmethod
    def send_sms_alert(phone_number, message):
        """
        Sends an SMS via Twilio. Falls back to console log if credentials are not configured.
        """
        if not phone_number:
            return
            
        sid = getattr(settings, 'TWILIO_ACCOUNT_SID', None)
        token = getattr(settings, 'TWILIO_AUTH_TOKEN', None)
        from_num = getattr(settings, 'TWILIO_FROM_NUMBER', None)

        if sid and token and from_num:
            try:
                from twilio.rest import Client
                client = Client(sid, token)
                client.messages.create(
                    body=message,
                    from_=from_num,
                    to=phone_number
                )
            except Exception as e:
                logger.error(f"Failed to send SMS to {phone_number}: {e}")
        else:
            logger.info(f"[MOCK SMS] To: {phone_number} | Message: {message}")
            print(f"\\n{'='*50}\\n[MOCK SMS] To: {phone_number}\\nMessage: {message}\\n{'='*50}\\n")
