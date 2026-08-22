from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from apps.brands.models import Brand
from apps.fitting.models import VirtualTryOn
from apps.accounts.models import ConsumerProfile
from apps.billing.models import BrandSubscription
from django.db.models import Sum

class DashboardView(SuperUserRequiredMixin, TemplateView):
    template_name = 'admin/dashboard.html'

    def get_context_data(self, **kwargs):
        from apps.catalog.models import Product, ProductVariant
        from apps.orders.models import Order, Cart
        
        context = super().get_context_data(**kwargs)
        
        # High Level KPIs
        context['total_brands'] = Brand.objects.count()
        context['total_vto_jobs'] = VirtualTryOn.objects.count()
        context['total_consumers'] = ConsumerProfile.objects.count()
        
        mrr = BrandSubscription.objects.filter(status='ACTIVE').aggregate(Sum('plan__monthly_price'))['plan__monthly_price__sum'] or 0
        context['mrr'] = f"${mrr:,.2f}"
        
        # Commerce Metrics
        context['total_products'] = Product.objects.count()
        context['total_variants'] = ProductVariant.objects.count()
        context['total_orders'] = Order.objects.count()
        context['active_carts'] = Cart.objects.count()
        
        total_gmv = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['total_gmv'] = f"${total_gmv:,.2f}"
        
        # VTO Engine Metrics
        context['vto_completed'] = VirtualTryOn.objects.filter(status='COMPLETED').count()
        context['vto_processing'] = VirtualTryOn.objects.filter(status='PROCESSING').count()
        context['vto_failed'] = VirtualTryOn.objects.filter(status='FAILED').count()
        
        return context

class AdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True

class AdminLogoutView(LogoutView):
    next_page = 'admin:login'
