from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import PlatformIntegration

class PlatformIntegrationListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = PlatformIntegration
    template_name = 'admin/core/platformintegration/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'provider_code', 'category', 'description']
    filter_fields = ['category', 'is_active_globally', 'requires_merchant_id', 'requires_api_key', 'requires_api_secret']

class PlatformIntegrationCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = PlatformIntegration
    template_name = 'admin/core/platformintegration/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:platformintegration_list')

class PlatformIntegrationUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = PlatformIntegration
    template_name = 'admin/core/platformintegration/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:platformintegration_list')
