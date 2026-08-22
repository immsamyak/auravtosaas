from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin

from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages
from apps.core.models import GlobalSettings

class GlobalSettingsUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = GlobalSettings
    template_name = 'admin/core/globalsettings/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:globalsettings_edit')

    def get_object(self, queryset=None):
        return GlobalSettings.get_settings()
        
    def form_valid(self, form):
        messages.success(self.request, "Global settings updated successfully.")
        return super().form_valid(form)
