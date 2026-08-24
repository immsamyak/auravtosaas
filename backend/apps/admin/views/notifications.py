from django.views.generic import ListView, CreateView
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
        
    from apps.core.email_utils import send_dynamic_email
    settings = GlobalSettings.get_settings()
    
    try:
        send_dynamic_email(
            subject=f"Aura Test - {settings.get_email_provider_display()}",
            template_name='emails/custom_campaign.html',
            context={'body_html': f'<p>This is a test of the <strong>{settings.email_provider.upper()}</strong> API integration via Django Anymail.</p>'},
            recipient_list=[request.user.email]
        )
        messages.success(request, f"Test email sent successfully to {request.user.email} using {settings.email_provider.upper()} API!")
    except Exception as e:
        messages.error(request, f"Failed to send test email: {str(e)}")
        
    return redirect('admin:notification_list')
