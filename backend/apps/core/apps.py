from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'apps.core'

    def ready(self):
        # Register signals
        import apps.core.signals
        
        # Start background scheduler
        import os
        import sys
        
        # Prevent scheduler from running multiple times in dev server or during migrations
        if os.environ.get('RUN_MAIN', None) == 'true' or not sys.argv or sys.argv[0].endswith('manage.py') and len(sys.argv) == 1:
            from . import scheduler
            scheduler.start()
