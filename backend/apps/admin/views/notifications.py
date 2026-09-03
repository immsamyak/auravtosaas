from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.core.models import NotificationCampaign, GlobalSettings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib import messages
from django import forms
from django.utils import timezone

class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_superuser

class NotificationCampaignForm(forms.ModelForm):
    scheduled_for = forms.DateTimeField(
        required=False, 
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500 focus:border-indigo-500'}),
        help_text="Leave blank to send immediately"
    )
    
    class Meta:
        model = NotificationCampaign
        fields = ['subject', 'body_html', 'target_audience', 'specific_users', 'scheduled_for']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500 focus:border-indigo-500'}),
            'body_html': forms.Textarea(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500 focus:border-indigo-500', 'rows': 6}),
            'target_audience': forms.Select(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500 focus:border-indigo-500'}),
            'specific_users': forms.SelectMultiple(attrs={'class': 'w-full rounded-xl border-slate-200 focus:ring-indigo-500 focus:border-indigo-500 h-32'}),
        }

class NotificationCampaignListView(SuperAdminRequiredMixin, ListView):
    model = NotificationCampaign
    template_name = 'admin/core/notifications/list.html'
    context_object_name = 'campaigns'
    ordering = ['-created_at']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        settings = GlobalSettings.get_settings()
        context['provider'] = settings.get_email_provider_display()
        return context

class NotificationCampaignCreateView(SuperAdminRequiredMixin, CreateView):
    model = NotificationCampaign
    form_class = NotificationCampaignForm
    template_name = 'admin/core/notifications/form.html'
    success_url = reverse_lazy('admin:notification_list')
    
    def form_valid(self, form):
        campaign = form.save(commit=False)
        if form.cleaned_data.get('scheduled_for'):
            campaign.status = NotificationCampaign.Status.SCHEDULED
            messages.success(self.request, f"Campaign scheduled for {campaign.scheduled_for}")
        else:
            campaign.status = NotificationCampaign.Status.SCHEDULED
            campaign.scheduled_for = timezone.now()
            messages.success(self.request, "Campaign queued for immediate delivery!")
            
        campaign.save()
        form.save_m2m()
        return super().form_valid(form)

def test_email_api(request):
    if not request.user.is_superuser:
        return redirect('admin:login')
        
    from apps.core.email_utils import dispatch_async_email
    settings = GlobalSettings.get_settings()
    
    try:
        context = {
            'subject': f"Aura Test - {settings.get_email_provider_display()}",
            'campaign_content': f'<p>This is a test of the <strong>{settings.email_provider.upper()}</strong> API integration via the background queue.</p>',
            'body_html': f'<p>This is a test of the <strong>{settings.email_provider.upper()}</strong> API integration via the background queue.</p>'
        }
        
        # Route it through the queue system so it shows up in the logs
        dispatch_async_email('custom_campaign', context, [request.user.email])
        
        messages.success(request, f"Test email queued successfully for {request.user.email} using {settings.email_provider.upper()} API!")
    except Exception as e:
        messages.error(request, f"Failed to queue test email: {str(e)}")
        
    return redirect('admin:notification_list')


from apps.core.models import SystemEmailTemplate

class SystemEmailTemplateListView(SuperAdminRequiredMixin, ListView):
    model = SystemEmailTemplate
    template_name = 'admin/core/notifications/templates/list.html'
    context_object_name = 'templates'
    
    def get_queryset(self):
        # Ensure all types exist in the DB efficiently
        current_count = SystemEmailTemplate.objects.count()
        expected_count = len(SystemEmailTemplate.EventType.choices)
        
        if current_count < expected_count:
            from apps.core.template_seed_data import get_seed_data
            existing_events = set(SystemEmailTemplate.objects.values_list('event_type', flat=True))
            new_templates = []
            
            for evt, _ in SystemEmailTemplate.EventType.choices:
                if evt not in existing_events:
                    subject, body_html = get_seed_data(evt)
                    new_templates.append(SystemEmailTemplate(
                        event_type=evt,
                        subject=subject,
                        body_html=body_html
                    ))
            
            if new_templates:
                SystemEmailTemplate.objects.bulk_create(new_templates)
                
        return SystemEmailTemplate.objects.all().order_by('event_type')

class SystemEmailTemplateUpdateView(SuperAdminRequiredMixin, UpdateView):
    model = SystemEmailTemplate
    template_name = 'admin/core/notifications/templates/form.html'
    fields = ['subject', 'body_html', 'is_active']
    success_url = reverse_lazy('admin:notification_template_list')
    
    def form_valid(self, form):
        messages.success(self.request, f"Template for {self.object.get_event_type_display()} updated successfully.")
        return super().form_valid(form)
