import re

with open('apps/orders/admin.py', 'r') as f:
    content = f.read()

new_order_admin = """
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'brand', 'user', 'status', 'total_amount', 'shipping_cost', 'created_at')
    list_filter = ('status', 'brand', 'created_at')
    search_fields = ('id', 'user__username', 'brand__name')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': (('brand', 'user'), ('status', 'created_at')),
            'classes': ('tab',)
        }),
        ('Financials', {
            'fields': (('total_amount', 'shipping_cost'), ('tax_amount', 'tax_rate')),
            'classes': ('tab',)
        }),
        ('Shipping Details', {
            'fields': ('shipping_address', 'shipping_city', 'shipping_postal_code'),
            'classes': ('tab',)
        }),
    )
    readonly_fields = ('created_at',)
"""

content = re.sub(r'@admin\.register\(Order\)\nclass OrderAdmin\(ModelAdmin\):.*?(?=@admin\.register|class CartItemInline)', new_order_admin + "\n", content, flags=re.DOTALL)

with open('apps/orders/admin.py', 'w') as f:
    f.write(content)
print("Updated orders admin")
