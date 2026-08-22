from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.billing.models import BrandSubscription

class BrandSubscriptionListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = BrandSubscription
    template_name = 'admin/billing/brandsubscription/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['status', 'stripe_customer_id', 'stripe_subscription_id']
    filter_fields = ['brand', 'plan', 'status']

class BrandSubscriptionCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = BrandSubscription
    template_name = 'admin/billing/brandsubscription/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandsubscription_list')

class BrandSubscriptionUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = BrandSubscription
    template_name = 'admin/billing/brandsubscription/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandsubscription_list')
