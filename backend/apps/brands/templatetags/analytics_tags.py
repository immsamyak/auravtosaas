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
            
    # Check for TikTok Pixel
    tiktok_integration = BrandIntegration.objects.filter(brand=brand, integration__provider_code='TIKTOK_PIXEL', is_active=True).first()
    if tiktok_integration:
        pixel_id = tiktok_integration.credentials.get('pixel_id')
        if pixel_id:
            scripts.append(f"""
            <!-- TikTok Pixel Code -->
            <script>
            !function (w, d, t) {{
              w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"];ttq.setAndDefer=function(t,e){{t[e]=function(){{t.push([e].concat(Array.prototype.slice.call(arguments,0)))}}}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){{for(var e=ttq._sq[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e}};ttq.load=function(e,n){{var i="https://analytics.tiktok.com/i18n/pixel/events.js";ttq._i=ttq._i||{{}},ttq._i[e]=[],ttq._i[e]._u=i,ttq._t=ttq._t||{{}},ttq._t[e]=+new Date,ttq._o=ttq._o||{{}},ttq._o[e]=n||{{}};var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=i+"?sdkid="+e+"&lib="+t;var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)}};
              ttq.load('{pixel_id}');
              ttq.page();
            }}(window, document, 'ttq');
            </script>
            <!-- End TikTok Pixel Code -->
            """)

    # Check for Klaviyo
    klaviyo_integration = BrandIntegration.objects.filter(brand=brand, integration__provider_code='KLAVIYO', is_active=True).first()
    if klaviyo_integration:
        public_key = klaviyo_integration.credentials.get('public_api_key')
        if public_key:
            scripts.append(f"""
            <!-- Klaviyo Onsite Tracking -->
            <script type="text/javascript" async src="https://static.klaviyo.com/onsite/js/klaviyo.js?company_id={public_key}"></script>
            """)

    # Check for Hotjar
    hotjar_integration = BrandIntegration.objects.filter(brand=brand, integration__provider_code='HOTJAR', is_active=True).first()
    if hotjar_integration:
        site_id = hotjar_integration.credentials.get('site_id')
        if site_id:
            scripts.append(f"""
            <!-- Hotjar Tracking Code -->
            <script>
                (function(h,o,t,j,a,r){{
                    h.hj=h.hj||function(){{(h.hj.q=h.hj.q||[]).push(arguments)}};
                    h._hjSettings={{hjid:{site_id},hjsv:6}};
                    a=o.getElementsByTagName('head')[0];
                    r=o.createElement('script');r.async=1;
                    r.src=t+h._hjSettings.hjid+j+h._hjSettings.hjsv;
                    a.appendChild(r);
                }})(window,document,'https://static.hotjar.com/c/hotjar-','.js?sv=');
            </script>
            """)

    # Check for Tawk.to
    tawk_integration = BrandIntegration.objects.filter(brand=brand, integration__provider_code='TAWK_TO', is_active=True).first()
    if tawk_integration:
        property_id_raw = tawk_integration.credentials.get('property_id', '')
        # Robustly parse property_id in case user pasted the full script or full URL
        import re
        # Look for the Tawk.to ID pattern (24 alphanumeric characters optionally followed by /widget_id)
        match = re.search(r'embed\.tawk\.to/([a-zA-Z0-9]{24}(?:/[a-zA-Z0-9_-]+)?)', property_id_raw)
        if match:
            property_id = match.group(1)
        else:
            # Maybe they just pasted the ID itself
            match_id = re.search(r'^([a-zA-Z0-9]{24}(?:/[a-zA-Z0-9_-]+)?)$', property_id_raw.strip())
            property_id = match_id.group(1) if match_id else None
            
        if property_id:
            # If it already includes the widget ID (like /default or /123), we don't append /default
            append_default = "" if "/" in property_id else "/default"
            scripts.append(f"""
            <!--Start of Tawk.to Script-->
            <script type="text/javascript">
            var Tawk_API=Tawk_API||{{}}, Tawk_LoadStart=new Date();
            (function(){{
            var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
            s1.async=true;
            s1.src='https://embed.tawk.to/{property_id}{append_default}';
            s1.charset='UTF-8';
            s1.setAttribute('crossorigin','*');
            s0.parentNode.insertBefore(s1,s0);
            }})();
            </script>
            <!--End of Tawk.to Script-->
            """)

    # Check for WhatsApp Widget
    from django.db.models import Q
    wa_integration = BrandIntegration.objects.filter(
        Q(integration__provider_code='WHATSAPP_WIDGET') | Q(integration__provider_code='WHATSAPP'),
        brand=brand, 
        is_active=True
    ).first()
    
    if wa_integration:
        phone = wa_integration.credentials.get('phone_number') or wa_integration.credentials.get('whatsapp_number')
        if phone:
            scripts.append(f"""
            <a href="https://wa.me/{phone}" target="_blank" style="position: fixed; bottom: 24px; right: 24px; background-color: #25D366; color: white; width: 56px; height: 56px; border-radius: 50%; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); z-index: 50; transition: transform 0.2s;" onmouseover="this.style.transform='scale(1.1)';" onmouseout="this.style.transform='scale(1)';">
                <i class="fa-brands fa-whatsapp" style="font-size: 30px;"></i>
            </a>
            """)
            
    return mark_safe("\n".join(scripts))
