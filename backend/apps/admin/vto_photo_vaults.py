from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.fitting.models import VTOPhotoVault

class VTOPhotoVaultListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = VTOPhotoVault
    template_name = 'admin/fitting/vtophotovault/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['pose_type']
    filter_fields = ['passport', 'pose_type', 'is_default']

class VTOPhotoVaultCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = VTOPhotoVault
    template_name = 'admin/fitting/vtophotovault/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:vtophotovault_list')

class VTOPhotoVaultUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = VTOPhotoVault
    template_name = 'admin/fitting/vtophotovault/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:vtophotovault_list')
