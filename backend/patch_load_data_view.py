import re

filepath = 'apps/orders/views.py'
with open(filepath, 'r') as f:
    content = f.read()

# Add logic to shipping_settings_view
import_str = "    from apps.orders.models import DeliveryProvince, DeliveryDistrict, DeliveryCity\n"
new_logic = """    from apps.orders.models import DeliveryProvince, DeliveryDistrict, DeliveryCity
    import json
    import urllib.request
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'load_default_data':
            country_iso2 = request.POST.get('country_iso2')
            if country_iso2:
                try:
                    # Fetch states
                    req_states = urllib.request.Request(
                        "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/json/states.json",
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req_states) as url:
                        states_data = json.loads(url.read().decode())
                        
                    # Fetch cities (we map to districts)
                    req_cities = urllib.request.Request(
                        "https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/json/cities.json",
                        headers={'User-Agent': 'Mozilla/5.0'}
                    )
                    with urllib.request.urlopen(req_cities) as url:
                        cities_data = json.loads(url.read().decode())
                        
                    country_states = [s for s in states_data if s.get('country_code') == country_iso2]
                    
                    prov_created = 0
                    dist_created = 0
                    
                    for state in country_states:
                        prov, created = DeliveryProvince.objects.get_or_create(
                            brand=brand,
                            name=state['name']
                        )
                        if created: prov_created += 1
                        
                        # Find cities for this state
                        state_cities = [c for c in cities_data if c.get('state_code') == state['state_code'] and c.get('country_code') == country_iso2]
                        
                        for city in state_cities:
                            dist, d_created = DeliveryDistrict.objects.get_or_create(
                                province=prov,
                                name=city['name']
                            )
                            if d_created: dist_created += 1
                            
                    messages.success(request, f"Loaded {prov_created} provinces and {dist_created} districts for {country_iso2}.")
                except Exception as e:
                    messages.error(request, f"Failed to load data: {str(e)}")
            return redirect('shipping_settings')
"""
content = content.replace("    from apps.orders.models import DeliveryProvince, DeliveryDistrict, DeliveryCity\n    \n    if request.method == 'POST':\n        action = request.POST.get('action')", new_logic)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated views.py with load default logic")
