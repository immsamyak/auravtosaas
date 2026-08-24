from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import FeatureFlag

class FeatureFlagListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = FeatureFlag
    template_name = 'admin/core/featureflag/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name']
    filter_fields = ['is_active']

class FeatureFlagCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = FeatureFlag
    template_name = 'admin/core/featureflag/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:featureflag_list')

class FeatureFlagUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = FeatureFlag
    template_name = 'admin/core/featureflag/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:featureflag_list')
