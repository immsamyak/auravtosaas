from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import Size

class SizeListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Size
    template_name = 'admin/catalog/size/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'code']
    filter_fields = ['brand', 'is_active']

class SizeCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Size
    template_name = 'admin/catalog/size/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:size_list')

class SizeUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Size
    template_name = 'admin/catalog/size/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:size_list')
