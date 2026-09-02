filepath = 'apps/brands/templates/brands/store_shop.html'
with open(filepath, 'r') as f:
    content = f.read()

target_badge = """                            {% if product.is_new %}
                            <div class="absolute top-4 left-4 z-10">
                                <span class="bg-theme-text-primary text-theme-bg text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-full">New</span>
                            </div>
                            {% endif %}"""

replacement_badge = """                            {% if product.total_stock <= 0 %}
                            <div class="absolute top-4 left-4 z-10">
                                <span class="bg-red-500 text-white text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-full shadow-lg">Out of Stock</span>
                            </div>
                            {% elif product.is_new %}
                            <div class="absolute top-4 left-4 z-10">
                                <span class="bg-theme-text-primary text-theme-bg text-xs font-bold px-3 py-1 uppercase tracking-wider rounded-full">New</span>
                            </div>
                            {% endif %}"""

if target_badge in content:
    content = content.replace(target_badge, replacement_badge)

with open(filepath, 'w') as f:
    f.write(content)
