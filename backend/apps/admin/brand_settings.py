from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import BrandSetting

class BrandSettingListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = BrandSetting
    template_name = 'admin/core/brandsetting/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['currency', 'contact_email', 'primary_color', 'google_review_url', 'wifi_network_name', 'wifi_password', 'pos_thermal_paper_size', 'tax_id_type', 'tax_id_number']
    filter_fields = ['brand', 'show_tax_on_receipt']

class BrandSettingCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = BrandSetting
    template_name = 'admin/core/brandsetting/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandsetting_list')

class BrandSettingUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = BrandSetting
    template_name = 'admin/core/brandsetting/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandsetting_list')
