from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import NewsletterSubscriber

class NewsletterSubscriberListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = NewsletterSubscriber
    template_name = 'admin/brands/newslettersubscriber/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class NewsletterSubscriberCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = NewsletterSubscriber
    template_name = 'admin/brands/newslettersubscriber/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:newslettersubscriber_list')

class NewsletterSubscriberUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = NewsletterSubscriber
    template_name = 'admin/brands/newslettersubscriber/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:newslettersubscriber_list')
