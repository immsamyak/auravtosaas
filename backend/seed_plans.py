import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.billing.models import SubscriptionPlan

# Free Trial (implicitly created when brand signs up, but let's define paid plans)
SubscriptionPlan.objects.get_or_create(
    name="Starter",
    defaults={
        "monthly_price": 299.00,
        "try_on_quota": 10000,
        "is_popular": False,
        "features": ["Up to 10,000 try-ons", "Standard resolution", "Email support"]
    }
)

SubscriptionPlan.objects.get_or_create(
    name="Growth",
    defaults={
        "monthly_price": 899.00,
        "try_on_quota": 50000,
        "is_popular": True,
        "features": ["Up to 50,000 try-ons", "High resolution HD", "Priority API queue"]
    }
)

SubscriptionPlan.objects.get_or_create(
    name="Enterprise",
    defaults={
        "monthly_price": 2999.00,
        "try_on_quota": -1,
        "is_popular": False,
        "features": ["Unlimited try-ons", "Custom SLA & Support", "Dedicated GPU nodes"]
    }
)

print("Seeded subscription plans!")
