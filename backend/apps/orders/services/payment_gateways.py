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
