from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import Category

class CategoryListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Category
    template_name = 'admin/catalog/category/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'slug', 'description']
    filter_fields = ['brand', 'parent', 'is_active']

class CategoryCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Category
    template_name = 'admin/catalog/category/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:category_list')

class CategoryUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Category
    template_name = 'admin/catalog/category/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:category_list')
