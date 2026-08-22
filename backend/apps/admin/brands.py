from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from apps.brands.models import Brand

class BrandListView(SuperUserRequiredMixin, SearchFilterMixin, ListView):
    model = Brand
    template_name = 'admin/brands/brand/list.html'
    context_object_name = 'objects'
    paginate_by = 15
    search_fields = ['name', 'slug', 'contact_email', 'status', 'description', 'support_email', 'support_phone', 'address', 'instagram_url', 'facebook_url', 'tiktok_url', 'twitter_url', 'pinterest_url', 'currency_code', 'currency_symbol']
    filter_fields = ['owner', 'theme', 'status']

class BrandCreateView(SuperUserRequiredMixin, TailwindFormViewMixin, CreateView):
    model = Brand
    template_name = 'admin/brands/brand/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brand_list')

class BrandUpdateView(SuperUserRequiredMixin, TailwindFormViewMixin, UpdateView):
    model = Brand
    template_name = 'admin/brands/brand/form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin:brand_list')

from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User

class ImpersonateBrandView(SuperUserRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        brand = get_object_or_404(Brand, pk=pk)
        if brand.owner:
            # Store the original superadmin ID
            request.session['impersonator_id'] = request.user.id
            login(request, brand.owner, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"You are now impersonating {brand.name}.")
            return redirect('dashboard')
        else:
            messages.error(request, "This brand has no owner to impersonate.")
            return redirect('admin:brand_list')

class ImpersonateRevertView(View):
    def get(self, request, *args, **kwargs):
        impersonator_id = request.session.get('impersonator_id')
        if impersonator_id:
            try:
                superadmin = User.objects.get(id=impersonator_id)
                login(request, superadmin, backend='django.contrib.auth.backends.ModelBackend')
                del request.session['impersonator_id']
                messages.success(request, "Reverted to superadmin.")
                return redirect('admin:dashboard')
            except User.DoesNotExist:
                pass
        
        messages.error(request, "Could not revert impersonation.")
        return redirect('index')
