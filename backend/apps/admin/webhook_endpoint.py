from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import WebhookEndpoint

class WebhookEndpointListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = WebhookEndpoint
    template_name = 'admin/brands/webhookendpoint/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class WebhookEndpointCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = WebhookEndpoint
    template_name = 'admin/brands/webhookendpoint/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:webhookendpoint_list')

class WebhookEndpointUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = WebhookEndpoint
    template_name = 'admin/brands/webhookendpoint/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:webhookendpoint_list')
