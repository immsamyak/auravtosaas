from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import ProductAIProfile

class ProductAIProfileListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = ProductAIProfile
    template_name = 'admin/catalog/productaiprofile/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['item_type', 'fit_type', 'material', 'processing_status']
    filter_fields = ['product_variant', 'processing_status']

class ProductAIProfileCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = ProductAIProfile
    template_name = 'admin/catalog/productaiprofile/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:productaiprofile_list')

class ProductAIProfileUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ProductAIProfile
    template_name = 'admin/catalog/productaiprofile/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:productaiprofile_list')
