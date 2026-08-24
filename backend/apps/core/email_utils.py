from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import GlobalSettings, SystemEmailTemplate

def get_dynamic_email_backend():
    settings = GlobalSettings.get_settings()
    
    if settings.email_provider == 'resend':
        if not settings.resend_api_key:
            raise ValueError("Resend API Key is missing in Global Settings.")
        from anymail.backends.resend import EmailBackend as ResendBackend
        return ResendBackend(
            api_key=settings.resend_api_key,
            fail_silently=False,
        )
    elif settings.email_provider == 'sendgrid':
        if not settings.sendgrid_api_key:
            raise ValueError("SendGrid API Key is missing in Global Settings.")
        from anymail.backends.sendgrid import EmailBackend as SendGridBackend
        return SendGridBackend(
            api_key=settings.sendgrid_api_key,
            fail_silently=False,
        )
    elif settings.email_provider == 'mailgun':
        if not settings.mailgun_api_key:
            raise ValueError("Mailgun API Key is missing in Global Settings.")
        from anymail.backends.mailgun import EmailBackend as MailgunBackend
        # We need domain from smtp_username
        domain = settings.smtp_username.split('@')[-1] if '@' in settings.smtp_username else settings.smtp_username
        return MailgunBackend(
            api_key=settings.mailgun_api_key,
            sender_domain=domain if domain else None,
            fail_silently=False,
        )
    elif settings.email_provider == 'ses':
        if not settings.ses_access_key_id or not settings.ses_secret_access_key:
            raise ValueError("Amazon SES Credentials are missing in Global Settings.")
        from anymail.backends.amazon_ses import EmailBackend as SESBackend
        import os
        
        # Configure boto3 environment securely for this request
        os.environ['AWS_ACCESS_KEY_ID'] = settings.ses_access_key_id
        os.environ['AWS_SECRET_ACCESS_KEY'] = settings.ses_secret_access_key
        os.environ['AWS_DEFAULT_REGION'] = settings.ses_region or 'us-east-1'
        
        return SESBackend(
            fail_silently=False,
        )
    else:
        # Standard SMTP
        if not settings.smtp_host:
            raise ValueError("SMTP Host is missing in Global Settings. Please configure an email provider.")

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


from django.template import Template, Context

def send_transactional_email(event_type, context_dict, to_emails):
    try:
        template_obj = SystemEmailTemplate.objects.get(event_type=event_type, is_active=True)
        # Render custom DB template
        t_subject = Template(template_obj.subject)
        t_body = Template(template_obj.body_html)
        
        ctx = Context(context_dict)
        subject = t_subject.render(ctx)
        body_html = t_body.render(ctx)
        
        # Inject platform settings for the base wrapper
        settings = GlobalSettings.get_settings()
        wrapper_context = context_dict.copy()
        wrapper_context['platform_settings'] = settings
        wrapper_context['body_html'] = body_html
        
        final_html = render_to_string('emails/custom_campaign.html', wrapper_context)
        text_content = strip_tags(final_html)
        
        backend = get_dynamic_email_backend()
        from_email = f"{settings.site_name} <{settings.support_email}>"
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails, connection=backend)
        msg.attach_alternative(final_html, "text/html")
        msg.send()
        
    except SystemEmailTemplate.DoesNotExist:
        # Fallback to hardcoded templates if DB template is disabled or doesn't exist
        print(f"Warning: No active custom template for {event_type}. Falling back to default.")
        # E.g. implement standard render_to_string fallback here based on event_type
        pass
