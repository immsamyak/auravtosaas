from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.shopping.models import GiftCardTransaction

class GiftCardTransactionListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = GiftCardTransaction
    template_name = 'admin/shopping/giftcardtransaction/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class GiftCardTransactionCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = GiftCardTransaction
    template_name = 'admin/shopping/giftcardtransaction/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:giftcardtransaction_list')

class GiftCardTransactionUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = GiftCardTransaction
    template_name = 'admin/shopping/giftcardtransaction/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:giftcardtransaction_list')
