import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.apps import apps
from django.db import models

total_models = 0
total_fks = 0
total_m2m = 0
total_o2o = 0

for app_config in apps.get_app_configs():
    if app_config.name.startswith('django.') or app_config.name in ['rest_framework', 'corsheaders']:
        continue
        
    for model in app_config.get_models():
        total_models += 1
        for f in model._meta.get_fields():
            if isinstance(f, models.ForeignKey):
                total_fks += 1
            elif isinstance(f, models.ManyToManyField):
                total_m2m += 1
            elif isinstance(f, models.OneToOneField):
                total_o2o += 1

print(f"Models: {total_models}")
print(f"Foreign Keys (1:N): {total_fks}")
print(f"Many-to-Many (N:M): {total_m2m}")
print(f"One-to-One (1:1): {total_o2o}")
