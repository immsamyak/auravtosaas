import re

themes = [
    'theme_athletic',
    'theme_couture',
    'theme_cyberpunk',
    'theme_glass',
    'theme_goth',
    'theme_minimal',
    'theme_sneaker'
]

for theme in themes:
    header_path = f"templates/storefront/{theme}/sections/header.html"
    base_path = f"templates/storefront/{theme}/base.html"
    
    # 1. Update header.html
    with open(header_path, 'r') as f:
        header_content = f.read()
    
    # Replace 'fixed' with 'sticky' in the opening header tag
    # using regex to ensure we only target the class="... fixed ..." or class="fixed ..."
    header_content = re.sub(r'(<header[^>]*?class="[^"]*?)\bfixed\b', r'\1sticky', header_content)
    
    with open(header_path, 'w') as f:
        f.write(header_content)
        
    # 2. Update base.html
    with open(base_path, 'r') as f:
        base_content = f.read()
        
    # Replace `<main class="flex-grow pt-XX">` with `<main class="flex-grow">`
    base_content = re.sub(r'(<main[^>]*?class="[^"]*?)\bpt-\d+\b', r'\1', base_content)
    
    # Clean up any trailing spaces inside the class attribute that might have been left
    base_content = re.sub(r'(<main[^>]*?class="[^"]*?)\s+"', r'\1"', base_content)
    
    with open(base_path, 'w') as f:
        f.write(base_content)

print("Fixed headers and main padding for all 7 themes.")
