from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.fitting.models import VTOProductAssets

class VTOProductAssetsListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = VTOProductAssets
    template_name = 'admin/fitting/vtoproductassets/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['asset_type']
    filter_fields = ['product_variant', 'asset_type', 'readiness_status']

class VTOProductAssetsCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = VTOProductAssets
    template_name = 'admin/fitting/vtoproductassets/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:vtoproductassets_list')

class VTOProductAssetsUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = VTOProductAssets
    template_name = 'admin/fitting/vtoproductassets/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:vtoproductassets_list')
