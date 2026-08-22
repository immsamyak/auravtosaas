from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.contrib.auth.models import User
from apps.brands.models import Brand
from apps.catalog.models import ProductVariant
import uuid


class ShippingZone(models.Model):
    """Owner-configurable shipping zones and rates."""
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='shipping_zones')
    name = models.CharField(max_length=100, help_text="e.g. Inside Valley, Outside Valley, Nationwide")
    rate = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, help_text="Shipping cost for this zone")
    estimated_days = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 1-2 days, 3-5 days")
    is_free_above = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, null=True, blank=True, help_text="Free shipping if order total is above this amount (leave blank for no free threshold)")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', 'rate']
        unique_together = ('brand', 'name')
    
    def __str__(self):
        return f"{self.brand.name} - {self.name}: Rs. {self.rate}"


class DeliveryProvince(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='delivery_provinces')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ('brand', 'name')
        
    def __str__(self):
        return self.name

class DeliveryDistrict(models.Model):
    province = models.ForeignKey(DeliveryProvince, on_delete=models.CASCADE, related_name='districts')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ('province', 'name')
        
    def __str__(self):
        return f"{self.name} ({self.province.name})"

class DeliveryCity(models.Model):
    district = models.ForeignKey(DeliveryDistrict, on_delete=models.CASCADE, related_name='cities')
    name = models.CharField(max_length=100)
    
    # Pricing for this specific city
    rate = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, default=0)
    estimated_days = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 1-2 days")
    is_free_above = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ('district', 'name')
        
    def __str__(self):
        return f"{self.name} - Rs. {self.rate}"


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    brand = models.ForeignKey('brands.Brand', on_delete=models.CASCADE, null=True, blank=True, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart {self.id} for {self.user.username if self.user else 'Guest'}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} in Cart {self.cart.id}"

class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('PROCESSING', 'Processing'),
        ('SENT_TO_COURIER', 'Sent to Courier'),
        ('COURIER_PROCESSING', 'Courier Processing'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, default=0.00)
    shipping_cost = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, default=0.00)
    shipping_zone = models.ForeignKey(ShippingZone, on_delete=models.SET_NULL, null=True, blank=True)
    delivery_city = models.ForeignKey(DeliveryCity, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Discount Details
    coupon = models.ForeignKey('brands.Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    discount_amount = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, default=0.00)
    
    # Tax Details
    tax_rate = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=5, decimal_places=2, default=0.00, help_text="Percentage applied at time of purchase")
    tax_amount = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2, default=0.00)
    
    # Integrations Tracking
    payment_provider = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. ESEWA, KHALTI, MANUAL")
    payment_reference_id = models.CharField(max_length=255, blank=True, null=True, help_text="Transaction ID from the gateway")
    payment_proof = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='payment_proofs/', blank=True, null=True, help_text="Screenshot of manual/QR payment")
    shipping_provider = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. PATHAO_PARCEL, NCM, UPAYA")
    tracking_number = models.CharField(max_length=255, blank=True, null=True, help_text="Consignment ID from the logistics provider")
    
    # Customer Details (for guest checkouts and shipping)
    customer_name = models.CharField(max_length=255, blank=True, null=True)
    customer_phone = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{9,15}$", message="Invalid phone format.")], max_length=20, blank=True, null=True)
    shipping_address = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def grand_total(self):
        return max(Decimal('0.00'), self.total_amount + self.shipping_cost + self.tax_amount - self.discount_amount)
    

    def clean(self):
        super().clean()
        if self.status == 'SHIPPED' and not self.tracking_number:
            raise ValidationError({'tracking_number': 'Tracking number is required when order is shipped.'})

    def __str__(self):
        return f"Order {self.id} - {self.brand.name} - {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product_variant} in Order {self.order.id}"

class ReturnRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved (Waiting for item)'),
        ('RECEIVED', 'Item Received'),
        ('REFUNDED', 'Refunded'),
        ('REJECTED', 'Rejected'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='returns')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='returns')
    customer_email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    reason = models.TextField(help_text="Customer reason for return")
    admin_notes = models.TextField(blank=True, help_text="Internal notes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return RMA-{self.id} for Order {self.order.id}"
