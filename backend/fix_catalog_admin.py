import re

with open('apps/catalog/admin.py', 'r') as f:
    content = f.read()

# I will write a highly customized ModelAdmin for Product
new_product_admin = """
@admin.register(Product)
class ProductAdmin(ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'brand', 'category', 'product_type', 'price', 'is_vto_ready', 'occasion', 'created_at')
    list_filter = ('brand', 'category', 'product_type', 'is_vto_ready', 'occasion', 'created_at')
    search_fields = ('name', 'brand__name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariantInline]
    filter_horizontal = ('style_tags',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': (('name', 'slug'), 'brand', 'description'),
            'classes': ('tab',)
        }),
        ('Classification', {
            'fields': (('category', 'product_type'), ('occasion', 'fit')),
            'classes': ('tab',)
        }),
        ('Pricing & Status', {
            'fields': ('price', 'is_vto_ready', 'style_tags'),
            'classes': ('tab',)
        }),
    )
"""
content = re.sub(r'@admin\.register\(Product\)\nclass ProductAdmin\(ModelAdmin\):.*?(?=@admin\.register)', new_product_admin + "\n", content, flags=re.DOTALL)

with open('apps/catalog/admin.py', 'w') as f:
    f.write(content)
print("Updated catalog admin")
