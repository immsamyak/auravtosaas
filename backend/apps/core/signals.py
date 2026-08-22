from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
import json
from .models import SystemAuditLog
from .middleware import get_current_user, get_current_request, get_client_ip

# Models to explicitly ignore to prevent spam
IGNORE_MODELS = ['systemauditlog', 'session', 'logentry', 'contenttype', 'notification']

def _get_model_name(sender):
    try:
        return ContentType.objects.get_for_model(sender).model
    except Exception:
        return sender.__name__.lower()

@receiver(post_save)
def audit_log_post_save(sender, instance, created, **kwargs):
    model_name = _get_model_name(sender)
    
    if model_name in IGNORE_MODELS:
        return
        
    action = 'CREATE' if created else 'UPDATE'
    
    request = get_current_request()
    actor = get_current_user()
    
    # Optional: Check if we are inside a request. If not, it's a background task.
    ip = get_client_ip(request) if request else '127.0.0.1'
    ua = request.META.get('HTTP_USER_AGENT', 'Background/CLI') if request else 'Background/CLI'
    
    try:
        # Avoid recursion or errors if the DB is in a bad state
        SystemAuditLog.objects.create(
            actor=actor if actor and actor.is_authenticated else None,
            action=action,
            model_name=model_name,
            object_id=str(instance.pk),
            object_repr=str(instance)[:250],
            ip_address=ip,
            user_agent=ua,
            payload={"created": created}
        )
    except Exception as e:
        # Silently ignore audit log failures to not break core app flow
        pass

@receiver(post_delete)
def audit_log_post_delete(sender, instance, **kwargs):
    model_name = _get_model_name(sender)
    
    if model_name in IGNORE_MODELS:
        return
        
    request = get_current_request()
    actor = get_current_user()
    
    ip = get_client_ip(request) if request else '127.0.0.1'
    ua = request.META.get('HTTP_USER_AGENT', 'Background/CLI') if request else 'Background/CLI'
    
    try:
        SystemAuditLog.objects.create(
            actor=actor if actor and actor.is_authenticated else None,
            action='DELETE',
            model_name=model_name,
            object_id=str(instance.pk),
            object_repr=str(instance)[:250],
            ip_address=ip,
            user_agent=ua,
            payload={}
        )
    except Exception as e:
        pass
