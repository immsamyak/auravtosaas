from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.billing.models import BrandSubscription

class BrandSubscriptionListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = BrandSubscription
    template_name = 'admin/billing/brandsubscription/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['status', 'stripe_customer_id', 'stripe_subscription_id']
    filter_fields = ['brand', 'plan', 'status']

class BrandSubscriptionCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = BrandSubscription
    template_name = 'admin/billing/brandsubscription/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandsubscription_list')

class BrandSubscriptionUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = BrandSubscription
    template_name = 'admin/billing/brandsubscription/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandsubscription_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object and self.object.brand:
            qs = self.object.brand.subscription_history.all()
            
            # Apply time/date filters if present
            date_start = self.request.GET.get('history_date_start')
            date_end = self.request.GET.get('history_date_end')
            
            if date_start:
                qs = qs.filter(created_at__gte=date_start)
            if date_end:
                qs = qs.filter(created_at__lte=date_end + " 23:59:59")
                
            context['history_list'] = qs
            context['history_date_start'] = date_start or ''
            context['history_date_end'] = date_end or ''
            
        return context
