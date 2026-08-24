from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import Color

class ColorListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Color
    template_name = 'admin/catalog/color/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'slug', 'hex_code']
    filter_fields = ['brand', 'is_active']

class ColorCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Color
    template_name = 'admin/catalog/color/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:color_list')

class ColorUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Color
    template_name = 'admin/catalog/color/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:color_list')
