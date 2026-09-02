import os
import re

messages_html = """
<script>
    window.STOCK_DICT = {{ stock_json|safe|default:"{}" }};
</script>
{% if messages %}
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
    {% for message in messages %}
    <div class="p-4 rounded-xl mb-4 text-sm font-bold shadow-sm {% if message.tags == 'error' %}bg-red-100 text-red-700 border border-red-200{% elif message.tags == 'success' %}bg-green-100 text-green-700 border border-green-200{% else %}bg-blue-100 text-blue-700 border border-blue-200{% endif %}">
        <i class="fa-solid fa-circle-exclamation mr-2"></i> {{ message }}
    </div>
    {% endfor %}
</div>
{% endif %}
"""

out_of_stock_badge = """
<template x-if="window.STOCK_DICT && window.STOCK_DICT[item.id] <= 0">
  <div class="text-[10px] text-red-600 font-bold bg-red-100 px-2 py-1 rounded inline-block mt-1 uppercase tracking-widest border border-red-200">
    Out of Stock - Remove to continue
  </div>
</template>
"""

disable_attrs = """ :disabled="$store.cart.items.some(i => window.STOCK_DICT && window.STOCK_DICT[i.id] <= 0)" :class="$store.cart.items.some(i => window.STOCK_DICT && window.STOCK_DICT[i.id] <= 0) ? 'opacity-50 cursor-not-allowed' : ''" """

storefront_dir = 'templates/storefront'

for theme in os.listdir(storefront_dir):
    if not theme.startswith('theme_'):
        continue
    
    checkout_file = os.path.join(storefront_dir, theme, 'checkout.html')
    if os.path.exists(checkout_file):
        with open(checkout_file, 'r') as f:
            content = f.read()
            
        modified = False
        
        # 1. Inject Messages Block
        if 'window.STOCK_DICT' not in content:
            # Inject after {% block content %}
            content = content.replace('{% block content %}', '{% block content %}\n' + messages_html, 1)
            modified = True
            
        # 2. Inject Out of Stock Badge in Order Summary
        if 'Out of Stock - Remove to continue' not in content:
            # Find x-text="item.name"
            # It usually looks like `x-text="item.name"></h3>` or `x-text="item.name"></span>`
            # Let's replace `x-text="item.name"></h3>` with `x-text="item.name"></h3>` + badge
            pattern = re.compile(r'(x-text="item\.name"[^>]*>[\s\S]*?</[a-zA-Z0-9]+>)')
            if pattern.search(content):
                content = pattern.sub(r'\1\n' + out_of_stock_badge, content)
                modified = True
                
        # 3. Disable Submit Button
        if '$store.cart.items.some' not in content:
            # Find <button type="submit" ...> and inject disable_attrs
            # Be careful not to mess up existing bindings if any.
            # We'll just replace `<button type="submit"` with `<button type="submit" <disable_attrs>`
            content = content.replace('<button type="submit"', '<button type="submit"' + disable_attrs)
            modified = True
            
        if modified:
            with open(checkout_file, 'w') as f:
                f.write(content)
            print(f"Fixed {theme}/checkout.html")
            
