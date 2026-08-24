from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import ProductType

class ProductTypeListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = ProductType
    template_name = 'admin/catalog/producttype/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'slug', 'description']
    filter_fields = ['brand', 'is_active']

class ProductTypeCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = ProductType
    template_name = 'admin/catalog/producttype/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:producttype_list')

class ProductTypeUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ProductType
    template_name = 'admin/catalog/producttype/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:producttype_list')
