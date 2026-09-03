from django.core.mail import EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import GlobalSettings, SystemEmailTemplate

def get_dynamic_email_backend():
    settings = GlobalSettings.get_settings()
    
    if settings.email_provider == 'resend':
        # Handled natively in the send_ functions to enforce the Python SDK
        return None
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
            password=settings.smtp_password or "",
            use_tls=(settings.smtp_encryption == 'tls' or settings.smtp_encryption == 'TLS'),
            use_ssl=(settings.smtp_encryption == 'ssl' or settings.smtp_encryption == 'SSL'),
            fail_silently=False,
            timeout=10,
            ssl_keyfile="",
            ssl_certfile=""
        )

def send_dynamic_email(subject, template_name, context, to_emails):
    settings = GlobalSettings.get_settings()
    
    raw_sender = settings.email_sender_address or settings.support_email or settings.smtp_username
    from_email = f'{settings.site_name} <{raw_sender}>' if raw_sender and '<' not in raw_sender else raw_sender
    
    # Inject platform settings into email context
    context['platform_settings'] = settings
    
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    if settings.email_provider == 'resend':
        import os
        import resend
        os.environ["RESEND_API_KEY"] = settings.resend_api_key
        resend.api_key = os.environ["RESEND_API_KEY"]
        
        params: resend.Emails.SendParams = {
            "from": from_email,
            "to": to_emails if isinstance(to_emails, list) else [to_emails],
            "subject": subject,
            "html": html_content,
        }
        resend.Emails.send(params)
    else:
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
        
        raw_sender = settings.email_sender_address or settings.support_email or settings.smtp_username
        from_email = f'{settings.site_name} <{raw_sender}>' if raw_sender and '<' not in raw_sender else raw_sender
        
        if settings.email_provider == 'resend':
            import os
            import resend
            os.environ["RESEND_API_KEY"] = settings.resend_api_key
            resend.api_key = os.environ["RESEND_API_KEY"]
            
            params: resend.Emails.SendParams = {
                "from": from_email,
                "to": to_emails if isinstance(to_emails, list) else [to_emails],
                "subject": subject,
                "html": final_html,
            }
            resend.Emails.send(params)
        else:
            backend = get_dynamic_email_backend()
            msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails, connection=backend)
            msg.attach_alternative(final_html, "text/html")
            msg.send()
        return subject
        
    except SystemEmailTemplate.DoesNotExist:
        # Fallback to hardcoded templates if DB template is disabled or doesn't exist
        print(f"Warning: No active custom template for {event_type}. Falling back to default.")
        # E.g. implement standard render_to_string fallback here based on event_type
        return False
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def dispatch_async_email(event_type, context, to_emails, brand=None):
    """
    Fire-and-forget email dispatcher using Celery (or sync fallback).
    """
    if brand:
        context['brand_name'] = brand.name
        if brand.logo:
            context['brand_logo'] = brand.logo.url
    
    try:
        from apps.core.tasks import send_email_async
        send_email_async.delay(event_type, context, to_emails)
    except (ImportError, Exception):
        # Fallback to synchronous if celery is not configured or fails
        try:
            from django.utils import timezone
            from apps.core.models import EmailLog
            
            for recipient in to_emails:
                email_log = EmailLog.objects.create(
                    recipient=recipient,
                    subject=f"Processing {event_type}...",
                    template_type=event_type,
                    status=EmailLog.Status.PENDING
                )
                success = send_transactional_email(event_type, context, [recipient])
                if success:
                    email_log.status = EmailLog.Status.SENT
                    email_log.sent_at = timezone.now()
                    if isinstance(success, str):
                        email_log.subject = success
                    else:
                        email_log.subject = f"Sent {event_type} to {recipient}"
                    email_log.save()
                else:
                    email_log.status = EmailLog.Status.FAILED
                    email_log.error_message = "Email backend failed to send."
                    email_log.save()
        except Exception as e:
            print(f"Failed to send email synchronously: {e}")


