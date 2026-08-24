from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from apps.fitting.models import VTOSession

class VTOSessionListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = VTOSession
    template_name = 'admin/fitting/vtosession/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['status']
    filter_fields = ['passport']

class VTOSessionCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = VTOSession
    template_name = 'admin/fitting/vtosession/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:vtosession_list')

class VTOSessionDetailView(PlatformAdminRequiredMixin, DetailView):
    model = VTOSession
    template_name = 'admin/fitting/vtosession/detail.html'
    context_object_name = 'session'
