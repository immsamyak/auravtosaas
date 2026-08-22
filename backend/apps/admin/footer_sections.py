from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import FooterSection

class FooterSectionListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = FooterSection
    template_name = 'admin/core/footersection/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['title']
    filter_fields = []

class FooterSectionCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = FooterSection
    template_name = 'admin/core/footersection/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:footersection_list')

class FooterSectionUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = FooterSection
    template_name = 'admin/core/footersection/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:footersection_list')
