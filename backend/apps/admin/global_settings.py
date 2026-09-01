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
            
            # Simple handling for SMTP provider testing
            if settings.email_provider != 'smtp':
                return JsonResponse({'success': False, 'error': 'Test email currently only supports the custom SMTP provider.'}, status=400)
                
            if not settings.smtp_host or not settings.smtp_port or not settings.smtp_username:
                return JsonResponse({'success': False, 'error': 'Incomplete SMTP settings in the database. Please save your settings first.'}, status=400)

            use_tls = settings.smtp_encryption == 'TLS'
            use_ssl = settings.smtp_encryption == 'SSL'

            backend = EmailBackend(
                host=settings.smtp_host,
                port=settings.smtp_port,
                username=settings.smtp_username,
                password=settings.smtp_password or "",
                use_tls=use_tls,
                use_ssl=use_ssl,
                fail_silently=False,
                timeout=10,
                ssl_keyfile="",
                ssl_certfile=""
            )
            
            from_email = settings.support_email or settings.smtp_username
            
            from django.template.loader import render_to_string
            html_message = render_to_string('emails/test_email.html', {
                'platform_settings': settings,
                'host': settings.smtp_host,
                'port': settings.smtp_port,
                'encryption': settings.smtp_encryption
            })
            
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
