from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.recommendations.models import SizeRecommendation

class SizeRecommendationListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = SizeRecommendation
    template_name = 'admin/recommendations/sizerecommendation/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['recommended_size', 'fit_type']
    filter_fields = ['user', 'product']

class SizeRecommendationCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = SizeRecommendation
    template_name = 'admin/recommendations/sizerecommendation/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:sizerecommendation_list')

class SizeRecommendationUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = SizeRecommendation
    template_name = 'admin/recommendations/sizerecommendation/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:sizerecommendation_list')
