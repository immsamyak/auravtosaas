from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from decimal import Decimal

from apps.brands.models import Brand

class Category(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='categories', help_text='Null = platform-wide default')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subcategories')
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.parent.name} > {self.name}" if self.parent else self.name

class ProductType(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='product_types', help_text='Null = platform-wide default')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='colors', help_text='Null = platform-wide default')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    hex_code = models.CharField(validators=[RegexValidator(regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", message="Invalid hex code.")], max_length=7, help_text="#RRGGBB")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Size(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='sizes', help_text='Null = platform-wide default')
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10, unique=True)
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class StyleTag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    OCCASION_CHOICES = [
        ('CASUAL', 'Casual'),
        ('FORMAL', 'Formal'),
        ('WEDDING', 'Wedding'),
        ('PARTY', 'Party'),
        ('OFFICE', 'Office'),
        ('TRAVEL', 'Travel'),
        ('ACTIVEWEAR', 'Activewear'),
    ]

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.SET_NULL, null=True)
    
    occasion = models.CharField(max_length=50, choices=OCCASION_CHOICES, blank=True, null=True)
    style_tags = models.ManyToManyField(StyleTag, blank=True, related_name='products')
    
    # Pricing is now independent of hardcoded USD references
    price = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_vto_ready = models.BooleanField(default=False)
    
    # SEO Settings
    seo_title = models.CharField(max_length=150, blank=True, null=True, help_text="Product SEO Title (max 150 chars)")
    seo_description = models.TextField(blank=True, null=True, help_text="Product SEO Meta Description")
    seo_keywords = models.CharField(max_length=255, blank=True, null=True, help_text="Comma separated keywords")
    seo_og_image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])], upload_to='product_seo/', blank=True, null=True, help_text="OpenGraph Image for social sharing")
    
    created_at = models.DateTimeField(auto_now_add=True)


    def clean(self):
        super().clean()
        if self.category and self.category.brand and self.brand != self.category.brand:
            raise ValidationError({'category': 'Category must belong to the same brand.'})
        if self.product_type and self.product_type.brand and self.brand != self.product_type.brand:
            raise ValidationError({'product_type': 'Product type must belong to the same brand.'})

    def __str__(self):
        return f"{self.brand.name} - {self.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='product_images/')
    is_primary = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-is_primary']

    def __str__(self):
        return f"Image for {self.product.name}"

class ProductModelImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='model_images')
    image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='product_model_images/')
    description = models.CharField(max_length=255, blank=True, null=True, help_text="e.g., Professional model wearing the product")
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"Model Image for {self.product.name}"

class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.RESTRICT)
    size = models.ForeignKey(Size, on_delete=models.RESTRICT)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='product_images/')
    
    @property
    def total_stock(self):
        return sum(sl.quantity for sl in self.stock_levels.all())

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.product.slug or self.product.name}-{self.color.name}-{self.size.code}")
            # Ensure uniqueness
            unique_slug = base_slug
            counter = 1
            while ProductVariant.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.color.name} ({self.size.code})"

class ProductAIProfile(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Validation/Processing'),
        ('COMPLETED', 'AI Ready'),
        ('FAILED', 'Processing Failed'),
    ]

    product_variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name='ai_profile')
    item_type = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., top, bottom, full_body")
    fit_type = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., slim, regular, oversized")
    material = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., cotton, denim, leather")
    
    processed_asset = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='products/ai_assets/processed/', blank=True, null=True)
    processing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    
    ai_metadata = models.JSONField(blank=True, null=True, default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"AI Profile for {self.product_variant}"

class SizeChart(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='size_charts')
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.brand.name} - {self.product_type.name} Chart"

class SizeChartRule(models.Model):
    size_chart = models.ForeignKey(SizeChart, on_delete=models.CASCADE, related_name='rules')
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    min_chest_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    max_chest_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    min_waist_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    max_waist_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    
    def __str__(self):
        return f"{self.size_chart.name}: {self.size.code}"


class Collection(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='collections/', blank=True, null=True)
    products = models.ManyToManyField(Product, related_name='collections', blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('brand', 'slug')
        
    def __str__(self):
        return f"{self.name} ({self.brand.name})"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user_name = models.CharField(max_length=100, default='Anonymous')
    rating = models.IntegerField(default=5)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.rating} Stars for {self.product.name} by {self.user_name}"
