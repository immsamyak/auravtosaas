from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.accounts.models import ConsumerProfile

class ConsumerProfileListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = ConsumerProfile
    template_name = 'admin/accounts/consumerprofile/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['phone_number', 'skin_tone_category']
    filter_fields = ['user']

class ConsumerProfileCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = ConsumerProfile
    template_name = 'admin/accounts/consumerprofile/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:consumerprofile_list')

class ConsumerProfileUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ConsumerProfile
    template_name = 'admin/accounts/consumerprofile/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:consumerprofile_list')
