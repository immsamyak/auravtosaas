from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.fitting.models import VTOProduct

class VTOProductListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = VTOProduct
    template_name = 'admin/fitting/vtoproduct/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['product_type']
    filter_fields = ['try_on', 'product_variant', 'selected_size', 'product_type']

class VTOProductCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = VTOProduct
    template_name = 'admin/fitting/vtoproduct/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:vtoproduct_list')

class VTOProductUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = VTOProduct
    template_name = 'admin/fitting/vtoproduct/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:vtoproduct_list')
