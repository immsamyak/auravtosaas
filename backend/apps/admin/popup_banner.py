from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import PopupBanner

class PopupBannerListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = PopupBanner
    template_name = 'admin/brands/popupbanner/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['id']
    filter_fields = []

class PopupBannerCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = PopupBanner
    template_name = 'admin/brands/popupbanner/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:popupbanner_list')

class PopupBannerUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = PopupBanner
    template_name = 'admin/brands/popupbanner/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:popupbanner_list')
