import requests
import json
from apps.brands.models import BrandIntegration

class NotificationDispatcher:
    """
    Handles triggering automated notifications and webhooks when an order is completed.
    """

    @classmethod
    def dispatch_order_success(cls, order):
        """
        Loops through active integrations for the brand and dispatches notifications.
        """
        integrations = BrandIntegration.objects.filter(brand=order.brand, is_active=True)
        
        for integration in integrations:
            code = integration.integration.provider_code
            if code == 'TWILIO':
                cls._dispatch_twilio_sms(order, integration)
            elif code == 'SENDGRID':
                cls._dispatch_sendgrid_email(order, integration)
            elif code == 'ZAPIER':
                cls._dispatch_zapier_webhook(order, integration)

    @classmethod
    def _dispatch_twilio_sms(cls, order, brand_integration):
        account_sid = brand_integration.credentials.get('account_sid')
        auth_token = brand_integration.credentials.get('auth_token')
        from_phone = brand_integration.credentials.get('from_phone')
        
        if not all([account_sid, auth_token, from_phone]):
            return
            
        # Try to get customer phone from shipping address or fallback
        to_phone = getattr(order.shipping_address, 'phone', '9800000000') if getattr(order, 'shipping_address', None) else "9800000000"
        
        message = f"Hello {order.user.first_name if order.user else 'Customer'}, your order #{order.id} from {order.brand.name} has been confirmed. Total: {getattr(order.brand, 'currency_symbol', '$')}{order.total_amount}."
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        payload = {
            "To": to_phone,
            "From": from_phone,
            "Body": message
        }
        
        try:
            requests.post(url, data=payload, auth=(account_sid, auth_token), timeout=5)
        except Exception as e:
            print(f"Twilio Dispatch Error: {e}")

    @classmethod
    def _dispatch_sendgrid_email(cls, order, brand_integration):
        api_key = brand_integration.credentials.get('api_key')
        
        if not api_key or not order.user or not order.user.email:
            return
            
        url = "https://api.sendgrid.com/v3/mail/send"
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "personalizations": [
                {
                    "to": [{"email": order.user.email}],
                    "subject": f"Order Confirmation: #{order.id}"
                }
            ],
            "from": {"email": f"orders@{order.brand.slug}.store", "name": order.brand.name},
            "content": [
                {
                    "type": "text/plain",
                    "value": f"Thank you for your purchase! Your order #{order.id} has been received."
                }
            ]
        }
        
        try:
            requests.post(url, json=payload, headers=headers, timeout=5)
        except Exception as e:
            print(f"SendGrid Dispatch Error: {e}")

    @classmethod
    def _dispatch_zapier_webhook(cls, order, brand_integration):
        webhook_url = brand_integration.credentials.get('webhook_url')
        
        if not webhook_url:
            return
            
        payload = {
            "event": "order_created",
            "order_id": str(order.id),
            "brand": order.brand.name,
            "total_amount": float(order.total_amount),
            "currency": getattr(order.brand, 'currency', 'USD'),
            "customer_name": order.user.get_full_name() if order.user else "Guest",
            "customer_email": order.user.email if order.user else "guest@example.com",
            "status": order.status,
            "created_at": order.created_at.isoformat()
        }
        
        try:
            requests.post(webhook_url, json=payload, timeout=5)
        except Exception as e:
            print(f"Zapier Dispatch Error: {e}")
