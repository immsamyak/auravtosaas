from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import Group

class GroupListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = Group
    template_name = 'admin/auth/group/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name']
    filter_fields = []

class GroupCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Group
    template_name = 'admin/auth/group/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:group_list')

class GroupUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Group
    template_name = 'admin/auth/group/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:group_list')
