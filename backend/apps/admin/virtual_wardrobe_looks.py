from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.fitting.models import VirtualWardrobeLook

class VirtualWardrobeLookListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = VirtualWardrobeLook
    template_name = 'admin/fitting/virtualwardrobelook/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['notes']
    filter_fields = ['user', 'try_on']

class VirtualWardrobeLookCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = VirtualWardrobeLook
    template_name = 'admin/fitting/virtualwardrobelook/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:virtualwardrobelook_list')

class VirtualWardrobeLookUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = VirtualWardrobeLook
    template_name = 'admin/fitting/virtualwardrobelook/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:virtualwardrobelook_list')
