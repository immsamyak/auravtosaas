from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.orders.models import ShippingZone

class ShippingZoneListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = ShippingZone
    template_name = 'admin/orders/shippingzone/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'estimated_days']
    filter_fields = ['brand', 'is_active']

class ShippingZoneCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = ShippingZone
    template_name = 'admin/orders/shippingzone/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:shippingzone_list')

class ShippingZoneUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ShippingZone
    template_name = 'admin/orders/shippingzone/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:shippingzone_list')
