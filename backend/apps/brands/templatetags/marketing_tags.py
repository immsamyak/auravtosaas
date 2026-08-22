from django import template
from apps.brands.models import PopupBanner

register = template.Library()

@register.inclusion_tag('brands/marketing/popup_injector.html', takes_context=True)
def render_brand_popups(context):
    request = context.get('request')
    brand = context.get('brand')
    
    if not brand or not request:
        return {'popups': []}
        
    current_path = request.path
    
    # Fetch active popups for this brand
    popups = PopupBanner.objects.filter(brand=brand, is_active=True)
    
    valid_popups = []
    for popup in popups:
        if popup.display_rule == 'ALL_PAGES':
            valid_popups.append(popup)
        elif popup.display_rule == 'HOMEPAGE_ONLY' and current_path == f'/store/{brand.slug}/':
            valid_popups.append(popup)
        elif popup.display_rule == 'SPECIFIC_URL' and popup.specific_url in current_path:
            valid_popups.append(popup)
            
    return {'popups': valid_popups}
