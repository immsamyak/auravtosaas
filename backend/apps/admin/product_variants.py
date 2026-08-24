from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import ProductVariant

class ProductVariantListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = ProductVariant
    template_name = 'admin/catalog/productvariant/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = []
    filter_fields = ['product', 'color', 'size']

class ProductVariantCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = ProductVariant
    template_name = 'admin/catalog/productvariant/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:productvariant_list')

class ProductVariantUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ProductVariant
    template_name = 'admin/catalog/productvariant/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:productvariant_list')
