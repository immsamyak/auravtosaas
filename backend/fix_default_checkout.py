import os
import re

checkout_file = 'apps/orders/templates/orders/checkout.html'
with open(checkout_file, 'r') as f:
    content = f.read()
    
# Just check if window.STOCK_DICT is there
if 'window.STOCK_DICT' not in content:
    # Append the script
    content = content.replace('{% block content %}', '{% block content %}\n<script>window.STOCK_DICT = {{ stock_json|safe|default:"{}" }};</script>', 1)
    
    out_of_stock_badge = """
<template x-if="window.STOCK_DICT && window.STOCK_DICT[item.id] <= 0">
  <div class="text-[10px] text-red-600 font-bold bg-red-100 px-2 py-1 rounded inline-block mt-1 uppercase tracking-widest border border-red-200">
    Out of Stock - Remove to continue
  </div>
</template>
"""
    disable_attrs = """ :disabled="$store.cart.items.some(i => window.STOCK_DICT && window.STOCK_DICT[i.id] <= 0)" :class="$store.cart.items.some(i => window.STOCK_DICT && window.STOCK_DICT[i.id] <= 0) ? 'opacity-50 cursor-not-allowed' : ''" """

    pattern = re.compile(r'(x-text="item\.name"[^>]*>[\s\S]*?</[a-zA-Z0-9]+>)')
    if pattern.search(content):
        content = pattern.sub(r'\1\n' + out_of_stock_badge, content)
        
    content = content.replace('<button type="submit"', '<button type="submit"' + disable_attrs)
    
    with open(checkout_file, 'w') as f:
        f.write(content)
    print("Fixed default checkout.html")
