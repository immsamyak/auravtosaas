from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import LandingPageConfig

from django.contrib import messages

class LandingPageConfigUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = LandingPageConfig
    template_name = 'admin/core/landingpageconfig/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:landingpageconfig_list') # we will map this URL name to this view

    def get_object(self, queryset=None):
        obj, created = LandingPageConfig.objects.get_or_create(id=1)
        return obj

    def form_valid(self, form):
        messages.success(self.request, "Landing Page Configuration updated successfully.")
        return super().form_valid(form)
