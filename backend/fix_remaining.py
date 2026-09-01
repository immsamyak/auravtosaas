import re

files = [
    'apps/brands/templates/brands/store_account.html',
    'apps/orders/templates/orders/checkout.html',
    'apps/orders/templates/orders/order_success.html',
    'apps/orders/templates/orders/track_order.html'
]

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    # Catch any remaining neutral classes
    content = re.sub(r'bg-neutral-500/[0-9]+', 'bg-theme-bg-secondary', content)
    content = re.sub(r'border-neutral-500/[0-9]+', 'border-theme-border-subtle', content)
    
    # In track_order line 82: `opacity-70` was used with `bg-theme-text-primary`. This is fine.
    
    with open(filepath, 'w') as f:
        f.write(content)
        print(f"Cleaned up {filepath}")
