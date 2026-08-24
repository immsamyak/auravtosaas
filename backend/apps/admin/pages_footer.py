from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import Page

class PageListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Page
    template_name = 'admin/core/page/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['title', 'slug', 'content']
    filter_fields = ['is_published']

class PageCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Page
    template_name = 'admin/core/page/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:page_list')

class PageUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Page
    template_name = 'admin/core/page/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:page_list')
