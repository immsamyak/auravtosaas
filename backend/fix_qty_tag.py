import os
import re

old_badge = """
<template x-if="window.STOCK_DICT && window.STOCK_DICT[item.id] <= 0">
  <div class="text-[10px] text-red-600 font-bold bg-red-100 px-2 py-1 rounded inline-block mt-1 uppercase tracking-widest border border-red-200">
    Out of Stock - Remove to continue
  </div>
</template>
"""

new_badge = """
<template x-if="window.STOCK_DICT && window.STOCK_DICT[item.id] <= 0">
  <span class="ml-2 text-[10px] text-red-600 font-bold bg-red-100 px-1.5 py-0.5 rounded uppercase tracking-widest border border-red-200">NO STOCK</span>
</template>
"""

storefront_dir = 'templates/storefront'

def fix_file(filepath):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r') as f:
        content = f.read()
        
    modified = False
    
    if old_badge in content:
        content = content.replace(old_badge, '')
        modified = True
        
    if new_badge not in content:
        qty_pattern = re.compile(r'(<p[^>]*x-text="`Qty: \${item\.quantity}`"[^>]*></p>)')
        if qty_pattern.search(content):
            # Wrap the QTY and the new badge in a flex container to keep them side by side
            content = qty_pattern.sub(r'<div class="flex items-center">\n\1\n' + new_badge.strip() + '\n</div>', content)
            modified = True
            
    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Fixed {filepath}")

for theme in os.listdir(storefront_dir):
    if not theme.startswith('theme_'):
        continue
    
    checkout_file = os.path.join(storefront_dir, theme, 'checkout.html')
    fix_file(checkout_file)

fix_file('apps/orders/templates/orders/checkout.html')
