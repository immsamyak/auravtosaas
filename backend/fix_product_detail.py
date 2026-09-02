filepath = 'apps/brands/templates/brands/store_product_detail.html'
with open(filepath, 'r') as f:
    content = f.read()

target_button = """                        <button type="button" 
                                @click="$store.cart.add({id: currentVariant ? currentVariant.id : '{{product.id}}', name: '{{product.name|escapejs}}', price: {{product.price}}, variant_name: (currentVariant ? (currentVariant.color_name + ' / ' + currentVariant.size_code) : ''), image: currentImageUrl}); window.showToast('Added to cart', 'success');" 
                                :disabled="isTryOnDisabled" 
                                :class="isTryOnDisabled ? 'opacity-50 cursor-not-allowed' : 'hover:opacity-70'" 
                                class="flex-1 border border-current bg-transparent py-4 px-8 flex items-center justify-center text-sm font-bold uppercase tracking-widest transition-opacity">
                            <i class="fa-solid fa-cart-plus mr-2"></i> Add to Cart
                        </button>"""

replacement_button = """                        <button type="button" 
                                @click="$store.cart.add({id: currentVariant ? currentVariant.id : '{{product.id}}', name: '{{product.name|escapejs}}', price: {{product.price}}, variant_name: (currentVariant ? (currentVariant.color_name + ' / ' + currentVariant.size_code) : ''), image: currentImageUrl}); window.showToast('Added to cart', 'success');" 
                                :disabled="!currentVariant || currentVariant.stock <= 0" 
                                :class="(!currentVariant || currentVariant.stock <= 0) ? 'opacity-50 cursor-not-allowed bg-theme-bg' : 'hover:opacity-70'" 
                                class="flex-1 border border-current bg-transparent py-4 px-8 flex items-center justify-center text-sm font-bold uppercase tracking-widest transition-opacity">
                            <template x-if="currentVariant && currentVariant.stock > 0">
                                <span><i class="fa-solid fa-cart-plus mr-2"></i> Add to Cart</span>
                            </template>
                            <template x-if="!currentVariant || currentVariant.stock <= 0">
                                <span><i class="fa-solid fa-box-open mr-2"></i> Out of Stock</span>
                            </template>
                        </button>"""

if target_button in content:
    content = content.replace(target_button, replacement_button)

with open(filepath, 'w') as f:
    f.write(content)
