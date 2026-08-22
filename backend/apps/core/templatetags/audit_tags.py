from django import template
from apps.core.models import SystemAuditLog

register = template.Library()

@register.simple_tag
def get_recent_audit_logs(limit=5):
    return SystemAuditLog.objects.all()[:limit]

@register.simple_tag
def get_unread_audit_count():
    # In a real app we might track 'last_read_at' per admin, 
    # but for now we just return the count of logs in the last 24h
    from django.utils import timezone
    from datetime import timedelta
    yesterday = timezone.now() - timedelta(days=1)
    return SystemAuditLog.objects.filter(created_at__gte=yesterday).count()
