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
                password=settings.smtp_password,
                use_tls=use_tls,
                use_ssl=use_ssl,
                fail_silently=False
            )
            
            from_email = settings.support_email or settings.smtp_username
            
            send_mail(
                subject='Test Email from Aura Platform',
                message='This is a test email to verify your SMTP settings are working correctly.\n\nSettings used:\nHost: {}\nPort: {}'.format(settings.smtp_host, settings.smtp_port),
                from_email=from_email,
                recipient_list=[email],
                connection=backend
            )
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
