import os
import django
from django.template import Engine
from django.template.exceptions import TemplateSyntaxError
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aura_project.settings")
django.setup()

engine = Engine.get_default()
error_count = 0

for root, dirs, files in os.walk("backend/templates"):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            try:
                engine.from_string(content)
            except TemplateSyntaxError as e:
                print(f"Error in {path}: {e}")
                error_count += 1

for root, dirs, files in os.walk("backend/apps"):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, "r") as f:
                content = f.read()
            try:
                engine.from_string(content)
            except TemplateSyntaxError as e:
                print(f"Error in {path}: {e}")
                error_count += 1

if error_count == 0:
    print("All templates syntax valid!")
else:
    print(f"Found {error_count} template errors.")
