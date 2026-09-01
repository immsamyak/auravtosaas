import re

files = [
    'apps/brands/templates/brands/store_account.html',
    'apps/orders/templates/orders/checkout.html',
    'apps/orders/templates/orders/order_success.html',
    'apps/orders/templates/orders/track_order.html'
]

replacements = [
    (r'bg-neutral-500/5', 'bg-theme-surface'),
    (r'bg-neutral-500/10', 'bg-theme-bg-secondary'),
    (r'bg-neutral-500/20', 'bg-theme-bg-secondary'),
    (r'border-neutral-500/20', 'border-theme-border-subtle'),
    (r'border-neutral-500/30', 'border-theme-border'),
    (r'border-neutral-500/40', 'border-theme-border'),
    (r'backdrop-blur-xl', ''),
    (r'backdrop-blur-2xl', ''),
    (r'backdrop-blur-md', ''),
    (r'mix-blend-exclusion', ''),
    (r'mix-blend-difference', ''),
    (r'mix-blend-multiply', ''),
    (r'mix-blend-normal', ''),
    (r'dark:mix-blend-normal', ''),
    (r'invert', ''),
    (r'text-current', 'text-theme-text-primary'),
    (r'border-current', 'border-theme-border'),
    (r'bg-current', 'bg-theme-text-primary'),
    (r'focus:border-current/40', 'focus:border-theme-border'),
    (r'focus:ring-current/30', 'focus:ring-theme-text-primary/30'),
    (r'focus:border-current', 'focus:border-theme-border'),
    (r'focus:ring-current', 'focus:ring-theme-text-primary/30'),
    (r'border-current/30', 'border-theme-border-subtle'),
    (r'placeholder-neutral-500/50', 'placeholder-theme-text-muted'),
    (r'text-white', 'text-theme-bg'), # In Buttons
]

# specific tweaks for text-white context inside buttons
for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()

    for old, new in replacements:
        content = re.sub(old, new, content)
    
    # Fix spans used for hacky styling
    content = re.sub(r'<span class="absolute inset-0 w-full h-full bg-theme-surface  pointer-events-none( rounded-full)?"></span>', '', content)
    
    # The text-theme-bg might look weird if applied globally where text-white was. 
    # Actually let's just make sure "text-theme-bg" is only in elements with bg-theme-text-primary
    
    # Fix the group-hover:scale-105 issue that was attached to the text span
    content = re.sub(r'<span class="relative z-10  text-theme-bg(.*?)">', r'<span class="relative z-10 \1">', content)
    content = re.sub(r'<span class="relative z-10  text-theme-bg">', '<span>', content)

    # Some specific cleanups
    content = re.sub(r'style="color: var\(--tw-prose-body\);"', '', content)
    content = re.sub(r'style=""', '', content)

    with open(filepath, 'w') as f:
        f.write(content)
        print(f"Updated {filepath}")
