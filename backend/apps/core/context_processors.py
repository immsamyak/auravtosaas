from .models import FooterSection

def footer_data(request):
    try:
        sections = FooterSection.objects.prefetch_related('links__page').all()
        return {'footer_sections': sections}
    except Exception:
        return {'footer_sections': []}

from .models import GlobalSettings

def global_settings(request):
    try:
        settings = GlobalSettings.get_settings()
        return {'platform_settings': settings}
    except Exception:
        return {}

from .models import Notification, FeatureFlag

def user_notifications(request):
    if request.user.is_authenticated:
        try:
            notifications = Notification.objects.filter(user=request.user)
            return {
                'unread_notifications': notifications.filter(is_read=False)[:5],
                'unread_notifications_count': notifications.filter(is_read=False).count(),
            }
        except Exception:
            return {}
    return {}

def feature_flags(request):
    try:
        flags = FeatureFlag.objects.all()
        # Return a dictionary like {'virtual_try_on': True, 'new_checkout': False}
        return {'feature_flags': {flag.name: flag.is_active for flag in flags}}
    except Exception:
        return {'feature_flags': {}}
