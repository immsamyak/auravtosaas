from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.forms import FileField, ImageField
from .widgets import TailwindImageWidget
from django.contrib import messages

class SuperUserRequiredMixin(UserPassesTestMixin):
    """
    Restricts view access exclusively to active superusers.
    Redirects unauthenticated or unauthorized users to the admin login page.
    """
    login_url = reverse_lazy('admin:login')

    def test_func(self):
        return self.request.user.is_active and self.request.user.is_superuser


class TailwindFormViewMixin:
    """Injects Tailwind CSS classes into all form widgets."""
    
    def form_valid(self, form):
        messages.success(self.request, f"Record saved successfully.")
        return super().form_valid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, "Validation failed. Please correct the errors below.")
        return super().form_invalid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            
            # Apply custom TailwindImageWidget for file/image uploads
            if isinstance(field, (FileField, ImageField)):
                # We instantiate it with the original widget's attrs just in case
                field.widget = TailwindImageWidget(attrs=field.widget.attrs)
            
            field.widget.attrs.setdefault('class', '')
            
            # Base classes for inputs
            base_classes = 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition mt-1'
            
            # Checkbox specific classes
            if getattr(field.widget, 'input_type', None) == 'checkbox':
                base_classes = 'w-5 h-5 text-indigo-600 bg-slate-100 border-slate-300 rounded focus:ring-indigo-500 focus:ring-2 mt-1 cursor-pointer'
            
            # File input specific classes (for the "Upload New" button)
            if getattr(field.widget, 'input_type', None) == 'file':
                base_classes = 'w-full px-4 py-3 rounded-xl border border-slate-200 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition mt-1 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100 cursor-pointer bg-white'

            field.widget.attrs['class'] += f' {base_classes}'
        return form

class SearchFilterMixin:
    """Adds universal ?q= searching and ?filter_x= matching to ListViews."""
    search_fields = []
    filter_fields = []
    
    def get_queryset(self):
        qs = super().get_queryset()
        
        # Text Search
        q = self.request.GET.get('q')
        if q and self.search_fields:
            from django.db.models import Q
            query = Q()
            for field in self.search_fields:
                query |= Q(**{f"{field}__icontains": q})
            qs = qs.filter(query)
            
        # Exact Filters (Booleans, Choices, FKs)
        if self.filter_fields:
            filter_kwargs = {}
            for field in self.filter_fields:
                val = self.request.GET.get(field)
                if val:
                    if val.lower() == 'true':
                        val = True
                    elif val.lower() == 'false':
                        val = False
                    filter_kwargs[field] = val
            if filter_kwargs:
                qs = qs.filter(**filter_kwargs)
                
        return qs.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        # Pass active filters so template can select them
        active_filters = {}
        for f in self.filter_fields:
            val = self.request.GET.get(f, '')
            active_filters[f] = val
        context['active_filters'] = active_filters
        
        # Pass filter choices to the context if we have a form/model
        # But for Alpine real-time, the template will hardcode the options during generation
        return context
