from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import LandingPageFeature

class LandingPageFeatureListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = LandingPageFeature
    template_name = 'admin/core/landingpagefeature/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['title', 'description']
    filter_fields = ['audience']

class LandingPageFeatureCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = LandingPageFeature
    template_name = 'admin/core/landingpagefeature/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:landingpagefeature_list')

    def get_initial(self):
        initial = super().get_initial()
        from apps.core.models import LandingPageConfig
        config = LandingPageConfig.objects.first()
        if config:
            initial['config'] = config.pk
        return initial

class LandingPageFeatureUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = LandingPageFeature
    template_name = 'admin/core/landingpagefeature/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:landingpagefeature_list')

class LandingPageFeatureDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = LandingPageFeature
    template_name = 'admin/core/landingpagefeature/delete.html'
    success_url = reverse_lazy('admin:landingpagefeature_list')
