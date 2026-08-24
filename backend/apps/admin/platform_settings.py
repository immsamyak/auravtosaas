from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import SystemSetting

class SystemSettingListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = SystemSetting
    template_name = 'admin/core/systemsetting/list.html'
    context_object_name = 'objects'
    search_fields = ['key', 'value', 'category', 'description']
    
    def get_queryset(self):
        return super().get_queryset().order_by('category', 'key')

class SystemSettingCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = SystemSetting
    template_name = 'admin/core/systemsetting/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:systemsetting_list')

class SystemSettingUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = SystemSetting
    template_name = 'admin/core/systemsetting/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:systemsetting_list')
