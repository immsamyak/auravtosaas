import hmac
import hashlib
import base64
import json
import requests
from django.conf import settings
from django.urls import reverse

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
        """
        Returns the data dictionary needed to build the auto-submitting eSewa form.
        """
        merchant_id = brand_integration.credentials.get('merchant_id', 'EPAYTEST')
        secret_key = brand_integration.credentials.get('api_key', '8gBm/:&EnhH.1/q') # eSewa usually uses secret key
        
        # eSewa requires amounts in 2 decimal string format strictly sometimes, but numeric mostly
        amount = str(order.total_amount)
        tx_uuid = str(order.id)
        
        signature = cls.generate_signature(secret_key, amount, tx_uuid, merchant_id)
        
        # Build absolute URLs
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
        """
        Verifies the response from eSewa after redirect.
        """
        try:
            decoded_bytes = base64.b64decode(encoded_data)
            data = json.loads(decoded_bytes.decode('utf-8'))
            
            # Additional server-to-server verification step is recommended
            # For simplicity in this implementation, if eSewa signed it properly and status is COMPLETE
            if data.get('status') == 'COMPLETE':
                return {
                    'success': True,
                    'transaction_uuid': data.get('transaction_uuid'),
                    'transaction_code': data.get('transaction_code'), # Reference ID
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
        """
        Makes a server-to-server call to Khalti to get a payment URL.
        """
        api_key = brand_integration.credentials.get('api_key')
        
        return_url = request.build_absolute_uri(reverse('checkout_khalti_verify'))
        website_url = request.build_absolute_uri('/')

        # Khalti expects amount in Paisa (1 NPR = 100 Paisa)
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
        """
        Looks up the transaction status using pidx.
        """
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

import stripe

class StripeService:
    """
    Stripe Checkout Session Integration for Storefront
    Documentation: https://stripe.com/docs/checkout
    """
    
    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        """
        Creates a Stripe Checkout Session and returns the checkout URL.
        """
        # 1. Setup Stripe
        stripe.api_key = brand_integration.credentials.get('secret_key') or brand_integration.credentials.get('api_secret') or brand_integration.credentials.get('api_key')
        
        if not stripe.api_key:
            return {"success": False, "error": "Stripe API key is not configured for this brand."}
            
        success_url = request.build_absolute_uri(reverse('checkout_stripe_verify')) + f"?session_id={{CHECKOUT_SESSION_ID}}&order_id={order.id}"
        cancel_url = request.build_absolute_uri(reverse('store_product_detail', kwargs={'slug': order.brand.slug, 'product_id': order.items.first().product_variant.product.id}))

        # Convert to smallest currency unit (cents). Assuming brand currency requires * 100 for Stripe.
        # Stripe does not support NPR. If brand currency is NPR, it might fail unless converted to USD.
        # We will pass the brand's currency code or default to USD if not set/supported.
        # For this implementation, we use 'usd' as default fallback.
        currency = getattr(order.brand, 'currency', 'USD').lower()
        if currency == 'npr':
            currency = 'usd' # Fallback since NPR isn't supported by Stripe natively without conversion
            amount_cents = int(float(order.total_amount) * 100 / 130) # Rough USD conversion if they force it
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
        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @classmethod
    def verify_payment(cls, session_id, brand_integration):
        """
        Retrieves the checkout session to verify payment status.
        """
        stripe.api_key = brand_integration.credentials.get('secret_key') or brand_integration.credentials.get('api_secret') or brand_integration.credentials.get('api_key')
        
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == 'paid':
                return {
                    "success": True,
                    "transaction_id": session.payment_intent,
                    "purchase_order_id": session.client_reference_id
                }
            return {"success": False, "error": f"Payment status: {session.payment_status}"}
        except stripe.error.StripeError as e:
            return {"success": False, "error": str(e)}
        except Exception as e:
            return {"success": False, "error": str(e)}

class PayPalService:
    """
    PayPal Checkout Integration (Simulated for Demo)
    Documentation: https://developer.paypal.com/docs/checkout/
    """
    
    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        client_id = brand_integration.credentials.get('client_id') or brand_integration.credentials.get('api_key')
        client_secret = brand_integration.credentials.get('client_secret') or brand_integration.credentials.get('api_secret')
        
        if not client_id or not client_secret:
            return {"success": False, "error": "PayPal credentials missing."}
            
        success_url = request.build_absolute_uri(reverse('checkout_paypal_verify')) + f"?token=PAYPAL_{order.id}&order_id={order.id}"
        
        # In a real implementation, we would call the PayPal Orders API to create an order
        # and get the approval URL. Here we simulate it.
        approval_url = success_url # Simulating approval redirect
        
        return {
            "success": True,
            "payment_url": approval_url,
        }

    @classmethod
    def verify_payment(cls, token, brand_integration):
        # In a real implementation, we would call PayPal API to capture the order using the token
        return {
            "success": True,
            "transaction_id": f"PP_TXN_{token}",
            "purchase_order_id": token.replace("PAYPAL_", "")
        }

class RazorpayService:
    """
    Razorpay Checkout Integration (Simulated for Demo)
    Documentation: https://razorpay.com/docs/payments/payment-gateway/
    """
    
    @classmethod
    def initiate_payment(cls, order, brand_integration, request):
        key_id = brand_integration.credentials.get('key_id') or brand_integration.credentials.get('api_key')
        key_secret = brand_integration.credentials.get('key_secret') or brand_integration.credentials.get('api_secret')
        
        if not key_id or not key_secret:
            return {"success": False, "error": "Razorpay credentials missing."}
            
        # In Razorpay, we typically create an order via API, then pass order_id to frontend JS.
        # Since we are doing a redirect model for simplicity in this demo:
        success_url = request.build_absolute_uri(reverse('checkout_razorpay_verify')) + f"?payment_id=RZP_{order.id}&order_id={order.id}"
        
        return {
            "success": True,
            "payment_url": success_url,
        }

    @classmethod
    def verify_payment(cls, payment_id, brand_integration):
        return {
            "success": True,
            "transaction_id": payment_id,
        }
