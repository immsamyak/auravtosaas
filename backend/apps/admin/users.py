from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User

class UserListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = User
    template_name = 'admin/auth/user/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['username', 'first_name', 'last_name', 'email']
    filter_fields = ['is_superuser', 'is_staff', 'is_active']

class UserCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = User
    template_name = 'admin/auth/user/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:user_list')

class UserUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = User
    template_name = 'admin/auth/user/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:user_list')
