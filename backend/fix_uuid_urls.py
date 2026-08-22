import os

URLS_PATH = "/Users/saamyak/COllege Project/Aura/backend/apps/admin/urls.py"

with open(URLS_PATH, 'r') as f:
    content = f.read()

# Replace <int:pk> with <str:pk> to support both UUID and AutoField primary keys
content = content.replace("<int:pk>", "<str:pk>")

with open(URLS_PATH, 'w') as f:
    f.write(content)

print("URLs updated to support UUID and string primary keys.")
