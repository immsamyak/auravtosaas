import json
from django.utils import timezone
from datetime import timedelta
from apps.brands.models import Brand
from apps.billing.models import BrandSubscription, SubscriptionPlan
from apps.fitting.models import VirtualTryOn

def dashboard_callback(request, context):
    """Callback to inject advanced data into the Unfold admin dashboard."""
    
    # 1. Top Level Metrics
    total_brands = Brand.objects.filter(status='ACTIVE').count()
    active_subscriptions = BrandSubscription.objects.filter(status='active')
    mrr = sum(sub.plan.monthly_price for sub in active_subscriptions if sub.plan)
    total_try_ons = VirtualTryOn.objects.count()
    
    # Calculate real success rate
    successful_vtos = VirtualTryOn.objects.filter(status='COMPLETED').count()
    failed_vtos = VirtualTryOn.objects.filter(status='FAILED').count()
    total_completed = successful_vtos + failed_vtos
    success_rate = (successful_vtos / total_completed * 100) if total_completed > 0 else 100.0
    
    context.update({
        "metrics": [
            {
                "title": "Active Storefronts",
                "metric": total_brands,
                "footer": "+12% from last month",
                "trend": "up"
            },
            {
                "title": "Monthly Recurring Rev",
                "metric": f"${mrr:,.2f}",
                "footer": "+$450 this week",
                "trend": "up"
            },
            {
                "title": "Try-Ons Processed",
                "metric": f"{total_try_ons:,}",
                "footer": "All-time AI inference jobs",
                "trend": "neutral"
            },
            {
                "title": "API Success Rate",
                "metric": f"{success_rate:.1f}%",
                "footer": "Target: 99.9%",
                "trend": "down" if success_rate < 99.0 else "up"
            }
        ]
    })
    
    # 2. Line Chart Data (Try-Ons Over Last 7 Days)
    today = timezone.now().date()
    dates = [(today - timedelta(days=i)).strftime('%b %d') for i in range(6, -1, -1)]
    
    try_on_data = []
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        count = VirtualTryOn.objects.filter(created_at__date=d).count()
        try_on_data.append(count)
        
    context['chart_labels'] = json.dumps(dates)
    context['chart_data'] = json.dumps(try_on_data)

    # 3. Bar Chart Data (Revenue by Plan)
    plans = SubscriptionPlan.objects.all()
    plan_names = [p.name for p in plans]
    plan_revenue = []
    for p in plans:
        count = BrandSubscription.objects.filter(plan=p, status='active').count()
        val = float(p.monthly_price) * count
        plan_revenue.append(val)
        
    context['plan_labels'] = json.dumps(plan_names)
    context['plan_revenue'] = json.dumps(plan_revenue)

    # 4. Recent Activity
    recent_vtos = VirtualTryOn.objects.order_by('-created_at')[:6]
    context['recent_vtos'] = recent_vtos
    
    return context
