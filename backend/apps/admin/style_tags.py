from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.catalog.models import StyleTag

class StyleTagListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = StyleTag
    template_name = 'admin/catalog/styletag/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'slug']
    filter_fields = ['is_active']

class StyleTagCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = StyleTag
    template_name = 'admin/catalog/styletag/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:styletag_list')

class StyleTagUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = StyleTag
    template_name = 'admin/catalog/styletag/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:styletag_list')
