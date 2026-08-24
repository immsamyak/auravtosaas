from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.contrib.auth.models import User

class StoreTheme(models.Model):
    name = models.CharField(max_length=100)
    business_type = models.CharField(max_length=100, help_text="e.g., Fashion & Apparel")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True, help_text="Enable or disable this theme globally")
    template_folder = models.CharField(max_length=100, help_text="Folder name in templates/storefront/ e.g., theme_fashion")
    preview_image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='theme_previews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Brand(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active Storefront'),
        ('INACTIVE', 'Inactive'),
        ('MAINTENANCE', 'Under Maintenance'),
    ]

    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owned_brand', null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=100, default='my-brand')
    contact_email = models.EmailField()
    logo = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='brand_logos/', blank=True, null=True)
    banner = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='brand_banners/', blank=True, null=True)
    
    # Hero Banner Text Settings
    banner_title = models.CharField(max_length=150, blank=True, null=True, help_text="Main heading for the storefront banner")
    banner_subtitle = models.TextField(blank=True, null=True, help_text="Subtitle or description for the banner")
    banner_cta_text = models.CharField(max_length=50, blank=True, null=True, help_text="Text for the call-to-action button (e.g. 'Shop Now')")
    banner_cta_link = models.CharField(max_length=200, blank=True, null=True, help_text="URL or section ID for the CTA (e.g. '#collection')")
    
    # Advanced Customization
    LOGO_ALIGNMENT_CHOICES = (
        ('left', 'Left'),
        ('center', 'Center'),
    )
    logo_alignment = models.CharField(max_length=10, choices=LOGO_ALIGNMENT_CHOICES, default='left', help_text="Alignment of the logo in the storefront header")
    top_announcement_text = models.CharField(max_length=200, blank=True, null=True, help_text="Text for the top announcement bar (e.g. 'Free Shipping on all orders')")
    banner_badge_text = models.CharField(max_length=50, blank=True, null=True, help_text="Small badge text in the hero section (e.g. 'Dropping Now')")
    banner_secondary_cta_text = models.CharField(max_length=50, blank=True, null=True, help_text="Text for a secondary button (e.g. 'Watch Video')")
    banner_secondary_cta_link = models.CharField(max_length=200, blank=True, null=True, help_text="URL for the secondary button")
    footer_copyright_text = models.CharField(max_length=200, blank=True, null=True, help_text="Custom copyright text for the footer")
    
    theme = models.ForeignKey(StoreTheme, on_delete=models.SET_NULL, null=True, blank=True, related_name='brands')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Store Details
    description = models.TextField(blank=True, null=True, help_text="Short description for the store footer")
    support_email = models.EmailField(blank=True, null=True)
    support_phone = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{9,15}$", message="Invalid phone format.")], max_length=50, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Social Links
    instagram_url = models.URLField(blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    tiktok_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    pinterest_url = models.URLField(blank=True, null=True)
    # Currency Override
    currency_code = models.CharField(max_length=10, blank=True, null=True, help_text="Override global currency (e.g., NPR, USD)")
    currency_symbol = models.CharField(max_length=10, blank=True, null=True, help_text="Override global symbol (e.g., Rs., $)")
    
    # B2B / Wholesale Settings
    b2b_discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))], help_text="Global B2B discount percentage for wholesale customers")
    enable_gift_cards = models.BooleanField(default=False, help_text="Enable gift card sales in this store")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def get_currency_symbol(self):
        if self.currency_symbol:
            return self.currency_symbol
        from apps.core.models import GlobalSettings
        global_settings = GlobalSettings.get_settings()
        return global_settings.currency_symbol or '$'

    @property
    def get_currency_code(self):
        if self.currency_code:
            return self.currency_code
        from apps.core.models import GlobalSettings
        global_settings = GlobalSettings.get_settings()
        return global_settings.currency or 'USD'

class BrandStaff(models.Model):
    ROLE_CHOICES = [
        ('OWNER', 'Owner'),
        ('ADMIN', 'Admin'),
        ('FULFILLMENT', 'Fulfillment & Orders'),
        ('SUPPORT', 'Customer Support'),
    ]
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='staff_members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brand_roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SUPPORT')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('brand', 'user')
        
    def __str__(self):
        return f"{self.user.username} - {self.role} at {self.brand.name}"

class MediaAsset(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='media_assets')
    file = models.FileField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg', 'pdf', 'mp4'])], upload_to='brand_media/')
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, blank=True, null=True)
    file_size = models.PositiveIntegerField(help_text="Size in bytes", default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_team(self):
        return self.staff_members.all()

class APIKey(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='api_keys')
    name = models.CharField(max_length=100)
    prefix = models.CharField(max_length=8)
    key_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.prefix}...)"

