import hmac
import hashlib
import base64
import json
import requests
from django.conf import settings
from django.urls import reverse
import stripe

class EsewaService:
    """
    eSewa ePay v2 Integration
    Documentation: https://developer.esewa.com.np/
    """
    # Use sandbox by default unless in strict production mode
    BASE_URL = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"
    VERIFY_URL = "https://rc-epay.esewa.com.np/api/epay/transaction/status/"

    @staticmethod
    def generate_signature(secret_key, total_amount, transaction_uuid, product_code):
        message = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
        hash_digest = hmac.new(
            secret_key.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(hash_digest).decode('utf-8')

    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        merchant_id = brand_integration.credentials.get('merchant_id', 'EPAYTEST')
        secret_key = brand_integration.credentials.get('api_key', '8gBm/:&EnhH.1/q') 
        
        amount = str(order.total_amount)
        tx_uuid = str(order.id)
        
        signature = cls.generate_signature(secret_key, amount, tx_uuid, merchant_id)
        
        success_url = request.build_absolute_uri(reverse('checkout_esewa_verify'))
        failure_url = request.build_absolute_uri(reverse('store_product_detail', kwargs={'slug': order.brand.slug, 'product_id': order.items.first().product_variant.product.id}))

        return {
            "url": cls.BASE_URL,
            "amount": amount,
            "tax_amount": "0",
            "total_amount": amount,
            "transaction_uuid": tx_uuid,
            "product_code": merchant_id,
            "product_service_charge": "0",
            "product_delivery_charge": "0",
            "success_url": success_url,
            "failure_url": failure_url,
            "signed_field_names": "total_amount,transaction_uuid,product_code",
            "signature": signature,
        }

    @classmethod
    def verify_payment(cls, encoded_data, brand_integration):
        try:
            decoded_bytes = base64.b64decode(encoded_data)
            data = json.loads(decoded_bytes.decode('utf-8'))
            
            if data.get('status') == 'COMPLETE':
                return {
                    'success': True,
                    'transaction_uuid': data.get('transaction_uuid'),
                    'transaction_code': data.get('transaction_code'),
                }
            return {'success': False, 'error': 'Transaction not completed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


class KhaltiService:
    """
    Khalti ePayment API v2
    Documentation: https://docs.khalti.com/
    """
    BASE_URL = "https://a.khalti.com/api/v2/epayment/initiate/"
    LOOKUP_URL = "https://a.khalti.com/api/v2/epayment/lookup/"

    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        api_key = brand_integration.credentials.get('api_key')
        
        return_url = request.build_absolute_uri(reverse('checkout_khalti_verify'))
        website_url = request.build_absolute_uri('/')

        amount_paisa = int(order.total_amount * 100)

        payload = {
            "return_url": return_url,
            "website_url": website_url,
            "amount": amount_paisa,
            "purchase_order_id": str(order.id),
            "purchase_order_name": f"Order #{order.id} at {order.brand.name}",
            "customer_info": {
                "name": order.user.get_full_name() if order.user else "Guest Customer",
                "email": order.user.email if order.user else "guest@example.com",
            }
        }

        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(cls.BASE_URL, json=payload, headers=headers)
            data = response.json()
            if response.status_code == 200:
                return {
                    "success": True,
                    "payment_url": data.get("payment_url"),
                    "pidx": data.get("pidx")
                }
            return {"success": False, "error": data.get("detail", "Khalti API Error")}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def verify_payment(cls, pidx, brand_integration):
        api_key = brand_integration.credentials.get('api_key')
        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {"pidx": pidx}
        
        try:
            response = requests.post(cls.LOOKUP_URL, json=payload, headers=headers)
            data = response.json()
            
            if response.status_code == 200 and data.get('status') == 'Completed':
                return {
                    "success": True,
                    "transaction_id": data.get("transaction_id"),
                    "purchase_order_id": data.get("purchase_order_id")
                }
            return {"success": False, "error": f"Payment not completed. Status: {data.get('status')}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class StripeService:
    """
    Stripe Checkout Session Integration
    """
    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        stripe.api_key = brand_integration.credentials.get('secret_key') or brand_integration.credentials.get('api_secret')
        
        if not stripe.api_key:
            return {"success": False, "error": "Stripe API key is not configured."}
            
        success_url = request.build_absolute_uri(reverse('checkout_stripe_verify')) + f"?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}"
        cancel_url = request.build_absolute_uri(reverse('store_product_detail', kwargs={'slug': order.brand.slug, 'product_id': order.items.first().product_variant.product.id}))

        currency = getattr(order.brand, 'currency', 'USD').lower()
        if currency == 'npr':
            currency = 'usd'
            amount_cents = int(float(order.total_amount) * 100 / 130)
        else:
            amount_cents = int(float(order.total_amount) * 100)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': currency,
                            'unit_amount': amount_cents,
                            'product_data': {
                                'name': f"Order #{order.id} at {order.brand.name}",
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                client_reference_id=str(order.id),
                customer_email=order.user.email if order.user else "guest@example.com",
            )
            return {
                "success": True,
                "payment_url": checkout_session.url,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def verify_payment(cls, session_id, brand_integration):
        stripe.api_key = brand_integration.credentials.get('secret_key') or brand_integration.credentials.get('api_secret')
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                return {
                    "success": True,
                    "transaction_id": session.payment_intent,
                    "purchase_order_id": session.client_reference_id
                }
            return {"success": False, "error": f"Payment status: {session.payment_status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}


class PayPalService:
    """
    PayPal REST API (v2 Orders) 
    """
    @classmethod
    def get_access_token(cls, client_id, client_secret):
        url = "https://api-m.sandbox.paypal.com/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        data = {"grant_type": "client_credentials"}
        response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret), timeout=10)
        if response.status_code == 200:
            return response.json().get('access_token')
        return None

    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        client_id = brand_integration.credentials.get('client_id')
        client_secret = brand_integration.credentials.get('client_secret')
        
        if not client_id or not client_secret:
            return {"success": False, "error": "PayPal credentials missing."}
            
        token = cls.get_access_token(client_id, client_secret)
        if not token:
            return {"success": False, "error": "Invalid PayPal Credentials."}
            
        url = "https://api-m.sandbox.paypal.com/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        success_url = request.build_absolute_uri(reverse('checkout_paypal_verify')) + f"?order_id={order.id}"
        cancel_url = request.build_absolute_uri(reverse('store_product_detail', kwargs={'slug': order.brand.slug, 'product_id': order.items.first().product_variant.product.id}))
        
        currency = getattr(order.brand, 'currency', 'USD').upper()
        if currency == 'NPR':
            currency = 'USD'
            total = round(float(order.total_amount) / 130, 2)
        else:
            total = round(float(order.total_amount), 2)
            
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [{
                "reference_id": str(order.id),
                "amount": {
                    "currency_code": currency,
                    "value": str(total)
                }
            }],
            "application_context": {
                "return_url": success_url,
                "cancel_url": cancel_url,
                "user_action": "PAY_NOW"
            }
        }
        
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        data = response.json()
        
        if response.status_code == 201:
            # Find approval link
            for link in data.get('links', []):
                if link.get('rel') == 'approve':
                    return {"success": True, "payment_url": link.get('href')}
        
        return {"success": False, "error": data.get('message', "PayPal Order Creation Failed")}

    @classmethod
    def verify_payment(cls, paypal_order_id, brand_integration):
        client_id = brand_integration.credentials.get('client_id')
        client_secret = brand_integration.credentials.get('client_secret')
        token = cls.get_access_token(client_id, client_secret)
        
        url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        
        response = requests.post(url, headers=headers, timeout=10)
        data = response.json()
        
        if response.status_code == 201 and data.get('status') == 'COMPLETED':
            return {
                "success": True,
                "transaction_id": data.get('id')
            }
        return {"success": False, "error": "Payment not captured."}


class RazorpayService:
    """
    Razorpay Orders API
    """
    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        key_id = brand_integration.credentials.get('key_id')
        key_secret = brand_integration.credentials.get('key_secret')
        
        if not key_id or not key_secret:
            return {"success": False, "error": "Razorpay credentials missing."}
            
        url = "https://api.razorpay.com/v1/orders"
        
        currency = getattr(order.brand, 'currency', 'INR').upper()
        if currency == 'NPR':
            currency = 'INR'
            amount = int(float(order.total_amount) * 100 / 1.6)
        else:
            amount = int(float(order.total_amount) * 100)
            
        payload = {
            "amount": amount,
            "currency": currency,
            "receipt": str(order.id)
        }
        
        response = requests.post(url, json=payload, auth=(key_id, key_secret), timeout=10)
        data = response.json()
        
        if response.status_code == 200:
            # We return a custom URL (e.g., our own view) that renders the Razorpay JS popup with this order_id
            # For this simulator backend, we'll mimic the success url redirect flow
            success_url = request.build_absolute_uri(reverse('checkout_razorpay_verify')) + f"?payment_id=sim_{data.get('id')}&order_id={order.id}"
            return {"success": True, "payment_url": success_url, "razorpay_order_id": data.get('id')}
            
        return {"success": False, "error": data.get('error', {}).get('description', 'Razorpay API Error')}

    @classmethod
    def verify_payment(cls, payment_id, brand_integration):
        return {"success": True, "transaction_id": payment_id}


class KlarnaService:
    """
    Klarna Payments API
    """
    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        username = brand_integration.credentials.get('username')
        password = brand_integration.credentials.get('password')
        
        if not username or not password:
            return {"success": False, "error": "Klarna credentials missing."}
            
        success_url = request.build_absolute_uri(reverse('checkout_klarna_verify')) + f"?order_id={order.id}"
        
        # Real implementation would call api.klarna.com/payments/v1/sessions
        return {"success": True, "payment_url": success_url}

    @classmethod
    def verify_payment(cls, order_id, brand_integration):
        return {"success": True, "transaction_id": f"KLA_{order_id}"}


class AfterpayService:
    """
    Afterpay API
    """
    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        merchant_id = brand_integration.credentials.get('merchant_id')
        secret_key = brand_integration.credentials.get('secret_key')
        
        if not merchant_id or not secret_key:
            return {"success": False, "error": "Afterpay credentials missing."}
            
        success_url = request.build_absolute_uri(reverse('checkout_afterpay_verify')) + f"?order_id={order.id}"
        
        # Real implementation would call api.afterpay.com/v2/checkouts
        return {"success": True, "payment_url": success_url}

    @classmethod
    def verify_payment(cls, order_id, brand_integration):
        return {"success": True, "transaction_id": f"AFT_{order_id}"}

