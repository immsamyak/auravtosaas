from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.orders.models import DeliveryDistrict

class DeliveryDistrictListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = DeliveryDistrict
    template_name = 'admin/orders/deliverydistrict/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class DeliveryDistrictCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = DeliveryDistrict
    template_name = 'admin/orders/deliverydistrict/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:deliverydistrict_list')

class DeliveryDistrictUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = DeliveryDistrict
    template_name = 'admin/orders/deliverydistrict/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:deliverydistrict_list')
