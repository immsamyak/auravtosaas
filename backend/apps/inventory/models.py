from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.brands.models import Brand
from apps.catalog.models import ProductVariant

class Location(models.Model):
    LOCATION_TYPES = (
        ('STORE', 'Physical Store'),
        ('WAREHOUSE', 'Warehouse'),
        ('ONLINE', 'Online Fulfillment Center'),
    )
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=255)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPES, default='STORE')
    address = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.brand.name} - {self.name} ({self.get_location_type_display()})"

class StockLevel(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='stock_levels')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='stock_levels')
    quantity = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('location', 'product_variant')
        
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_quantity = None
        if not is_new:
            try:
                old_quantity = StockLevel.objects.get(pk=self.pk).quantity
            except StockLevel.DoesNotExist:
                pass
                
        super().save(*args, **kwargs)
        
        # Create Audit Log if quantity changed
        if is_new or (old_quantity is not None and old_quantity != self.quantity):
            StockAuditLog.objects.create(
                stock_level=self,
                previous_quantity=old_quantity if old_quantity is not None else 0,
                new_quantity=self.quantity,
                action_type=getattr(self, '_audit_action', 'MANUAL'),
                reference_id=getattr(self, '_audit_reference', None),
                notes=getattr(self, '_audit_notes', None)
            )
        
        # trigger notification if dropping to or below 5
        if self.quantity <= 5 and (is_new or (old_quantity is not None and old_quantity > 5)):
            from apps.core.utils import notify
            from apps.core.email_utils import dispatch_async_email
            brand = self.product_variant.product.brand
            
            # In-app notification
            notify(
                user=brand.owner,
                title="Low Stock Alert",
                message=f"{self.product_variant.product.name} ({self.product_variant.size.code}) is at {self.quantity} in {self.location.name}.",
                icon_class="fa-solid fa-triangle-exclamation text-rose-500",
                action_url=f"/dashboard/products/{self.product_variant.product.id}/"
            )
            
            # Email notification
            try:
                context = {
                    'product_name': self.product_variant.product.name,
                    'variant_name': str(self.product_variant),
                    'stock_level': self.quantity,
                }
                dispatch_async_email('low_inventory_alert', context, [brand.owner.email], brand)
            except Exception as e:
                pass


    def __str__(self):
        return f"{self.product_variant} @ {self.location.name}: {self.quantity}"

class StockAuditLog(models.Model):
    ACTION_CHOICES = (
        ('MANUAL', 'Manual Adjustment'),
        ('ORDER', 'Order Fulfillment'),
        ('RESTOCK', 'Restock/Purchase'),
        ('RETURN', 'Customer Return'),
        ('POS', 'POS Sale'),
    )
    stock_level = models.ForeignKey(StockLevel, on_delete=models.CASCADE, related_name='audit_logs')
    previous_quantity = models.IntegerField()
    new_quantity = models.IntegerField()
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES, default='MANUAL')
    reference_id = models.CharField(max_length=100, null=True, blank=True, help_text="Order ID or Transaction ID")
    notes = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.stock_level.product_variant} - {self.action_type}: {self.previous_quantity} -> {self.new_quantity}"
