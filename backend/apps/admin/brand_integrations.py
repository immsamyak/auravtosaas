from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.brands.models import BrandIntegration

class BrandIntegrationListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = BrandIntegration
    template_name = 'admin/brands/brandintegration/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = []
    filter_fields = ['brand', 'integration', 'is_active']

class BrandIntegrationCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = BrandIntegration
    template_name = 'admin/brands/brandintegration/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandintegration_list')

class BrandIntegrationUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = BrandIntegration
    template_name = 'admin/brands/brandintegration/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandintegration_list')
