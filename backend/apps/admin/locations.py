from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.inventory.models import Location

class LocationListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = Location
    template_name = 'admin/inventory/location/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'location_type', 'address']
    filter_fields = ['brand', 'location_type', 'is_active']

class LocationCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Location
    template_name = 'admin/inventory/location/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:location_list')

class LocationUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Location
    template_name = 'admin/inventory/location/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:location_list')
