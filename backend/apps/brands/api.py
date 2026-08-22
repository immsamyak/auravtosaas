import json
import time
from functools import wraps
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ObjectDoesNotExist

from .models import APIKey, APILog, Brand
from apps.catalog.models import Product, ProductVariant, Collection
from apps.orders.models import Order, OrderItem

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def api_key_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        start_time = time.time()
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        token = None
        if auth_header.startswith('Bearer '):
            token = auth_header.split('Bearer ')[1].strip()
            
        status_code = 200
        brand = None
        api_key_prefix = ''
            
        try:
            if not token:
                raise ValueError("Missing or invalid Authorization header")
                
            # In a highly secure system, we would hash the incoming token and compare it to key_hash.
            # For this MVP, since we store the full token in key_hash, we compare directly.
            try:
                api_key = APIKey.objects.get(key_hash=token, is_active=True)
                brand = api_key.brand
                api_key_prefix = api_key.prefix
                request.brand = brand
            except ObjectDoesNotExist:
                raise ValueError("Invalid or inactive API Key")
                
            response = view_func(request, *args, **kwargs)
            status_code = response.status_code
            
        except ValueError as e:
            status_code = 401
            response = JsonResponse({'error': str(e)}, status=401)
        except Exception as e:
            status_code = 500
            response = JsonResponse({'error': 'Internal server error'}, status=500)
            
        # Log the API Request
        latency_ms = int((time.time() - start_time) * 1000)
        
        if brand:
            APILog.objects.create(
                brand=brand,
                api_key_prefix=api_key_prefix,
                endpoint=request.path,
                method=request.method,
                status_code=status_code,
                ip_address=get_client_ip(request),
                latency_ms=latency_ms
            )
            
        return response
    return _wrapped_view

@csrf_exempt
@api_key_required
@require_http_methods(["GET"])
def products_api(request):
    """
    Returns a list of all active products for the authenticated brand.
    """
    brand = request.brand
    products = Product.objects.filter(brand=brand, is_active=True).prefetch_related('variants', 'images')
    
    data = []
    for product in products:
        variants_data = []
        for variant in product.variants.all():
            variants_data.append({
                'id': variant.id,
                'sku': f"{product.slug}-{variant.id}",
                'price': float(product.price),
                'stock_quantity': variant.total_stock,
                'color': variant.color.name if variant.color else None,
                'size': variant.size.name if variant.size else None,
            })
            
        images_data = []
        for img in product.images.all():
            images_data.append({
                'id': img.id,
                'url': request.build_absolute_uri(img.image.url),
                'is_primary': img.is_primary
            })
            
        data.append({
            'id': product.id,
            'name': product.name,
            'slug': product.slug,
            'description': product.description,
            'category': product.category.name if product.category else None,
            'variants': variants_data,
            'images': images_data,
            'created_at': product.created_at.isoformat()
        })
        
    return JsonResponse({'status': 'success', 'count': len(data), 'data': data})

@csrf_exempt
@api_key_required
@require_http_methods(["GET"])
def collections_api(request):
    """
    Returns a list of all active collections for the authenticated brand.
    """
    brand = request.brand
    collections = Collection.objects.filter(brand=brand, is_active=True).prefetch_related('products')
    
    data = []
    for collection in collections:
        data.append({
            'id': collection.id,
            'name': collection.name,
            'slug': collection.slug,
            'description': collection.description,
            'image_url': request.build_absolute_uri(collection.image.url) if collection.image else None,
            'product_count': collection.products.filter(is_active=True).count(),
            'created_at': collection.created_at.isoformat()
        })
        
    return JsonResponse({'status': 'success', 'count': len(data), 'data': data})

