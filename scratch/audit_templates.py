import os
import django
import sys

sys.path.append(os.path.join(os.getcwd(), 'backend'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()

from apps.core.models import SystemEmailTemplate

templates = SystemEmailTemplate.objects.all().order_by('event_type')
for t in templates:
    print(f"- {t.event_type} - {t.name}")
