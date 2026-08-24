from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import SizeChart

class SizeChartListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = SizeChart
    template_name = 'admin/catalog/sizechart/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name']
    filter_fields = ['brand', 'product_type', 'is_active']

class SizeChartCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = SizeChart
    template_name = 'admin/catalog/sizechart/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:sizechart_list')

class SizeChartUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = SizeChart
    template_name = 'admin/catalog/sizechart/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:sizechart_list')
