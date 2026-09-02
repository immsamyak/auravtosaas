import os
import re

cart_slideover_html = """
<!-- Cart Slide-over -->
<div aria-labelledby="slide-over-title" aria-modal="true" class="fixed inset-0 z-[100] overflow-hidden" role="dialog" style="display: none;" x-show="isCartOpen">
<div @click="isCartOpen = false" class="absolute inset-0 bg-black/60 backdrop-blur-sm transition-opacity" x-show="isCartOpen" x-transition.opacity=""></div>
<div class="fixed inset-y-0 right-0 pl-10 max-w-full flex">
<div @click.stop="" class="w-screen max-w-md transform transition ease-in-out duration-500 sm:duration-700" x-show="isCartOpen" x-transition:enter="translate-x-full" x-transition:enter-end="translate-x-0" x-transition:enter-start="translate-x-full" x-transition:leave="translate-x-0" x-transition:leave-end="translate-x-full" x-transition:leave-start="translate-x-0">
<div class="h-full flex flex-col bg-theme-surface shadow-xl overflow-y-scroll text-black">
<!-- Cart Header -->
<div class="flex-1 py-6 overflow-y-auto px-4 sm:px-6">
<div class="flex items-start justify-between">
<h2 class="text-xl font-bold text-theme-text-primary" id="slide-over-title">Shopping Cart</h2>
<div class="ml-3 h-7 flex items-center">
<button @click="isCartOpen = false" class="-m-2 p-2 text-theme-text-disabled hover:text-gray-500" type="button">
<span class="sr-only">Close panel</span>
<i class="fa-solid fa-xmark text-xl"></i>
</button>
</div>
</div>
<div class="mt-8">
<div class="flow-root">
<ul class="-my-6 divide-y divide-gray-200" role="list">
<template x-if="$store.cart.items.length === 0">
<li class="py-12 text-center">
<i class="fa-solid fa-bag-shopping text-4xl text-gray-300 mb-4"></i>
<p class="text-theme-text-muted font-medium">Your cart is currently empty.</p>
</li>
</template>
<template :key="index" x-for="(item, index) in $store.cart.items">
<li class="py-6 flex">
<div class="flex-shrink-0 w-24 h-24 border border-theme-border rounded-md overflow-hidden bg-theme-bg">
<img :alt="item.name" :src="item.image" class="w-full h-full object-center object-cover"/>
</div>
<div class="ml-4 flex-1 flex flex-col">
<div>
<div class="flex justify-between text-base font-medium text-theme-text-primary">
<h3 x-text="item.name"></h3>
<p class="ml-4" x-text="'{{ brand.currency_symbol|default:'$'|escapejs }}' + (item.price * item.quantity).toFixed(2)"></p>
</div>
<p class="mt-1 text-sm text-theme-text-muted" x-text="(!item.variant_name || item.variant_name === 'undefined / undefined') ? '' : item.variant_name"></p>
</div>
<div class="flex-1 flex items-end justify-between text-sm">
<p class="text-theme-text-muted">Qty <span x-text="item.quantity"></span></p>
<div class="flex">
<button @click="$store.cart.remove(index)" class="font-medium text-red-600 hover:text-red-500" type="button">Remove</button>
</div>
</div>
</div>
</li>
</template>
</ul>
</div>
</div>
</div>
<!-- Cart Footer -->
<div class="border-t border-theme-border py-6 px-4 sm:px-6">
<div class="flex justify-between text-lg font-bold text-theme-text-primary">
<p>Subtotal</p>
<p x-text="'{{ brand.currency_symbol|default:'$'|escapejs }}' + $store.cart.total.toFixed(2)"></p>
</div>
<p class="mt-0.5 text-sm text-theme-text-muted">Shipping and taxes calculated at checkout.</p>
<div class="mt-6">
<form method="POST" action="{% url 'storefront_checkout' brand.slug %}">
{% csrf_token %}
<input type="hidden" name="cart_data" :value="JSON.stringify($store.cart.items)">
<button type="submit" class="w-full flex items-center justify-center rounded-md border border-transparent bg-black px-6 py-3 text-base font-medium text-white shadow-sm hover:bg-gray-800" :disabled="$store.cart.items.length === 0" :class="$store.cart.items.length === 0 ? 'opacity-50 cursor-not-allowed' : ''">
Checkout
</button>
</form>
</div>
<div class="mt-6 flex justify-center text-sm text-center text-theme-text-muted">
<p>
or <button @click="isCartOpen = false" class="text-black font-medium hover:text-gray-700" type="button">Continue Shopping<span aria-hidden="true"> &rarr;</span></button>
</p>
</div>
</div>
</div>
</div>
</div>
</div>
"""

out_of_stock_badge = """
 {% if product.total_stock <= 0 %}
 <div class="absolute top-3 left-3 bg-red-600 text-white px-3 py-1 text-[10px] font-bold uppercase tracking-widest shadow-sm z-20">Out of Stock</div>
 {% endif %}
"""

storefront_dir = 'templates/storefront'

for theme in os.listdir(storefront_dir):
    if not theme.startswith('theme_'):
        continue
    
    theme_path = os.path.join(storefront_dir, theme)
    base_file = os.path.join(theme_path, 'base.html')
    
    if os.path.exists(base_file):
        with open(base_file, 'r') as f:
            content = f.read()
        
        if '<!-- Cart Slide-over -->' not in content:
            # Append cart slideover right before </body>
            if '</body>' in content:
                content = content.replace('</body>', cart_slideover_html + '\n</body>')
                with open(base_file, 'w') as f:
                    f.write(content)
                print(f"Added cart slide-over to {theme}/base.html")
    
    products_file = os.path.join(theme_path, 'sections', 'products.html')
    if os.path.exists(products_file):
        with open(products_file, 'r') as f:
            content = f.read()
            
        if 'Out of Stock' not in content:
            # Usually the product card starts with an <a> tag and then an image
            # Let's insert the badge after '<a class="..." href="...">\n'
            # We can use regex to find `<a ... href="{% url 'store_product_detail' ... %}">`
            pattern = re.compile(r'(<a[^>]*href="{% url \'store_product_detail\' [^}]* %}"[^>]*>)')
            new_content = pattern.sub(r'\1' + out_of_stock_badge, content)
            
            if new_content != content:
                with open(products_file, 'w') as f:
                    f.write(new_content)
                print(f"Added Out of Stock badge to {theme}/sections/products.html")
