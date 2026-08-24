from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.inventory.models import Location

class LocationListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Location
    template_name = 'admin/inventory/location/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'location_type', 'address']
    filter_fields = ['brand', 'location_type', 'is_active']

class LocationCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Location
    template_name = 'admin/inventory/location/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:location_list')

class LocationUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Location
    template_name = 'admin/inventory/location/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:location_list')
