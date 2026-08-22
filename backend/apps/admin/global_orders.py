from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.orders.models import Order

class OrderListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = Order
    template_name = 'admin/orders/order/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['status', 'payment_provider', 'payment_reference_id', 'shipping_provider', 'tracking_number', 'customer_name', 'customer_phone', 'shipping_address']
    filter_fields = ['user', 'brand', 'status', 'shipping_zone']

class OrderCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Order
    template_name = 'admin/orders/order/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:order_list')

class OrderUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Order
    template_name = 'admin/orders/order/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:order_list')
