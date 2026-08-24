from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.accounts.models import UserPhotoProfile

class UserPhotoProfileListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = UserPhotoProfile
    template_name = 'admin/accounts/userphotoprofile/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['session_key', 'processing_status']
    filter_fields = ['user', 'processing_status', 'is_default']

class UserPhotoProfileCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = UserPhotoProfile
    template_name = 'admin/accounts/userphotoprofile/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:userphotoprofile_list')

class UserPhotoProfileUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = UserPhotoProfile
    template_name = 'admin/accounts/userphotoprofile/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:userphotoprofile_list')
