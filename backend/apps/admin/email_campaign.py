from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import EmailCampaign

class EmailCampaignListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = EmailCampaign
    template_name = 'admin/brands/emailcampaign/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class EmailCampaignCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = EmailCampaign
    template_name = 'admin/brands/emailcampaign/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:emailcampaign_list')

class EmailCampaignUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = EmailCampaign
    template_name = 'admin/brands/emailcampaign/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:emailcampaign_list')
