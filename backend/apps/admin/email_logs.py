from django.views.generic import ListView
from apps.core.models import EmailLog
from .mixins import PlatformAdminRequiredMixin

class EmailLogListView(PlatformAdminRequiredMixin, ListView):
    model = EmailLog
    template_name = 'admin/email_logs/list.html'
    context_object_name = 'logs'
    paginate_by = 50
    
    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        
        if status:
            qs = qs.filter(status=status)
        if search:
            qs = qs.filter(recipient__icontains=search) | qs.filter(subject__icontains=search)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'System Email Logs'
        
        # Calculate stats
        context['total_emails'] = EmailLog.objects.count()
        context['total_pending'] = EmailLog.objects.filter(status='pending').count()
        context['total_sent'] = EmailLog.objects.filter(status='sent').count()
        context['total_failed'] = EmailLog.objects.filter(status='failed').count()
        
        return context
