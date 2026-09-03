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

import sys

@receiver(post_save)
def audit_log_post_save(sender, instance, created, **kwargs):
    if len(sys.argv) > 1 and sys.argv[1] in ['migrate', 'makemigrations', 'flush', 'loaddata']:
        # Don't run audit logs during migrations or management commands
        return
        
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
    if len(sys.argv) > 1 and sys.argv[1] in ['migrate', 'makemigrations', 'flush', 'loaddata']:
        # Don't run audit logs during migrations or management commands
        return
        
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

from apps.core.models import ContactMessage
from apps.brands.models import NewsletterSubscriber
from apps.core.email_utils import send_dynamic_email
from apps.core.models import GlobalSettings
import threading

def send_async_email(subject, template_name, context, to_emails):
    from apps.core.models import EmailLog
    from django.utils import timezone
    
    def send():
        for recipient in to_emails:
            email_log = EmailLog.objects.create(
                recipient=recipient,
                subject=subject,
                template_type='Automated Reply',
                status=EmailLog.Status.PENDING
            )
            try:
                send_dynamic_email(subject, template_name, context, [recipient])
                email_log.status = EmailLog.Status.SENT
                email_log.sent_at = timezone.now()
                email_log.save()
            except Exception as e:
                print(f"Error sending automated email: {e}")
                email_log.status = EmailLog.Status.FAILED
                email_log.error_message = str(e)
                email_log.save()

    threading.Thread(target=send, daemon=True).start()

@receiver(post_save, sender=ContactMessage)
def contact_message_email_handler(sender, instance, created, **kwargs):
    if created:
        settings = GlobalSettings.get_settings()
        admin_email = settings.support_email
        
        # 1. Auto-reply to customer
        send_async_email(
            subject=f"We received your message - {settings.site_name}",
            template_name="emails/custom_campaign.html",
            context={
                "body_html": f"<p>Hi {instance.name},</p><p>Thank you for reaching out to us. We have received your message and our team will get back to you shortly.</p><p>Best,<br>The {settings.site_name} Team</p>"
            },
            to_emails=[instance.email]
        )
        
        # 2. Notification to Admin/Brand Owner
        if admin_email:
            send_async_email(
                subject=f"New Contact Support Request from {instance.name}",
                template_name="emails/custom_campaign.html",
                context={
                    "body_html": f"<h3>New Support Request Received</h3><p><strong>From:</strong> {instance.name} ({instance.email})</p><p><strong>Message:</strong><br>{instance.message}</p>"
                },
                to_emails=[admin_email]
            )

@receiver(post_save, sender=NewsletterSubscriber)
def newsletter_subscriber_email_handler(sender, instance, created, **kwargs):
    if created:
        settings = GlobalSettings.get_settings()
        brand = instance.brand
        brand_email = brand.contact_email or (brand.owner.email if brand.owner else None)
        
        # 1. Welcome to Newsletter subscriber
        send_async_email(
            subject=f"Welcome to {brand.name} Newsletter!",
            template_name="emails/custom_campaign.html", 
            context={
                "user": {"first_name": "Subscriber"},
                "body_html": f"<h2>Welcome! 🎉</h2><p>Thank you for subscribing to the <strong>{brand.name}</strong> newsletter! You'll now receive the latest updates directly to your inbox.</p>"
            },
            to_emails=[instance.email]
        )
        
        # 2. Notification to Admin/Brand Owner
        if brand_email:
            send_async_email(
                subject=f"New Newsletter Subscriber for {brand.name}!",
                template_name="emails/custom_campaign.html",
                context={
                    "body_html": f"<p>Good news! <strong>{instance.email}</strong> has just subscribed to your brand's newsletter.</p>"
                },
                to_emails=[brand_email]
            )

from apps.brands.models import BrandContactMessage

@receiver(post_save, sender=BrandContactMessage)
def brand_contact_message_email_handler(sender, instance, created, **kwargs):
    if created:
        settings = GlobalSettings.get_settings()
        brand = instance.brand
        brand_email = brand.contact_email or (brand.owner.email if brand.owner else None)
        
        # 1. Auto-reply to customer
        send_async_email(
            subject=f"We received your message - {brand.name}",
            template_name="emails/custom_campaign.html",
            context={
                "body_html": f"<p>Hi {instance.name},</p><p>Thank you for reaching out to <strong>{brand.name}</strong>. We have received your message and our team will get back to you shortly.</p><p>Best,<br>The {brand.name} Team</p>"
            },
            to_emails=[instance.email]
        )
        
        # 2. Notification to Brand Owner
        if brand_email:
            send_async_email(
                subject=f"New Customer Message for {brand.name} from {instance.name}",
                template_name="emails/custom_campaign.html",
                context={
                    "body_html": f"<h3>New Support Request Received</h3><p><strong>From:</strong> {instance.name} ({instance.email})</p><p><strong>Message:</strong><br>{instance.message}</p>"
                },
                to_emails=[brand_email]
            )
