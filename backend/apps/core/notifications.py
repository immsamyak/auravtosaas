import logging
from django.conf import settings
from apps.core.email_utils import send_dynamic_email

logger = logging.getLogger(__name__)

class NotificationManager:

    @staticmethod
    def send_custom_campaign(user, campaign):
        from .email_utils import send_dynamic_email
        context = {
            'user': user,
            'campaign': campaign,
            'body_html': campaign.body_html
        }
        send_dynamic_email(
            subject=campaign.subject,
            template_name='emails/custom_campaign.html',
            context=context,
            to_emails=[user.email]
        )

    @staticmethod
    def send_welcome_email(user, brand=None):
        context = {
            'user': user,
            'brand': brand,
        }
        send_dynamic_email(
            subject=f"Welcome to Aura, {user.first_name or user.username}!",
            template_name='emails/welcome.html',
            context=context,
            to_emails=[user.email]
        )

    @staticmethod
    def send_password_reset_email(user, reset_url):
        context = {
            'user': user,
            'reset_url': reset_url,
        }
        send_dynamic_email(
            subject="Reset Your Aura Password",
            template_name='emails/password_reset.html',
            context=context,
            to_emails=[user.email]
        )

    @staticmethod
    def send_order_confirmation(order):
        context = {
            'order': order,
            'customer_name': order.customer_name or order.user.username,
        }
        email = order.user.email if order.user else getattr(order, 'customer_email', None)
        if email:
            send_dynamic_email(
                subject=f"Order Confirmation #{order.id}",
                template_name='emails/order_confirmation.html',
                context=context,
                to_emails=[email]
            )

    @staticmethod
    def send_subscription_success(brand, subscription):
        context = {
            'brand': brand,
            'subscription': subscription,
        }
        if brand.owner:
            send_dynamic_email(
                subject="Subscription Upgrade Successful",
                template_name='emails/subscription_success.html',
                context=context,
                to_emails=[brand.owner.email]
            )

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
