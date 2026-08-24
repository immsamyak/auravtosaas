from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from apps.brands.models import BrandStaff

class BrandStaffListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = BrandStaff
    template_name = 'admin/brands/brandstaff/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['user__email', 'user__username', 'brand__name']
    filter_fields = ['role', 'brand']

class BrandStaffUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = BrandStaff
    template_name = 'admin/brands/brandstaff/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brandstaff_list')