class WebhookEndpoint(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='webhooks')
    url = models.URLField()
    secret_key = models.CharField(max_length=64)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    events = models.JSONField(default=list, help_text="List of subscribed events e.g. ['order.created']")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url

class BrandIntegration(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='integrations')
    integration = models.ForeignKey('core.PlatformIntegration', on_delete=models.CASCADE, related_name='brand_configs')
    
    is_active = models.BooleanField(default=False)
    
    # Store credentials inside a JSON field
    credentials = models.JSONField(default=dict, blank=True, help_text="Store API keys, merchant IDs, etc. here")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('brand', 'integration')
        
    def __str__(self):
        return f"{self.integration.name} for {self.brand.name} - {'Active' if self.is_active else 'Inactive'}"

    @property
    def whatsapp_number(self):
        if not isinstance(self.credentials, dict):
            return ""
        return self.credentials.get('whatsapp_number') or self.credentials.get('merchant_id', '')

    @property
    def whatsapp_instructions(self):
        if not isinstance(self.credentials, dict):
            return ""
        return self.credentials.get('instructions', '')

class PopupBanner(models.Model):
    BANNER_TYPES = (
        ('TOP_BAR', 'Top Bar Banner'),
        ('BOTTOM_POPUP', 'Bottom Popup'),
        ('MODAL', 'Center Modal'),
    )
    DISPLAY_RULES = (
        ('ALL_PAGES', 'All Pages'),
        ('HOMEPAGE_ONLY', 'Homepage Only'),
        ('SPECIFIC_URL', 'Specific URL Path'),
    )
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='popup_banners')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    banner_type = models.CharField(max_length=20, choices=BANNER_TYPES, default='TOP_BAR')
    
    image = models.ImageField(upload_to='brands/marketing/popups/', blank=True, null=True)
    headline = models.CharField(max_length=255, blank=True)
    body_content = models.TextField(blank=True)
    
    cta_text = models.CharField(max_length=100, blank=True)
    cta_link = models.CharField(max_length=255, blank=True)
    open_in_new_tab = models.BooleanField(default=False)
    
    display_rule = models.CharField(max_length=20, choices=DISPLAY_RULES, default='ALL_PAGES')
    specific_url = models.CharField(max_length=255, blank=True, help_text="e.g. /shop/")
    delay_seconds = models.IntegerField(default=0, help_text="Show after this many seconds")
    
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.get_banner_type_display()} - {self.title}"

class Coupon(models.Model):
    DISCOUNT_TYPES = (
        ('PERCENTAGE', 'Percentage Discount'),
        ('FIXED', 'Fixed Amount Discount'),
    )
    CONDITIONS = (
        ('NONE', 'No Condition'),
        ('FIRST_PURCHASE', 'First Purchase Only'),
    )
    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='coupons')
    code = models.CharField(max_length=50)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES, default='PERCENTAGE')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2, help_text="Percentage or Fixed Amount")
    
    condition = models.CharField(max_length=20, choices=CONDITIONS, default='NONE')
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_uses = models.IntegerField(default=0, help_text="0 for unlimited")
    times_used = models.IntegerField(default=0)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('brand', 'code')
        
    def __str__(self):
        return f"{self.code} - {self.discount_value} {self.get_discount_type_display()}"

class NewsletterSubscriber(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='subscribers')
    email = models.EmailField()
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('brand', 'email')
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return f"{self.email} - {self.brand.name}"

class EmailCampaign(models.Model):
    STATUS_CHOICES = (
        ('DRAFT', 'Draft'),
        ('SCHEDULED', 'Scheduled'),
        ('SENT', 'Sent'),
    )
    TARGET_CHOICES = (
        ('SUBSCRIBERS', 'Newsletter Subscribers'),
        ('CUSTOMERS', 'Registered Customers'),
        ('BOTH', 'Everyone'),
    )

    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='email_campaigns')
    name = models.CharField(max_length=255, help_text="Internal name for this campaign")
    subject = models.CharField(max_length=255, help_text="Email subject line")
    
    target_audience = models.CharField(max_length=20, choices=TARGET_CHOICES, default='SUBSCRIBERS')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    
    html_content = models.TextField(help_text="HTML email content")
    
    scheduled_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"

class APILog(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='api_logs')
    api_key_prefix = models.CharField(max_length=50, blank=True)
    endpoint = models.CharField(max_length=255)
    method = models.CharField(max_length=10)
    status_code = models.IntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    latency_ms = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.method} {self.endpoint} [{self.status_code}]"
