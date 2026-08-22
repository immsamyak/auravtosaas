import os

ADMIN_TEMPLATES_DIR = "/Users/saamyak/COllege Project/Aura/backend/templates/admin"

for root, dirs, files in os.walk(ADMIN_TEMPLATES_DIR):
    for file in files:
        if file == 'form.html':
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            new_content = content.replace('class="max-w-3xl mx-auto"', 'class="max-w-7xl mx-auto"')
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Expanded layout in {filepath}")

print("All form.html templates have been expanded.")
