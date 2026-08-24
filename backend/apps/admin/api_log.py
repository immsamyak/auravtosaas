from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import APILog

class APILogListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = APILog
    template_name = 'admin/brands/apilog/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class APILogCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = APILog
    template_name = 'admin/brands/apilog/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:apilog_list')

class APILogUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = APILog
    template_name = 'admin/brands/apilog/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:apilog_list')
