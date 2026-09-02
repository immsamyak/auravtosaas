import os

filepath = 'apps/inventory/models.py'
with open(filepath, 'r') as f:
    content = f.read()

# Add StockAuditLog Model
new_model = """
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
"""

# Modify StockLevel.save to support `_audit_action`, `_audit_reference`, `_audit_notes`
target_save = """    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_quantity = None
        if not is_new:
            try:
                old_quantity = StockLevel.objects.get(pk=self.pk).quantity
            except StockLevel.DoesNotExist:
                pass
                
        super().save(*args, **kwargs)
        
        # trigger notification if dropping to or below 5"""

replacement_save = """    def save(self, *args, **kwargs):
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
        
        # trigger notification if dropping to or below 5"""

if "class StockAuditLog" not in content:
    content = content + new_model
    content = content.replace(target_save, replacement_save)

with open(filepath, 'w') as f:
    f.write(content)
