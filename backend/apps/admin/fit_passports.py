from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.fitting.models import FitPassport

class FitPassportListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = FitPassport
    template_name = 'admin/fitting/fitpassport/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['session_key', 'body_shape', 'fit_preference', 'gender_preference']
    filter_fields = ['user', 'body_shape', 'fit_preference', 'gender_preference']

class FitPassportCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = FitPassport
    template_name = 'admin/fitting/fitpassport/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:fitpassport_list')

class FitPassportUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = FitPassport
    template_name = 'admin/fitting/fitpassport/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:fitpassport_list')
