from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.catalog.models import Collection

class CollectionListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Collection
    template_name = 'admin/catalog/collection/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class CollectionCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Collection
    template_name = 'admin/catalog/collection/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:collection_list')

class CollectionUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Collection
    template_name = 'admin/catalog/collection/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:collection_list')
