import re

html_files = ['aura_codecanyon_preview.html', 'codecanyon-preview/index.html']

admin_replace = """<ul class="space-y-3 text-slate-300 text-sm">
                        <li class="flex gap-2 items-start"><span class="text-indigo-400">&check;</span> <span><strong>Store Network & Commerce:</strong> Brands & Tenants, Store Themes, Global Orders, Gift Cards, Return Requests.</span></li>
                        <li class="flex gap-2 items-start"><span class="text-indigo-400">&check;</span> <span><strong>Catalog & Inventory:</strong> Products, Variants, Collections, AI Profiles, Size Charts, Stock Levels, Shipping Zones.</span></li>
                        <li class="flex gap-2 items-start"><span class="text-indigo-400">&check;</span> <span><strong>Virtual Try-On Engine:</strong> VTO Jobs, Queue Dashboard, Fit Passports, Wardrobe Looks, Photo Vault.</span></li>
                        <li class="flex gap-2 items-start"><span class="text-indigo-400">&check;</span> <span><strong>Platform Settings & API:</strong> Global Config, Subscriptions, Developer API, Webhooks, Security Audit Logs.</span></li>
                    </ul>"""

brand_replace = """<ul class="space-y-3 text-slate-300 text-sm">
                        <li class="flex gap-2 items-start"><span class="text-purple-400">&check;</span> <span><strong>Analytics & Reports:</strong> Deep-dive Finance and Store Overview Analytics.</span></li>
                        <li class="flex gap-2 items-start"><span class="text-purple-400">&check;</span> <span><strong>Store Management:</strong> Catalog, Orders, Returns, Abandoned Carts, Point of Sale (POS), Warehouses.</span></li>
                        <li class="flex gap-2 items-start"><span class="text-purple-400">&check;</span> <span><strong>Marketing:</strong> Popup Banners, Coupons, Subscribers, and Email Campaigns.</span></li>
                        <li class="flex gap-2 items-start"><span class="text-purple-400">&check;</span> <span><strong>Configuration:</strong> Brand Settings, Team Management, Billing, Theme Gallery, Add-ons.</span></li>
                    </ul>"""

for f in html_files:
    with open(f, 'r') as file:
        content = file.read()
    
    # Replace Admin list
    content = re.sub(
        r'<ul class="space-y-4 text-slate-300">(?:.*?)</ul>', 
        admin_replace, 
        content, 
        count=1, 
        flags=re.DOTALL
    )
    
    # Replace Brand list
    content = re.sub(
        r'<ul class="space-y-4 text-slate-300">(?:.*?)</ul>', 
        brand_replace, 
        content, 
        count=1, 
        flags=re.DOTALL
    )
    
    # Update Admin Demo link
    content = content.replace('href="/admin/"', 'href="https://aura.alvicsxinfo.tech/admin/login" target="_blank"')
    
    # Update Brand Demo link & credentials
    content = content.replace('User: randomowner', 'User: alvics')
    content = content.replace('href="/dashboard/"', 'href="https://aura.alvicsxinfo.tech/login" target="_blank"')
    
    # Update Customer link (if known, but assuming standard)
    content = content.replace('href="/accounts/login/"', 'href="https://aura.alvicsxinfo.tech/accounts/login/" target="_blank"')
    
    with open(f, 'w') as file:
        file.write(content)

# Fix DEMO_CREDENTIALS.md
with open('DEMO_CREDENTIALS.md', 'r') as file:
    demo = file.read()

demo = demo.replace('`https://api.raptipublic.edu.np` (Or your configured domain)', '`https://aura.alvicsxinfo.tech`')
demo = demo.replace('**Login URL**: `/admin/`', '**Login URL**: `https://aura.alvicsxinfo.tech/admin/login`')
demo = demo.replace('**Login URL**: `/dashboard/`', '**Login URL**: `https://aura.alvicsxinfo.tech/login`')
demo = demo.replace('**Username**: `randomowner`', '**Username**: `alvics`')
demo = demo.replace('**Login URL**: `/accounts/login/`', '**Login URL**: `https://aura.alvicsxinfo.tech/accounts/login/`')

with open('DEMO_CREDENTIALS.md', 'w') as file:
    file.write(demo)

print("Updates applied.")
