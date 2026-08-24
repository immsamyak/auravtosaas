from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.billing.models import SubscriptionPlan

class SubscriptionPlanListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = SubscriptionPlan
    template_name = 'admin/billing/subscriptionplan/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'stripe_price_id']
    filter_fields = ['is_popular']

class SubscriptionPlanCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = SubscriptionPlan
    template_name = 'admin/billing/subscriptionplan/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:subscriptionplan_list')

class SubscriptionPlanUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = SubscriptionPlan
    template_name = 'admin/billing/subscriptionplan/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:subscriptionplan_list')
