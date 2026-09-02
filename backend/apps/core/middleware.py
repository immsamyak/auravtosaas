import threading

_thread_locals = threading.local()

def get_current_request():
    return getattr(_thread_locals, 'request', None)

def get_current_user():
    request = get_current_request()
    if request and hasattr(request, 'user'):
        return request.user
    return None

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class AuditLoggingMiddleware:
    """
    Middleware to store the request in a thread-local variable so that 
    model signals can access the current user, IP, and User-Agent.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _thread_locals.request = request
        response = self.get_response(request)
        _thread_locals.request = None
        return response

from django.conf import settings
from django.shortcuts import redirect

class CustomDomainMiddleware:
    """
    Middleware to route custom domains to the correct storefront view invisibly.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow bypassing via a GET param if ever needed for debugging, though not strictly required
        if 'bypass_domain' in request.GET:
            return self.get_response(request)

        # Ignore static and media files
        if request.path_info.startswith(settings.MEDIA_URL) or request.path_info.startswith(settings.STATIC_URL):
            return self.get_response(request)
            
        host = request.get_host().split(':')[0].lower()
        
        # Don't intercept localhost or the main domain (assuming aura.alvicsxinfo.tech is not a custom domain for a specific brand)
        # However, checking the DB is perfectly fine.
        from apps.brands.models import Brand
        
        brand = Brand.objects.filter(custom_domain__iexact=host).first()
        
        if brand and brand.subscription and brand.subscription.plan and brand.subscription.plan.allow_custom_domain:
            original_path = request.path_info
            
            # If the user visits the raw /store/slug URL on their custom domain, enforce clean URL by redirecting
            store_prefix = f"/store/{brand.slug}"
            if original_path.startswith(store_prefix):
                clean_path = original_path[len(store_prefix):]
                if not clean_path.startswith('/'):
                    clean_path = '/' + clean_path
                # Keep query params
                query_string = request.META.get('QUERY_STRING', '')
                if query_string:
                    clean_path = f"{clean_path}?{query_string}"
                return redirect(clean_path)
            
            # Prepend the store prefix internally so Django routes to the correct view!
            if original_path == '/':
                request.path_info = f"/store/{brand.slug}/"
            else:
                request.path_info = f"/store/{brand.slug}{original_path}"
                
            request.path = request.path_info

        return self.get_response(request)
