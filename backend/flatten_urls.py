import re

URLS_PATH = "/Users/saamyak/COllege Project/Aura/backend/apps/admin/urls.py"

with open(URLS_PATH, 'r') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    match = re.search(r"path\('([^']*)',", line)
    if match:
        route = match.group(1)
        # Skip top level routes or already flattened ones
        if route in ['', 'login/', 'logout/', 'orders/', 'orders/add/', 'orders/<str:pk>/', 
                     'brands/', 'brands/add/', 'brands/<str:pk>/', 
                     'users/', 'users/add/', 'users/<str:pk>/', 
                     'roles/', 'roles/add/', 'roles/<str:pk>/']:
            new_lines.append(line)
            continue
            
        parts = route.split('/')
        # parts usually looks like ['core', 'systemsetting', '']
        if len(parts) >= 3:
            # Remove the app prefix (the first part)
            new_route = '/'.join(parts[1:])
            line = line.replace(f"path('{route}',", f"path('{new_route}',")
            
    new_lines.append(line)

with open(URLS_PATH, 'w') as f:
    f.writelines(new_lines)

print("URLs flattened to a single slug.")
