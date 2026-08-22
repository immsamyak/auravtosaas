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

from .models import Notification

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
