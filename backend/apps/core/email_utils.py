from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import GlobalSettings

def get_dynamic_email_backend():
    settings = GlobalSettings.get_settings()
    
    # If no host is set, return None so it falls back to console in development
    # But for a real system, we construct the backend
    if not settings.smtp_host:
        return None

    return EmailBackend(
        host=settings.smtp_host,
        port=settings.smtp_port,
        username=settings.smtp_username,
        password=settings.smtp_password,
        use_tls=True if settings.smtp_port == 587 else False,
        use_ssl=True if settings.smtp_port == 465 else False,
        fail_silently=False,
    )

def send_dynamic_email(subject, template_name, context, to_emails):
    settings = GlobalSettings.get_settings()
    from_email = f"{settings.site_name} <{settings.support_email}>"
    
    # Inject platform settings into email context
    context['platform_settings'] = settings
    
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    backend = get_dynamic_email_backend()
    
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails, connection=backend)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
