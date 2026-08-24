from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import Coupon

class CouponListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Coupon
    template_name = 'admin/brands/coupon/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class CouponCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Coupon
    template_name = 'admin/brands/coupon/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:coupon_list')

class CouponUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Coupon
    template_name = 'admin/brands/coupon/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:coupon_list')
