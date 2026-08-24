from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.catalog.models import ProductReview

class ProductReviewListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = ProductReview
    template_name = 'admin/catalog/productreview/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class ProductReviewCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = ProductReview
    template_name = 'admin/catalog/productreview/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:productreview_list')

class ProductReviewUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ProductReview
    template_name = 'admin/catalog/productreview/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:productreview_list')
