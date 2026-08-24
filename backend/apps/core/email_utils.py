from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import GlobalSettings

def get_dynamic_email_backend():
    settings = GlobalSettings.get_settings()
    
    if settings.email_provider == 'resend':
        from anymail.backends.resend import EmailBackend as ResendBackend
        return ResendBackend(
            api_key=settings.resend_api_key,
            fail_silently=False,
        )
    elif settings.email_provider == 'sendgrid':
        from anymail.backends.sendgrid import EmailBackend as SendGridBackend
        return SendGridBackend(
            api_key=settings.sendgrid_api_key,
            fail_silently=False,
        )
    elif settings.email_provider == 'mailgun':
        from anymail.backends.mailgun import EmailBackend as MailgunBackend
        # We need domain from smtp_username
        domain = settings.smtp_username.split('@')[-1] if '@' in settings.smtp_username else settings.smtp_username
        return MailgunBackend(
            api_key=settings.mailgun_api_key,
            sender_domain=domain if domain else None,
            fail_silently=False,
        )
    elif settings.email_provider == 'ses':
        from anymail.backends.amazon_ses import EmailBackend as SESBackend
        import os
        
        # Configure boto3 environment securely for this request
        os.environ['AWS_ACCESS_KEY_ID'] = settings.ses_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = settings.ses_secret_access_key
        os.environ['AWS_DEFAULT_REGION'] = settings.ses_region
        
        return SESBackend(
            fail_silently=False,
        )
    else:
        # Standard SMTP
        if not settings.smtp_host:
            return None

        return EmailBackend(
            host=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password,
            use_tls=(settings.smtp_encryption == 'tls'),
            use_ssl=(settings.smtp_encryption == 'ssl'),
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
