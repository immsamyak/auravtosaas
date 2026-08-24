from .mixins import SuperUserRequiredMixin, TailwindFormViewMixin, SearchFilterMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from apps.brands.models import Brand
from apps.fitting.models import VirtualTryOn
from apps.accounts.models import ConsumerProfile
from apps.billing.models import BrandSubscription
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
import psutil
import time
from django.db import connection
import platform
import subprocess

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
        now = timezone.now()
        last_30 = now - timedelta(days=30)
        
        context['total_products'] = Product.objects.count()
        context['total_variants'] = ProductVariant.objects.count()
        
        total_orders = Order.objects.count()
        context['total_orders'] = total_orders
        
        active_carts = Cart.objects.count()
        context['active_carts'] = active_carts
        
        total_gmv = Order.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        context['total_gmv'] = f"${total_gmv:,.2f}"
        
        # Calculate Trends & Advanced Stats
        context['new_brands_trend'] = f"{Brand.objects.filter(created_at__gte=last_30).count()} New"
        context['vto_trend'] = f"+{VirtualTryOn.objects.filter(created_at__gte=last_30).count()} Run"
        context['orders_trend'] = f"+{Order.objects.filter(created_at__gte=last_30).count()}"
        context['consumers_trend'] = f"+{ConsumerProfile.objects.filter(user__date_joined__gte=last_30).count()} New"
        
        aov = float(total_gmv) / total_orders if total_orders > 0 else 0.0
        context['avg_order_value'] = f"${aov:,.2f}"
        
        total_checkouts = active_carts + total_orders
        abandonment = (active_carts / total_checkouts * 100) if total_checkouts > 0 else 0.0
        context['cart_abandonment'] = f"{abandonment:.1f}%"
        
        total_consumers = context['total_consumers']
        conversion = (total_orders / total_consumers * 100) if total_consumers > 0 else 0.0
        context['conversion_rate'] = f"{conversion:.1f}%"
        
        refunded = Order.objects.filter(status='REFUNDED').count()
        refund_rate = (refunded / total_orders * 100) if total_orders > 0 else 0.0
        context['refund_rate'] = f"{refund_rate:.1f}%"
        
        top_size = ProductVariant.objects.filter(size__isnull=False).values('size__name').annotate(c=Count('id')).order_by('-c').first()
        context['top_size'] = top_size['size__name'] if top_size else "N/A"
        
        top_color = ProductVariant.objects.filter(color__isnull=False).values('color__name').annotate(c=Count('id')).order_by('-c').first()
        context['top_color'] = top_color['color__name'] if top_color else "N/A"
        
        disk_used = psutil.disk_usage('/').used
        context['storage_used'] = f"{round(disk_used / (1024**3), 1)} GB"

        # VTO Engine Metrics
        context['vto_completed'] = VirtualTryOn.objects.filter(status='COMPLETED').count()
        context['vto_processing'] = VirtualTryOn.objects.filter(status='PROCESSING').count()
        context['vto_failed'] = VirtualTryOn.objects.filter(status='FAILED').count()
        
        # Real-time System Metrics (Deep Research)

        # Try to get real CPU name
        try:
            if platform.system() == "Darwin":
                sys_cpu_name = subprocess.check_output(["sysctl", "-n", "machdep.cpu.brand_string"]).strip().decode("utf-8")
            else:
                with open("/proc/cpuinfo") as f:
                    for line in f:
                        if "model name" in line:
                            sys_cpu_name = line.split(":")[1].strip()
                            break
                    else:
                        sys_cpu_name = platform.processor()
        except Exception:
            sys_cpu_name = platform.processor() or "Unknown CPU"

        context['sys_cpu'] = psutil.cpu_percent(interval=0.1)
        context['sys_cpu_name'] = sys_cpu_name
        
        mem = psutil.virtual_memory()
        context['sys_mem'] = mem.percent
        context['sys_mem_total'] = f"{round(mem.total / (1024**3))}GB Total Configured"
        
        disk = psutil.disk_usage('/')
        context['sys_disk'] = disk.percent
        context['sys_disk_total'] = f"{round(disk.total / (1024**3))}GB Total Storage"
        
        # Measure DB Latency and Version
        try:
            t1 = time.time()
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.execute("SELECT version()")
                db_version = cursor.fetchone()[0]
            db_latency = int((time.time() - t1) * 1000)
            
            # Extract just the main engine name from version string
            if "PostgreSQL" in db_version:
                context['sys_db_name'] = "PostgreSQL " + db_version.split()[1]
            elif "sqlite" in db_version.lower():
                context['sys_db_name'] = "SQLite Database"
            else:
                context['sys_db_name'] = db_version[:20]
        except Exception:
            db_latency = 0
            context['sys_db_name'] = "Database"
        
        uptime_seconds = time.time() - psutil.boot_time()
        days, remainder = divmod(uptime_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)
        context['sys_uptime'] = f"{int(days)}d {int(hours)}h {int(minutes)}m"
        context['sys_db_latency'] = db_latency
        
        # Redis Cache Hit Rate (Real-time from Coolify server)
        try:
            import redis
            r = redis.Redis(
                host='64.227.167.223',
                port=6379,
                db=1,
                password='bx2Ee2Q8grqKcWfawRwCVoz8YKyQsqciijqsSmUIe1PDZIOnbbYj9liWJ2c6jQDp',
                decode_responses=True
            )
            info = r.info('stats')
            hits = info.get('keyspace_hits', 0)
            misses = info.get('keyspace_misses', 0)
            total = hits + misses
            context['sys_cache_hit_rate'] = round((hits / total * 100), 1) if total > 0 else 0.0
        except Exception:
            context['sys_cache_hit_rate'] = "Offline"
            
        context['sys_queue_depth'] = max(0, context['vto_processing']) # Tied to active processing jobs
        
        return context

class AdminLoginView(LoginView):
    template_name = 'admin/login.html'
    redirect_authenticated_user = True

class AdminLogoutView(LogoutView):
    next_page = 'admin:login'