@csrf_exempt
@api_key_required
@require_http_methods(["GET"])
def single_product_api(request, product_id):
    """
    Returns full details for a single product.
    """
    brand = request.brand
    try:
        product = Product.objects.prefetch_related('variants', 'images').get(id=product_id, brand=brand, is_active=True)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
        
    variants_data = []
    for variant in product.variants.all():
        variants_data.append({
            'id': variant.id,
            'sku': f"{product.slug}-{variant.id}",
            'price': float(product.price),
            'stock_quantity': variant.total_stock,
            'color': variant.color.name if variant.color else None,
            'size': variant.size.name if variant.size else None,
        })
        
    images_data = []
    for img in product.images.all():
        images_data.append({
            'id': img.id,
            'url': request.build_absolute_uri(img.image.url),
            'is_primary': img.is_primary
        })
        
    data = {
        'id': product.id,
        'name': product.name,
        'slug': product.slug,
        'description': product.description,
        'category': product.category.name if product.category else None,
        'variants': variants_data,
        'images': images_data,
        'created_at': product.created_at.isoformat()
    }
        
    return JsonResponse({'status': 'success', 'data': data})

@csrf_exempt
@api_key_required
@require_http_methods(["GET"])
def order_list_api(request):
    """
    Returns a list of all orders for the authenticated brand.
    """
    brand = request.brand
    orders = Order.objects.filter(brand=brand).order_by('-created_at')[:50] # Limit to 50 for MVP
    
    data = []
    for order in orders:
        data.append({
            'id': order.id,
            'customer_name': order.customer_name,
            'customer_phone': order.customer_phone,
            'status': order.status,
            'total_amount': float(order.total_amount),
            'created_at': order.created_at.isoformat()
        })
        
    return JsonResponse({'status': 'success', 'count': len(data), 'data': data})

@csrf_exempt
@api_key_required
@require_http_methods(["POST"])
def orders_api(request):
    """
    Creates a new order for the authenticated brand.
    Expected JSON payload:
    {
        "customer_phone": "+1234567890",
        "customer_name": "John Doe",
        "shipping_address": "123 Main St",
        "items": [
            {"variant_id": 1, "quantity": 2}
        ]
    }
    """
    brand = request.brand
    
    try:
        body = json.loads(request.body)
        
        customer_phone = body.get('customer_phone')
        if not customer_phone:
            return JsonResponse({'error': 'customer_phone is required'}, status=400)
            
        items = body.get('items', [])
        if not items:
            return JsonResponse({'error': 'items array cannot be empty'}, status=400)
            
        # Create the Order
        order = Order.objects.create(
            brand=brand,
            customer_phone=customer_phone,
            customer_name=body.get('customer_name', ''),
            shipping_address=body.get('shipping_address', ''),
            status='PENDING',
            total_amount=0
        )
        
        total_amount = 0
        for item in items:
            variant_id = item.get('variant_id') or item.get('product_id') # handle both for backward compat with docs
            quantity = int(item.get('quantity', 1))
            
            try:
                # Need to find the product via the variant, or if they passed product_id, we just get the first variant
                if item.get('variant_id'):
                    variant = ProductVariant.objects.get(id=variant_id, product__brand=brand)
                    product = variant.product
                else:
                    product = Product.objects.get(id=variant_id, brand=brand)
                    variant = product.variants.first()
                    
                if not variant:
                    raise ObjectDoesNotExist()
                    
                # Calculate subtotal
                subtotal = product.price * quantity
                total_amount += subtotal
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_variant=variant,
                    quantity=quantity,
                    price_at_time=product.price
                )
                
            except ObjectDoesNotExist:
                # Rollback order creation if variant doesn't exist
                order.delete()
                return JsonResponse({'error': f'Invalid variant/product ID {variant_id}'}, status=404)
                
        # Update order total
        order.total_amount = total_amount
        order.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Order created successfully',
            'order': {
                'id': order.id,
                'order_number': str(order.id).split('-')[0].upper(), # Secure alphanumeric order number
                'total_amount': float(total_amount),
                'status': order.status
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON payload'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
