from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import FAQItem, Metric, IntegrationPlatform

class FAQItemListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = FAQItem
    template_name = 'admin/core/faqitem/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['question']
    filter_fields = ['is_active']

class FAQItemCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = FAQItem
    template_name = 'admin/core/faqitem/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:faqitem_list')

class FAQItemUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = FAQItem
    template_name = 'admin/core/faqitem/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:faqitem_list')

class FAQItemDeleteView(SuperUserRequiredMixin, DeleteView):
    model = FAQItem
    template_name = 'admin/core/faqitem/delete.html'
    success_url = reverse_lazy('admin:faqitem_list')

class MetricListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = Metric
    template_name = 'admin/core/metric/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['label', 'value']
    filter_fields = ['is_active']

class MetricCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Metric
    template_name = 'admin/core/metric/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:metric_list')

class MetricUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Metric
    template_name = 'admin/core/metric/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:metric_list')

class MetricDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Metric
    template_name = 'admin/core/metric/delete.html'
    success_url = reverse_lazy('admin:metric_list')

class IntegrationPlatformListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name']
    filter_fields = ['is_active']

class IntegrationPlatformCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:integrationplatform_list')

class IntegrationPlatformUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:integrationplatform_list')

class IntegrationPlatformDeleteView(SuperUserRequiredMixin, DeleteView):
    model = IntegrationPlatform
    template_name = 'admin/core/integrationplatform/delete.html'
    success_url = reverse_lazy('admin:integrationplatform_list')
