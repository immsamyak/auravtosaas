from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import FAQItem, Metric, IntegrationPlatform

class FAQItemListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = FAQItem
    template_name = 'admin/core/faqitem/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['question']
    filter_fields = ['is_active']

class FAQItemCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = FAQItem
    template_name = 'admin/core/faqitem/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:faqitem_list')

class FAQItemUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = FAQItem
    template_name = 'admin/core/faqitem/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:faqitem_list')

class FAQItemDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = FAQItem
    template_name = 'admin/core/faqitem/delete.html'
    success_url = reverse_lazy('admin:faqitem_list')

class MetricListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Metric
    template_name = 'admin/core/metric/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['label', 'value']
    filter_fields = ['is_active']

class MetricCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Metric
    template_name = 'admin/core/metric/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:metric_list')

class MetricUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Metric
    template_name = 'admin/core/metric/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:metric_list')

class MetricDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = Metric
    template_name = 'admin/core/metric/delete.html'
    success_url = reverse_lazy('admin:metric_list')

class IntegrationPlatformListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name']
    filter_fields = ['is_active']

class IntegrationPlatformCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:integrationplatform_list')

class IntegrationPlatformUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:integrationplatform_list')

class IntegrationPlatformDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/delete.html'
    success_url = reverse_lazy('admin:integrationplatform_list')
