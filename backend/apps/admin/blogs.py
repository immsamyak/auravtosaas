from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.core.models import BlogPost

class BlogPostListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = BlogPost
    template_name = 'admin/core/blogpost/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['title', 'content', 'author_name']
    filter_fields = ['is_published']

class BlogPostCreateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, CreateView):
    model = BlogPost
    template_name = 'admin/core/blogpost/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:blogpost_list')

class BlogPostUpdateView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = BlogPost
    template_name = 'admin/core/blogpost/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:blogpost_list')

class BlogPostDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'admin/core/blogpost/delete.html'
    success_url = reverse_lazy('admin:blogpost_list')
