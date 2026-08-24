from django.db.models import Count, Avg
from apps.fitting.models import VirtualTryOn
from apps.catalog.models import ProductVariant

class DashboardAnalyticsService:
    @staticmethod
    def get_dashboard_metrics(brand):
        total_try_ons = VirtualTryOn.objects.filter(product_variant__product__brand=brand).count()
        # Fallback to total brand purchases since VTO conversion tracking was decoupled
        from apps.orders.models import OrderItem
        purchases = OrderItem.objects.filter(order__brand=brand).count()
        conversion_rate = round((purchases / total_try_ons * 100), 1) if total_try_ons > 0 else 0
        
        avg_confidence = VirtualTryOn.objects.filter(product_variant__product__brand=brand).aggregate(Avg('ai_confidence_score'))['ai_confidence_score__avg']
        avg_confidence = round((avg_confidence * 100), 1) if avg_confidence else 0
        
        # Top products by Try-On count for this brand
        top_products = ProductVariant.objects.filter(product__brand=brand).annotate(
            try_on_count=Count('try_ons')
        ).order_by('-try_on_count')[:5]
        
        # Real-time Chart Data (Last 7 Days)
        from django.utils import timezone
        import datetime
        from django.db.models.functions import TruncDate
        
        today = timezone.now().date()
        chart_labels = []
        chart_data = []
        
        # Get try-ons grouped by date
        daily_try_ons = VirtualTryOn.objects.filter(
            product_variant__product__brand=brand,
            created_at__gte=today - datetime.timedelta(days=6)
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(count=Count('id'))
        
        try_ons_dict = {entry['date'].strftime('%b %d'): entry['count'] for entry in daily_try_ons if entry['date']}
        
        for i in range(6, -1, -1):
            date_label = (today - datetime.timedelta(days=i)).strftime('%b %d')
            chart_labels.append(date_label)
            chart_data.append(try_ons_dict.get(date_label, 0))
            
        from django.db.models import Sum, F
        from apps.orders.models import Order, OrderItem
        
        # Additional Revenue Metrics
        total_revenue = Order.objects.filter(
            brand=brand, 
            status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED']
        ).annotate(
            calc_grand_total=F('total_amount') + F('shipping_cost') + F('tax_amount') - F('discount_amount')
        ).aggregate(total=Sum('calc_grand_total'))['total'] or 0
        
        # Revenue Over Time Chart (Last 7 Days)
        revenue_data = []
        daily_revenue = Order.objects.filter(
            brand=brand,
            status__in=['PAID', 'SHIPPED', 'DELIVERED', 'COMPLETED'],
            created_at__gte=today - datetime.timedelta(days=6)
        ).annotate(
            date=TruncDate('created_at'),
            calc_grand_total=F('total_amount') + F('shipping_cost') + F('tax_amount') - F('discount_amount')
        ).values('date').annotate(total=Sum('calc_grand_total'))
        
        revenue_dict = {entry['date'].strftime('%b %d'): float(entry['total']) for entry in daily_revenue if entry['date']}
        
        for i in range(6, -1, -1):
            date_label = (today - datetime.timedelta(days=i)).strftime('%b %d')
            revenue_data.append(revenue_dict.get(date_label, 0.0))

        # Recent Activity
        recent_try_ons = VirtualTryOn.objects.filter(
            product_variant__product__brand=brand
        ).select_related('product_variant__product', 'session__passport__user').order_by('-created_at')[:6]
        
        # System Health (Status Breakdown)
        status_counts = VirtualTryOn.objects.filter(product_variant__product__brand=brand).values('status').annotate(count=Count('id'))
        status_data = {
            'completed': 0,
            'failed': 0,
            'processing': 0
        }
        for s in status_counts:
            if s['status'] == 'COMPLETED':
                status_data['completed'] = s['count']
            elif s['status'] == 'FAILED':
                status_data['failed'] = s['count']
            else:
                status_data['processing'] += s['count']
                
        import json
        
        return {
            'total_try_ons': total_try_ons,
            'total_revenue': total_revenue,
            'revenue_data': json.dumps(revenue_data),
            'purchases': purchases,
            'conversion_rate': conversion_rate,
            'avg_confidence': avg_confidence,
            'top_products': top_products,
            'chart_labels': json.dumps(chart_labels),
            'chart_data': json.dumps(chart_data),
            'recent_try_ons': recent_try_ons,
            'status_data': json.dumps([status_data['completed'], status_data['processing'], status_data['failed']]),
        }
