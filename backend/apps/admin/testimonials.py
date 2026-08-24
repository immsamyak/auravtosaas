from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import Testimonial

class TestimonialListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = Testimonial
    template_name = 'admin/core/testimonial/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['quote', 'author_name', 'author_title']
    filter_fields = ['is_active']

class TestimonialCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Testimonial
    template_name = 'admin/core/testimonial/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:testimonial_list')

class TestimonialUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Testimonial
    template_name = 'admin/core/testimonial/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:testimonial_list')
