from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.orders.models import DeliveryProvince

class DeliveryProvinceListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = DeliveryProvince
    template_name = 'admin/orders/deliveryprovince/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class DeliveryProvinceCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = DeliveryProvince
    template_name = 'admin/orders/deliveryprovince/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:deliveryprovince_list')

class DeliveryProvinceUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = DeliveryProvince
    template_name = 'admin/orders/deliveryprovince/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:deliveryprovince_list')
