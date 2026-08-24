from .mixins import PlatformAdminRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from apps.core.models import ContactMessage

class ContactMessageListView(PlatformAdminRequiredMixin, SearchFilterMixin, ListView):
    model = ContactMessage
    template_name = 'admin/core/contactmessage/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'email', 'message']
    filter_fields = ['is_read']

class ContactMessageDetailView(PlatformAdminRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = ContactMessage
    template_name = 'admin/core/contactmessage/form.html'
    fields = ['is_read']
    success_url = reverse_lazy('admin:contactmessage_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Mark as read when opened
        if not self.object.is_read:
            self.object.is_read = True
            self.object.save()
        return context

class ContactMessageDeleteView(PlatformAdminRequiredMixin, DeleteView):
    model = ContactMessage
    template_name = 'admin/core/contactmessage/delete.html'
    success_url = reverse_lazy('admin:contactmessage_list')
