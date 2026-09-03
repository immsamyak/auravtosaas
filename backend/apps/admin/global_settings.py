from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin

from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.core.models import GlobalSettings

class GlobalSettingsUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = GlobalSettings
    template_name = 'admin/core/globalsettings/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:globalsettings_edit')

    def get_object(self, queryset=None):
        return GlobalSettings.get_settings()
        
    def form_valid(self, form):
        messages.success(self.request, "Global settings updated successfully.")
        return super().form_valid(form)

from django.http import JsonResponse
from django.views import View
import json
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import send_mail

class TestEmailView(PlatformAdminRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            email = data.get('email')
            if not email:
                return JsonResponse({'success': False, 'error': 'Email address is required.'}, status=400)
                
            settings = GlobalSettings.get_settings()
            
            from_email = settings.support_email or settings.smtp_username or "onboarding@resend.dev"
            
            from django.template.loader import render_to_string
            html_message = render_to_string('emails/test_email.html', {
                'platform_settings': settings,
                'host': settings.smtp_host,
                'port': settings.smtp_port,
                'encryption': settings.smtp_encryption
            })

            if settings.email_provider == 'resend':
                if not settings.resend_api_key:
                    return JsonResponse({'success': False, 'error': 'Resend API Key is missing. Please save your settings first.'}, status=400)
                try:
                    import os
                    import resend
                    from resend.exceptions import ResendError
                    
                    # 1. Set environment variable & api_key as required by SDK docs
                    os.environ["RESEND_API_KEY"] = settings.resend_api_key
                    resend.api_key = os.environ["RESEND_API_KEY"]
                    
                    # 2. Use snake_case params inside resend.Emails.SendParams
                    params: resend.Emails.SendParams = {
                        "from": from_email,
                        "to": [email],
                        "subject": f'Test Email from {settings.site_name or "Aura"}',
                        "html": html_message,
                    }
                    
                    # 3. Call the SDK, which raises an exception on failure
                    resend.Emails.send(params)
                    return JsonResponse({'success': True})
                except ImportError:
                    return JsonResponse({'success': False, 'error': 'resend Python SDK is not installed. Run: pip install resend'}, status=500)
                except Exception as error:
                    # 4. Catch ResendError (or catch-all Exception)
                    return JsonResponse({'success': False, 'error': str(error)}, status=500)

            backend = None
            
            if settings.email_provider == 'smtp':
                if not settings.smtp_host or not settings.smtp_port or not settings.smtp_username:
                    return JsonResponse({'success': False, 'error': 'Incomplete SMTP settings in the database. Please save your settings first.'}, status=400)

                use_tls = settings.smtp_encryption == 'tls'
                use_ssl = settings.smtp_encryption == 'ssl'

                from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
                backend = SMTPEmailBackend(
                    host=settings.smtp_host,
                    port=settings.smtp_port,
                    username=settings.smtp_username,
                    password=settings.smtp_password or "",
                    use_tls=use_tls,
                    use_ssl=use_ssl,
                    fail_silently=False,
                    timeout=10,
                )
                
            elif settings.email_provider == 'sendgrid':
                if not settings.sendgrid_api_key:
                    return JsonResponse({'success': False, 'error': 'SendGrid API Key is missing. Please save your settings first.'}, status=400)
                from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
                backend = SMTPEmailBackend(
                    host='smtp.sendgrid.net',
                    port=587,
                    username='apikey',
                    password=settings.sendgrid_api_key,
                    use_tls=True,
                    fail_silently=False,
                    timeout=10,
                )
                
            elif settings.email_provider == 'mailgun':
                if not settings.mailgun_api_key:
                    return JsonResponse({'success': False, 'error': 'Mailgun API Key is missing. Please save your settings first.'}, status=400)
                try:
                    from anymail.backends.mailgun import EmailBackend as MailgunBackend
                    backend = MailgunBackend(api_key=settings.mailgun_api_key)
                except ImportError:
                    return JsonResponse({'success': False, 'error': 'django-anymail is not installed. Please install it to use Mailgun.'}, status=500)
                    
            elif settings.email_provider == 'ses':
                if not settings.ses_access_key_id or not settings.ses_secret_access_key:
                    return JsonResponse({'success': False, 'error': 'Amazon SES credentials are missing. Please save your settings first.'}, status=400)
                from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend
                region = settings.ses_region or 'us-east-1'
                backend = SMTPEmailBackend(
                    host=f'email-smtp.{region}.amazonaws.com',
                    port=587,
                    username=settings.ses_access_key_id,
                    password=settings.ses_secret_access_key,
                    use_tls=True,
                    fail_silently=False,
                    timeout=10,
                )
            else:
                return JsonResponse({'success': False, 'error': 'Unsupported email provider selected.'}, status=400)
            
            send_mail(
                subject=f'Test Email from {settings.site_name or "Aura"}',
                message=f'This is a test email to verify your SMTP settings are working correctly.\n\nSettings used:\nHost: {settings.smtp_host}\nPort: {settings.smtp_port}',
                from_email=from_email,
                recipient_list=[email],
                connection=backend,
                html_message=html_message
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print("TEST EMAIL ERROR:", error_details)
            return JsonResponse({'success': False, 'error': str(e), 'traceback': error_details}, status=500)
