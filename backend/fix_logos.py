import re
import glob

files = glob.glob('templates/storefront/theme_*/sections/logo_list.html')
files.append('templates/storefront/global_logo_list.html')

pattern = re.compile(r'(\s*)(<i class="fa-brands fa-vogue[^>]+></i>\s*<i class="fa-brands fa-etsy[^>]+></i>\s*<i class="fa-brands fa-amazon[^>]+></i>\s*<i class="fa-brands fa-shopify[^>]+></i>\s*<i class="fa-brands fa-pinterest[^>]+></i>)')

for filepath in files:
    with open(filepath, 'r') as f:
        content = f.read()
    
    match = pattern.search(content)
    if match:
        indent = match.group(1)
        original_icons = match.group(2)
        
        replacement = f"""{indent}{{% if settings.logos %}}{indent}    {{% for logo in settings.logos %}}{indent}        {{% if logo.image_url %}}{indent}            <img src="{{{{ logo.image_url }}}}" alt="Brand Logo" class="h-12 md:h-16 w-auto object-contain hover:scale-110 transition-transform mix-blend-multiply">{indent}        {{% endif %}}{indent}    {{% endfor %}}{indent}{{% else %}}{indent}{original_icons}{indent}{{% endif %}}"""
        
        new_content = content.replace(match.group(0), replacement)
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"Pattern not found in {filepath}")
