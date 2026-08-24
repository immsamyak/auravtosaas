from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.shopping.models import GiftCard

class GiftCardListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = GiftCard
    template_name = 'admin/shopping/giftcard/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class GiftCardCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = GiftCard
    template_name = 'admin/shopping/giftcard/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:giftcard_list')

class GiftCardUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = GiftCard
    template_name = 'admin/shopping/giftcard/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:giftcard_list')
