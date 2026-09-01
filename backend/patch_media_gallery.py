import re

filepath = 'apps/brands/templates/brands/media_gallery.html'
with open(filepath, 'r') as f:
    content = f.read()

replacement = """ <!-- Product Images -->
 {% for p_img in product_images %}
 <div x-show="(activeTab === 'all' || activeTab === 'products') && (searchTerm === '' || '{{ p_img.product.name|lower|escapejs }}'.includes(searchTerm.toLowerCase()))" 
 x-transition
 class="group relative bg-theme-bg rounded-2xl border border-theme-border dark:border-slate-600/50/50 overflow-hidden hover:border-indigo-300 hover:shadow-md transition-all duration-200 aspect-square flex flex-col">
 <div class="flex-1 bg-theme-bg-secondary relative overflow-hidden flex items-center justify-center">
 <img src="{{ p_img.image.url }}" alt="{{ p_img.product.name }}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">
 
 <!-- Overlay Actions -->
 <div class="absolute inset-0 bg-slate-900/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3 backdrop-blur-[2px]">
 <a href="{{ p_img.image.url }}" target="_blank" class="w-8 h-8 bg-white/90 rounded-full flex items-center justify-center text-theme-text-secondary hover:text-indigo-600 hover:scale-110 transition-all" title="View">
 <i class="fa-solid fa-eye text-sm"></i>
 </a>
 </div>
 </div>
 <div class="p-3 bg-theme-surface border-t border-theme-border-subtle dark:border-slate-600/50/50">
 <p class="text-xs font-bold text-theme-text-primary truncate" title="{{ p_img.product.name }}">{{ p_img.product.name }}</p>
 <p class="text-[10px] font-medium text-theme-text-disabled mt-0.5">Product Image</p>
 </div>
 </div>
 {% endfor %}
 
 {% for v_img in product_variants %}
 <div x-show="(activeTab === 'all' || activeTab === 'products') && (searchTerm === '' || '{{ v_img.product.name|lower|escapejs }}'.includes(searchTerm.toLowerCase()))" 
 x-transition
 class="group relative bg-theme-bg rounded-2xl border border-theme-border dark:border-slate-600/50/50 overflow-hidden hover:border-indigo-300 hover:shadow-md transition-all duration-200 aspect-square flex flex-col">
 <div class="flex-1 bg-theme-bg-secondary relative overflow-hidden flex items-center justify-center">
 <img src="{{ v_img.image.url }}" alt="{{ v_img.product.name }}" class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">
 
 <!-- Overlay Actions -->
 <div class="absolute inset-0 bg-slate-900/40 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-3 backdrop-blur-[2px]">
 <a href="{{ v_img.image.url }}" target="_blank" class="w-8 h-8 bg-white/90 rounded-full flex items-center justify-center text-theme-text-secondary hover:text-indigo-600 hover:scale-110 transition-all" title="View">
 <i class="fa-solid fa-eye text-sm"></i>
 </a>
 </div>
 </div>
 <div class="p-3 bg-theme-surface border-t border-theme-border-subtle dark:border-slate-600/50/50">
 <p class="text-xs font-bold text-theme-text-primary truncate" title="{{ v_img.product.name }}">{{ v_img.product.name }}</p>
 <p class="text-[10px] font-medium text-theme-text-disabled mt-0.5">Product Variant Image</p>
 </div>
 </div>
 {% endfor %}"""

pattern = re.compile(r' <!-- Product Images -->\n {% for p_img in product_images %}.*?{% endfor %}', re.DOTALL)

if pattern.search(content):
    content = pattern.sub(replacement, content)
    with open(filepath, 'w') as f:
        f.write(content)
    print("Patched apps/brands/templates/brands/media_gallery.html successfully.")
else:
    print("Pattern not found in apps/brands/templates/brands/media_gallery.html!")
