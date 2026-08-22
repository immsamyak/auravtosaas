import os

ADMIN_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/admin"

for root, dirs, files in os.walk(ADMIN_DIR):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
                
            new_content = content.replace("'custom_admin/", "'admin/")
            new_content = new_content.replace('"custom_admin/', '"admin/')
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated includes in {filepath}")

print("Template includes fixed.")
