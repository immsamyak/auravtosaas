from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.orders.models import Cart

class CartListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = Cart
    template_name = 'admin/orders/cart/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = []
    filter_fields = ['user']

class CartCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Cart
    template_name = 'admin/orders/cart/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:cart_list')

class CartUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Cart
    template_name = 'admin/orders/cart/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:cart_list')
