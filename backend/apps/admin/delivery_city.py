from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.orders.models import DeliveryCity

class DeliveryCityListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = DeliveryCity
    template_name = 'admin/orders/deliverycity/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class DeliveryCityCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = DeliveryCity
    template_name = 'admin/orders/deliverycity/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:deliverycity_list')

class DeliveryCityUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = DeliveryCity
    template_name = 'admin/orders/deliverycity/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:deliverycity_list')
