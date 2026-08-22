import re

URLS_PATH = "/Users/saamyak/COllege Project/Aura/backend/apps/admin/urls.py"

with open(URLS_PATH, 'r') as f:
    content = f.read()

# Replace orders/order/ with orders/
content = content.replace("path('orders/order/',", "path('orders/',")
content = content.replace("path('orders/order/add/',", "path('orders/add/',")
content = content.replace("path('orders/order/<str:pk>/',", "path('orders/<str:pk>/',")

# Replace brands/brand/ with brands/
content = content.replace("path('brands/brand/',", "path('brands/',")
content = content.replace("path('brands/brand/add/',", "path('brands/add/',")
content = content.replace("path('brands/brand/<str:pk>/',", "path('brands/<str:pk>/',")

# Replace auth/user/ with users/
content = content.replace("path('auth/user/',", "path('users/',")
content = content.replace("path('auth/user/add/',", "path('users/add/',")
content = content.replace("path('auth/user/<str:pk>/',", "path('users/<str:pk>/',")

# Replace auth/group/ with roles/
content = content.replace("path('auth/group/',", "path('roles/',")
content = content.replace("path('auth/group/add/',", "path('roles/add/',")
content = content.replace("path('auth/group/<str:pk>/',", "path('roles/<str:pk>/',")

with open(URLS_PATH, 'w') as f:
    f.write(content)

print("Redundant URLs cleaned up.")
