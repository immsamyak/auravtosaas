from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.brands.models import StoreTheme

class StoreThemeListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = StoreTheme
    template_name = 'admin/brands/storetheme/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'business_type', 'description', 'template_folder']
    filter_fields = ['is_active']

class StoreThemeCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = StoreTheme
    template_name = 'admin/brands/storetheme/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:storetheme_list')

class StoreThemeUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = StoreTheme
    template_name = 'admin/brands/storetheme/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:storetheme_list')
