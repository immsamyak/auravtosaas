from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import APIKey

class APIKeyListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = APIKey
    template_name = 'admin/brands/apikey/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class APIKeyCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = APIKey
    template_name = 'admin/brands/apikey/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:apikey_list')

class APIKeyUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = APIKey
    template_name = 'admin/brands/apikey/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:apikey_list')
