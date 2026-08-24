from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.brands.models import Brand

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    stripe_price_id = models.CharField(max_length=255, blank=True, null=True, help_text="Stripe Price ID (e.g. price_1N...)")
    monthly_price = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, default=0.00)
    try_on_quota = models.IntegerField(default=10000, help_text="Number of try-ons per billing cycle (-1 for unlimited)")
    is_popular = models.BooleanField(default=False)
    features = models.JSONField(default=list, help_text="List of features as JSON strings")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} (${self.monthly_price}/mo)"

class BrandSubscription(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('trialing', 'Trialing'),
        ('past_due', 'Past Due'),
        ('canceled', 'Canceled'),
        ('incomplete', 'Incomplete')
    ]
    
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')
    
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    
    try_ons_used = models.IntegerField(default=0)
    current_period_end = models.DateTimeField(blank=True, null=True)
    trial_ends_at = models.DateTimeField(blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand.name} - {self.status}"
        
    def can_try_on(self):
        """Check if the brand has an active subscription and hasn't exceeded quota."""
        if self.status not in ['active', 'trialing']:
            return False
        if not self.plan:
            return False
        if self.plan.try_on_quota == -1:
            return True
        return self.try_ons_used < self.plan.try_on_quota


from django.db.models.signals import pre_save
from django.dispatch import receiver
from apps.core.notifications import NotificationManager

@receiver(pre_save, sender=BrandSubscription)
def subscription_status_changed(sender, instance, **kwargs):
    if instance.id:
        old_sub = BrandSubscription.objects.get(pk=instance.id)
        # Trigger if it wasn't active and now is, OR if the plan changed and is active
        if instance.status == 'ACTIVE' and (old_sub.status != 'ACTIVE' or old_sub.plan_id != instance.plan_id):
            try:
                NotificationManager.send_subscription_success(instance.brand, instance)
            except Exception as e:
                import logging
                logging.getLogger(__name__).error(f"Failed to send subscription confirmation: {e}")
