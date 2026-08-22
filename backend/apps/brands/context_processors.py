from apps.brands.models import Brand, PopupBanner

def storefront_popups(request):
    """
    Context processor to inject active popups into the storefront templates.
    Extracts the brand slug from the URL resolver and fetches active popups.
    """
    try:
        if getattr(request, 'resolver_match', None) and 'slug' in request.resolver_match.kwargs:
            slug = request.resolver_match.kwargs.get('slug')
            brand = Brand.objects.get(slug=slug)
            
            # Get active popups for this brand
            popups = PopupBanner.objects.filter(brand=brand, is_active=True).order_by('-created_at')
            return {'storefront_popups': popups}
    except Exception:
        pass
        
    return {}
