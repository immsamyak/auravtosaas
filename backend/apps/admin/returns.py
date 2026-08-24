from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.orders.models import ReturnRequest

class ReturnRequestListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = ReturnRequest
    template_name = 'admin/orders/returnrequest/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['order__id', 'reason', 'status']
    filter_fields = ['status']

class ReturnRequestUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ReturnRequest
    template_name = 'admin/orders/returnrequest/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:returnrequest_list')
