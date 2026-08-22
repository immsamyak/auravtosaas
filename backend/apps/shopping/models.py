from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.contrib.auth.models import User
from apps.brands.models import Brand
import uuid
import secrets
import string


class GiftCard(models.Model):
    """
    Purchasable gift cards tied to a specific brand.
    Can be redeemed at checkout to add store credit.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('REDEEMED', 'Fully Redeemed'),
        ('EXPIRED', 'Expired'),
        ('DISABLED', 'Disabled'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='gift_cards')
    
    # Unique redemption code (e.g., AURA-XXXX-XXXX-XXXX)
    code = models.CharField(max_length=30, unique=True, db_index=True)
    
    # Monetary value
    initial_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))], help_text="Original gift card value")
    remaining_value = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))], help_text="Remaining balance")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Purchase & Recipient info
    purchased_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='purchased_gift_cards')
    recipient_email = models.EmailField(blank=True, help_text="Email to send the gift card to")
    recipient_name = models.CharField(max_length=200, blank=True)
    personal_message = models.TextField(blank=True, help_text="Gift message from sender")
    
    redeemed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='redeemed_gift_cards')
    redeemed_at = models.DateTimeField(null=True, blank=True)
    
    expires_at = models.DateTimeField(null=True, blank=True, help_text="Leave blank for no expiry")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Gift Card {self.code} — {self.brand.get_currency_symbol}{self.remaining_value}/{self.initial_value}"
    
    @classmethod
    def generate_code(cls):
        """Generate a unique gift card code like AURA-XXXX-XXXX-XXXX"""
        chars = string.ascii_uppercase + string.digits
        while True:
            segments = [''.join(secrets.choice(chars) for _ in range(4)) for _ in range(3)]
            code = f"AURA-{'-'.join(segments)}"
            if not cls.objects.filter(code=code).exists():
                return code
    
    def redeem(self, amount, user=None):
        """Deduct amount from gift card. Returns actual amount deducted."""
        if self.status != 'ACTIVE':
            raise ValidationError("This gift card is not active.")
        deducted = min(amount, self.remaining_value)
        self.remaining_value -= deducted
        if self.remaining_value <= 0:
            self.status = 'REDEEMED'
            self.redeemed_by = user
            from django.utils import timezone
            self.redeemed_at = timezone.now()
        self.save()
        return deducted


class GiftCardTransaction(models.Model):
    """Tracks every debit/credit against a gift card for audit."""
    TRANSACTION_TYPES = [
        ('PURCHASE', 'Initial Purchase'),
        ('REDEMPTION', 'Redeemed at Checkout'),
        ('REFUND', 'Refund / Credit Back'),
    ]
    
    gift_card = models.ForeignKey(GiftCard, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)
    
    order = models.ForeignKey('orders.Order', on_delete=models.SET_NULL, null=True, blank=True, help_text="Associated order")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} — {self.amount} on {self.gift_card.code}"
