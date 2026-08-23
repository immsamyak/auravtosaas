from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from apps.fitting.models import VirtualTryOn

class VirtualTryOnListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = VirtualTryOn
    template_name = 'admin/fitting/virtualtryon/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['status', 'provider', 'error_message']
    filter_fields = ['session', 'base_photo', 'product_variant', 'selected_size', 'status', 'provider']

class VirtualTryOnCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = VirtualTryOn
    template_name = 'admin/fitting/virtualtryon/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:virtualtryon_list')

class VirtualTryOnDetailView(SuperUserRequiredMixin, DetailView):
    model = VirtualTryOn
    template_name = 'admin/fitting/virtualtryon/detail.html'
    context_object_name = 'job'
