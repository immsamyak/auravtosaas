import re

filepath = 'apps/brands/views.py'
with open(filepath, 'r') as f:
    content = f.read()

# Store Account View
account_pattern = re.compile(r"    return render\(request, \'brands/store_account\.html\', \{")
account_replacement = """    template_name = f"storefront/{brand.theme.template_folder}/account.html" if brand.theme and brand.theme.is_active else 'brands/store_account.html'
    
    return render(request, template_name, {"""
content = account_pattern.sub(account_replacement, content)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated apps/brands/views.py")
