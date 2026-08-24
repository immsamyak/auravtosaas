from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import Product

class ProductListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Product
    template_name = 'admin/catalog/product/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'slug', 'description', 'occasion']
    filter_fields = ['brand', 'category', 'product_type', 'occasion', 'is_active', 'is_vto_ready']

class ProductCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Product
    template_name = 'admin/catalog/product/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:product_list')

class ProductUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Product
    template_name = 'admin/catalog/product/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:product_list')
