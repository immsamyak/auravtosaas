def notify(user, title, message, icon_class="fa-solid fa-bell", action_url=None):
    """
    Helper function to create notifications.
    """
    from apps.core.models import Notification
    
    if not user:
        return None
        
    return Notification.objects.create(
        user=user,
        title=title,
        message=message,
        icon_class=icon_class,
        action_url=action_url
    )

def get_brand_url(brand=None):
    """
    Get the full URL for a brand based on its custom domain or fallback to a localhost URL for development.
    """
    from django.conf import settings
    base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
    
    if not brand:
        return base_url

    # In production/staging with custom domains, you would check brand.custom_domain
    if getattr(brand, 'custom_domain', None):
        return f"https://{brand.custom_domain}"
    
    # Fallback to local routing
    # Check if we should use subdomain routing (e.g., brand_slug.domain.com)
    protocol = "https" if "https" in base_url else "http"
    base_domain = base_url.split("://")[-1]
    
    if hasattr(brand, 'slug'):
        return f"{protocol}://{brand.slug}.{base_domain}"
    
    return base_url
