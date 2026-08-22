from django.views.generic import ListView
from apps.core.models import SystemAuditLog
from .mixins import SuperUserRequiredMixin

class AuditLogListView(SuperUserRequiredMixin, ListView):
    model = SystemAuditLog
    template_name = 'admin/audit/list.html'
    context_object_name = 'logs'
    paginate_by = 50
    
    def get_queryset(self):
        qs = super().get_queryset()
        action = self.request.GET.get('action')
        model_name = self.request.GET.get('model_name')
        
        if action:
            qs = qs.filter(action=action)
        if model_name:
            qs = qs.filter(model_name__icontains=model_name)
            
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'System Audit Logs'
        return context
