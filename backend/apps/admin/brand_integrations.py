from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.brands.models import BrandIntegration

class BrandIntegrationListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = BrandIntegration
    template_name = 'admin/brands/brandintegration/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = []
    filter_fields = ['brand', 'integration', 'is_active']

class BrandIntegrationCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = BrandIntegration
    template_name = 'admin/brands/brandintegration/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandintegration_list')

class BrandIntegrationUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = BrandIntegration
    template_name = 'admin/brands/brandintegration/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandintegration_list')
