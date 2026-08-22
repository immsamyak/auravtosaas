from django import template
from django.utils.safestring import mark_safe
from apps.brands.models import BrandIntegration

register = template.Library()

@register.simple_tag
def render_brand_analytics(brand):
    """
    Injects Google Analytics and Meta Pixel scripts if the brand has configured them.
    """
    if not brand:
        return ""
        
    scripts = []
    
    # Check for GA4
    ga4_integration = BrandIntegration.objects.filter(
        brand=brand, 
        integration__provider_code='GA4', 
        is_active=True
    ).first()
    
    if ga4_integration:
        measurement_id = ga4_integration.credentials.get('merchant_id') # We mapped ID to merchant_id in UI
        if measurement_id:
            scripts.append(f"""
            <!-- Google tag (gtag.js) -->
            <script async src="https://www.googletagmanager.com/gtag/js?id={measurement_id}"></script>
            <script>
              window.dataLayer = window.dataLayer || [];
              function gtag(){{dataLayer.push(arguments);}}
              gtag('js', new Date());

              gtag('config', '{measurement_id}');
            </script>
            """)
            
    # Check for Meta Pixel
    meta_integration = BrandIntegration.objects.filter(
        brand=brand, 
        integration__provider_code='META_PIXEL', 
        is_active=True
    ).first()
    
    if meta_integration:
        pixel_id = meta_integration.credentials.get('merchant_id')
        if pixel_id:
            scripts.append(f"""
            <!-- Meta Pixel Code -->
            <script>
            !function(f,b,e,v,n,t,s)
            {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
            n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
            if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
            n.queue=[];t=b.createElement(e);t.async=!0;
            t.src=v;s=b.getElementsByTagName(e)[0];
            s.parentNode.insertBefore(t,s)}}(window, document,'script',
            'https://connect.facebook.net/en_US/fbevents.js');
            fbq('init', '{pixel_id}');
            fbq('track', 'PageView');
            </script>
            <noscript><img height="1" width="1" style="display:none"
            src="https://www.facebook.com/tr?id={pixel_id}&ev=PageView&noscript=1"
            /></noscript>
            <!-- End Meta Pixel Code -->
            """)
            
    return mark_safe("\n".join(scripts))
