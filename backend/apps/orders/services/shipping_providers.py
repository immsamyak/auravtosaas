import requests

class LogisticsService:
    """
    Unified Logistics Service to abstract multiple shipping providers.
    """
    
    @classmethod
    def dispatch_order(cls, order, brand_integration):
        """
        Routes the order to the correct logistics provider.
        """
        provider_code = brand_integration.integration.provider_code
        
        try:
            if provider_code == 'PATHAO_PARCEL':
                return cls._dispatch_pathao(order, brand_integration)
            elif provider_code == 'NCM':
                return cls._dispatch_ncm(order, brand_integration)
            elif provider_code == 'UPAYA':
                return cls._dispatch_upaya(order, brand_integration)
            
            return {'success': False, 'error': f'Unsupported shipping provider: {provider_code}'}
        except requests.exceptions.RequestException as e:
            return {'success': False, 'error': f"API Network Error: {str(e)}"}
        except Exception as e:
            return {'success': False, 'error': f"Integration Error: {str(e)}"}

    @classmethod
    def _get_pathao_token(cls, client_id, client_secret, username, password):
        """
        Retrieves OAuth2 Bearer token from Pathao.
        """
        url = "https://api-hermes.pathao.com/aladdin/api/v1/issue-token"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "username": username,
            "password": password,
            "grant_type": "password"
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json().get('access_token')

    @classmethod
    def _dispatch_pathao(cls, order, brand_integration):
        """
        Pathao Parcel API Integration (Live)
        """
        client_id = brand_integration.credentials.get('client_id')
        client_secret = brand_integration.credentials.get('client_secret')
        username = brand_integration.credentials.get('username')
        password = brand_integration.credentials.get('password')
        store_id = brand_integration.credentials.get('merchant_id') # Stored as merchant_id in our DB
        
        if not all([client_id, client_secret, username, password, store_id]):
            return {"success": False, "error": "Missing Pathao credentials in dashboard."}

        # 1. Get OAuth2 Token
        access_token = cls._get_pathao_token(client_id, client_secret, username, password)

        # 2. Build Payload
        payload = {
            "store_id": int(store_id),
            "merchant_order_id": str(order.id),
            "recipient_name": order.user.get_full_name() if order.user else "Guest",
            "recipient_phone": "9800000000", # TODO: Get from Order.shipping_address
            "recipient_address": "Kathmandu, Nepal",
            "recipient_city": 1, # Default
            "recipient_zone": 1, # Default
            "recipient_area": 1, # Default
            "delivery_type": 48, # Standard delivery (48 hours)
            "item_type": 2, # Parcel
            "item_quantity": order.items.count() if order.items.count() else 1,
            "item_weight": 1.0, # KG
            "amount_to_collect": float(order.total_amount) if order.payment_provider == 'CUSTOM_MANUAL' else 0,
            "item_description": f"Order {order.id} from {order.brand.name}"
        }
        
        # 3. Create Order
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://api-hermes.pathao.com/aladdin/api/v1/orders", 
            json=payload, 
            headers=headers,
            timeout=15
        )
        data = response.json()
        
        if response.status_code in [200, 201] and data.get('code') == 200:
            return {
                "success": True,
                "tracking_number": data.get('data', {}).get('consignment_id'),
                "status": "Created"
            }
            
        return {"success": False, "error": data.get('message', 'Pathao API Error')}

    @classmethod
    def _dispatch_ncm(cls, order, brand_integration):
        """
        Nepal Can Move (NCM) API Integration (Live)
        """
        api_token = brand_integration.credentials.get('api_key')
        
        if not api_token:
            return {"success": False, "error": "Missing NCM API Token in dashboard."}
            
        payload = {
            "customer_name": order.user.get_full_name() if order.user else "Guest",
            "customer_phone": "9800000000",
            "delivery_address": "Kathmandu, Nepal",
            "cod_amount": float(order.total_amount) if order.payment_provider == 'CUSTOM_MANUAL' else 0,
            "weight": 1.0,
            "reference_id": str(order.id)
        }
        
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://app.nepalcanmove.com/api/v1/order/create",
            json=payload,
            headers=headers,
            timeout=15
        )
        data = response.json()
        
        if response.status_code in [200, 201]:
            return {
                "success": True,
                "tracking_number": data.get('tracking_id', f"NCM-{order.id.hex[:8].upper()}"),
                "status": "Created"
            }
            
        return {"success": False, "error": data.get('message', 'NCM API Error')}

    @classmethod
    def _dispatch_upaya(cls, order, brand_integration):
        """
        Upaya CityCargo API Integration (Live)
        """
        api_key = brand_integration.credentials.get('api_key')
        
        if not api_key:
            return {"success": False, "error": "Missing Upaya API Key in dashboard."}
            
        payload = {
            "order_number": str(order.id),
            "recipient_name": order.user.get_full_name() if order.user else "Guest",
            "recipient_contact": "9800000000",
            "delivery_address": "Kathmandu, Nepal",
            "payment_mode": "COD" if order.payment_provider == 'CUSTOM_MANUAL' else "PREPAID",
            "total_amount": float(order.total_amount),
            "weight": 1.0
        }
        
        headers = {
            "api-key": api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.post(
            "https://delivery.upaya.com.np/api/order",
            json=payload,
            headers=headers,
            timeout=15
        )
        
        data = response.json()
        
        if response.status_code in [200, 201]:
            return {
                "success": True,
                "tracking_number": data.get('tracking_no', f"UPY-{order.id.hex[:8].upper()}"),
                "status": "Created"
            }
            
        return {"success": False, "error": data.get('message', 'Upaya API Error')}
