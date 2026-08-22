from django import template
from django.db.models import Sum, Count
from apps.brands.models import Brand
from apps.orders.models import Order
from apps.fitting.models import VirtualTryOn
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_hq_stats():
    total_brands = Brand.objects.count()
    total_users = User.objects.count()
    total_vtos = VirtualTryOn.objects.filter(status='COMPLETED').count()
    total_revenue = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
    
    return {
        'total_brands': total_brands,
        'total_users': total_users,
        'total_vtos': total_vtos,
        'total_revenue': total_revenue,
    }

@register.simple_tag
def get_recent_orders():
    return Order.objects.select_related('brand', 'user').order_by('-created_at')[:10]

@register.simple_tag
def get_active_brands():
    return Brand.objects.annotate(order_count=Count('orders')).order_by('-order_count')[:5]
