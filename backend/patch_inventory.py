import re

filepath = 'apps/inventory/models.py'
with open(filepath, 'r') as f:
    content = f.read()

replacement = """        # trigger notification if dropping to or below 5
        if self.quantity <= 5 and (is_new or (old_quantity is not None and old_quantity > 5)):
            from apps.core.utils import notify
            from apps.core.email_utils import dispatch_async_email
            brand = self.product_variant.product.brand
            
            # In-app notification
            notify(
                user=brand.owner,
                title="Low Stock Alert",
                message=f"{self.product_variant.product.name} ({self.product_variant.size.code}) is at {self.quantity} in {self.location.name}.",
                icon_class="fa-solid fa-triangle-exclamation text-rose-500",
                action_url=f"/dashboard/products/{self.product_variant.product.id}/"
            )
            
            # Email notification
            try:
                context = {
                    'product_name': self.product_variant.product.name,
                    'variant_name': str(self.product_variant),
                    'stock_level': self.quantity,
                }
                dispatch_async_email('low_inventory_alert', context, [brand.owner.email], brand)
            except Exception as e:
                pass
"""

# Replace the existing notification block
pattern = re.compile(r'        # trigger notification if dropping to or below 5\n.*?(?=\n\n    def __str__)', re.DOTALL)
content = pattern.sub(replacement, content)

with open(filepath, 'w') as f:
    f.write(content)
