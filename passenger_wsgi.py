import os
import sys

# Add the 'backend' directory to the Python path
cwd = os.getcwd()
backend_dir = os.path.join(cwd, 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

# Import the Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
