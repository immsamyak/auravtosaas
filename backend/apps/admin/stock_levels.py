from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.inventory.models import StockLevel

class StockLevelListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = StockLevel
    template_name = 'admin/inventory/stocklevel/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = []
    filter_fields = ['location', 'product_variant']

class StockLevelCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = StockLevel
    template_name = 'admin/inventory/stocklevel/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:stocklevel_list')

class StockLevelUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = StockLevel
    template_name = 'admin/inventory/stocklevel/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:stocklevel_list')
