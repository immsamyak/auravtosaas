from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.brands.models import Brand

class SystemSetting(models.Model):
    CATEGORY_CHOICES = [
        ('GENERAL', 'General'),
        ('AI', 'Artificial Intelligence'),
        ('MEDIA', 'Media & Uploads'),
        ('RECOMMENDATION', 'Recommendations'),
    ]
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='GENERAL')
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"

class FeatureFlag(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g., virtual_try_on")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {'Enabled' if self.is_active else 'Disabled'}"

class BrandSetting(models.Model):
    brand = models.OneToOneField(Brand, on_delete=models.CASCADE, related_name='settings')
    currency = models.CharField(max_length=10, default='USD')
    tax_rate = models.DecimalField(validators=[MinValueValidator(Decimal('0.00'))], max_digits=5, decimal_places=2, default=0.00, help_text="Percentage (e.g., 13.00 for 13%)")
    contact_email = models.EmailField(blank=True, null=True)
    logo = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='brand_logos/', blank=True, null=True)
    primary_color = models.CharField(validators=[RegexValidator(regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", message="Invalid hex code.")], max_length=7, default='#000000', help_text="Hex color code")
    
    # Store Display Features
    google_review_url = models.URLField(blank=True, null=True, help_text="Direct link for Google Reviews")
    wifi_network_name = models.CharField(max_length=100, blank=True, null=True, help_text="WiFi SSID for store")
    wifi_password = models.CharField(max_length=100, blank=True, null=True)
    pos_thermal_paper_size = models.CharField(max_length=20, default='80mm', help_text="e.g. 58mm, 80mm")
    
    # Billing & Legal
    tax_id_type = models.CharField(max_length=20, blank=True, null=True, help_text="e.g. PAN, VAT, GST")
    tax_id_number = models.CharField(max_length=50, blank=True, null=True)
    show_tax_on_receipt = models.BooleanField(default=True, help_text="Display Tax/PAN on printed receipts and customer display")
    
    def __str__(self):
        return f"Settings for {self.brand.name}"

class LandingPageConfig(models.Model):
    """Singleton model for SaaS landing page configuration"""
    # Hero Section
    hero_headline = models.CharField(max_length=255, default="The ultimate AI fitting room for modern fashion brands")
    hero_subheadline = models.TextField(default="Stop dealing with returns due to poor sizing. Aura uses state-of-the-art Generative AI and Computer Vision to let your customers try on your entire catalog virtually.")
    hero_primary_cta = models.CharField(max_length=50, default="Start your Store")
    hero_secondary_cta = models.CharField(max_length=50, default="Brand Login")
    
    # Demo Section
    demo_title = models.CharField(max_length=255, default="Experience it live")
    demo_subtitle = models.CharField(max_length=255, default="Trusted Brands")
    
    # Footer Section
    footer_text = models.CharField(max_length=255, default="© 2026 Aura Virtual Try-On. All rights reserved.")
    
    # Features Section
    features_title = models.CharField(max_length=255, default="Why choose Aura")
    features_subtitle = models.CharField(max_length=255, default="Everything you need to run a successful virtual fitting room.")
    
    # Testimonials Section
    testimonials_title = models.CharField(max_length=255, default="What our clients say")
    testimonials_subtitle = models.CharField(max_length=255, default="Trusted by leading fashion brands worldwide.")
    
    # Blog Section
    blog_title = models.CharField(max_length=255, default="Latest from our blog")
    blog_subtitle = models.CharField(max_length=255, default="News, tips, and insights about fashion tech.")
    
    # Contact Section
    contact_title = models.CharField(max_length=255, default="Get in touch")
    contact_subtitle = models.CharField(max_length=255, default="We'd love to hear from you.")
    contact_email = models.EmailField(default="contact@auravto.com")
    contact_phone = models.CharField(max_length=50, default="+1 (555) 123-4567")
    contact_address = models.CharField(max_length=255, default="123 Fashion Ave, NY 10001")
    
    # Social Links
    social_twitter = models.URLField(blank=True, null=True, help_text="X/Twitter Profile URL")
    social_instagram = models.URLField(blank=True, null=True, help_text="Instagram Profile URL")
    social_linkedin = models.URLField(blank=True, null=True, help_text="LinkedIn Page URL")
    social_facebook = models.URLField(blank=True, null=True, help_text="Facebook Page URL")
    
    # FAQ Section
    faq_title = models.CharField(max_length=255, default="Frequently Asked Questions")
    faq_subtitle = models.CharField(max_length=255, default="Everything you need to know about Aura.")
    
    # Final CTA Section
    cta_title = models.CharField(max_length=255, default="Ready to transform your store?")
    cta_subtitle = models.CharField(max_length=255, default="Join the top fashion brands using Aura to reduce returns and increase conversion.")
    cta_button_text = models.CharField(max_length=50, default="Start your free trial")
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Landing Page Config"
        verbose_name_plural = "Landing Page Configs"

    def __str__(self):
        return "Active SaaS Landing Page Configuration"

class FAQItem(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['display_order', '-created_at']
        verbose_name = "FAQ Item"
        verbose_name_plural = "FAQ Items"

    def __str__(self):
        return self.question

class LandingPageFeature(models.Model):
    AUDIENCE_CHOICES = [
        ('BRAND', 'Brand Owners'),
        ('SHOPPER', 'Shoppers / End Users'),
    ]
    
    config = models.ForeignKey(LandingPageConfig, on_delete=models.CASCADE, related_name='features')
    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)
    icon_class = models.CharField(max_length=100, help_text="FontAwesome class e.g., 'fa-solid fa-chart-line'")
    title = models.CharField(max_length=150)
    description = models.TextField()
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['audience', 'display_order']
        
    def __str__(self):
        return f"[{self.get_audience_display()}] {self.title}"

class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField(help_text="HTML content for the page")
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FooterSection(models.Model):
    title = models.CharField(max_length=100)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return self.title

class FooterLink(models.Model):
    section = models.ForeignKey(FooterSection, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.SET_NULL, null=True, blank=True, help_text="Link to an internal CMS page")
    external_url = models.URLField(blank=True, null=True, help_text="Or provide an external URL (e.g. https://twitter.com)")
    show_new_badge = models.BooleanField(default=False)
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order']

    def __str__(self):
        return f"{self.section.title} > {self.title}"

class GlobalSettings(models.Model):
    # General
    site_name = models.CharField(max_length=100, default='AURA.')
    support_email = models.EmailField(default='support@aura.com')
    site_logo = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='site/', blank=True, null=True)
    site_favicon = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='site/', blank=True, null=True)
    
    # Branding
    primary_color = models.CharField(validators=[RegexValidator(regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", message="Invalid hex code.")], max_length=20, default='#4f46e5', help_text="Hex code (e.g., #4f46e5)")
    secondary_color = models.CharField(validators=[RegexValidator(regex=r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", message="Invalid hex code.")], max_length=20, default='#1e293b', help_text="Hex code (e.g., #1e293b)")
    currency = models.CharField(max_length=10, default='USD')
    currency_symbol = models.CharField(max_length=10, default='$')
    
    # Virtual Try-On (VTO)
    class VTOEngine(models.TextChoices):
        LOCAL = 'local', 'Local API (ComfyUI / Stable Diffusion)'
        REPLICATE = 'replicate', 'Cloud API: Replicate'
        HUGGINGFACE = 'huggingface', 'Cloud API: Hugging Face Spaces'
        
    vto_engine = models.CharField(
        max_length=20,
        choices=VTOEngine.choices,
        default=VTOEngine.LOCAL,
        help_text="Select which AI engine to use for Virtual Try-On."
    )
    
    # Replicate Config
    replicate_api_key = models.CharField(max_length=255, blank=True, null=True, help_text="Required if using Replicate API")
    replicate_model_version = models.CharField(max_length=255, default='cuuupid/idm-vton', help_text="e.g. cuuupid/idm-vton")
    
    # Hugging Face Config
    hf_space_id = models.CharField(max_length=255, blank=True, null=True, default='fashn-ai/fashn-vton-1.5', help_text="e.g. fashn-ai/fashn-vton-1.5 or your duplicated space ID")
    hf_api_token = models.CharField(max_length=255, blank=True, null=True, help_text="Your Hugging Face Access Token (Required if space is private or duplicated)")
    
    
    # SMTP
    smtp_host = models.CharField(max_length=255, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=255, blank=True)
    smtp_password = models.CharField(max_length=255, blank=True)
    
    # Payments (Stripe)
    stripe_environment = models.CharField(max_length=10, choices=[('TEST', 'Stripe Test Mode'), ('LIVE', 'Stripe Live Mode')], default='TEST', help_text="Toggle between Test Mode and Live Production Mode.")
    
    stripe_test_public_key = models.CharField(max_length=255, blank=True)
    stripe_test_secret_key = models.CharField(max_length=255, blank=True)
    stripe_test_webhook_secret = models.CharField(max_length=255, blank=True)
    
    stripe_live_public_key = models.CharField(max_length=255, blank=True)
    stripe_live_secret_key = models.CharField(max_length=255, blank=True)
    stripe_live_webhook_secret = models.CharField(max_length=255, blank=True)

    @property
    def get_stripe_public_key(self):
        return self.stripe_live_public_key if self.stripe_environment == 'LIVE' else self.stripe_test_public_key

    @property
    def get_stripe_secret_key(self):
        return self.stripe_live_secret_key if self.stripe_environment == 'LIVE' else self.stripe_test_secret_key

    @property
    def get_stripe_webhook_secret(self):
        return self.stripe_live_webhook_secret if self.stripe_environment == 'LIVE' else self.stripe_test_webhook_secret
    
    # SMS (Twilio)
    twilio_account_sid = models.CharField(max_length=255, blank=True)
    twilio_auth_token = models.CharField(max_length=255, blank=True)
    twilio_sender_number = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = "Platform Setting"
        verbose_name_plural = "Platform Settings"

    def save(self, *args, **kwargs):
        self.pk = 1 # Singleton
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Global Platform Settings"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, default='Customer', help_text="e.g., CEO at Fashion Brand")
    content = models.TextField()
    avatar = models.ImageField(upload_to='testimonials/', blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    rating = models.IntegerField(default=5, help_text="1 to 5 stars")
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order', '-created_at']

    def __str__(self):
        return f"{self.name} - {self.role}"

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    content = models.TextField()
    excerpt = models.TextField(blank=True, help_text="Short description for the blog listing page")
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True, validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])])
    author_name = models.CharField(max_length=100, default="Aura Team")
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

class PlatformIntegration(models.Model):
    CATEGORY_CHOICES = [
        ('PAYMENT', 'Payments'),
        ('SHIPPING', 'Shipping & Logistics'),
        ('MARKETING', 'Marketing & Analytics'),
        ('OTHER', 'Other Add-ons')
    ]
    
    name = models.CharField(max_length=100)
    provider_code = models.CharField(max_length=50, unique=True, help_text="e.g. ESEWA, KHALTI, PATHAO")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    
    # UI configuration
    logo = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='integrations/', blank=True, null=True, help_text="Upload logo for the integration")
    
    # State
    is_active_globally = models.BooleanField(default=True, help_text="Turn off to disable this integration for all stores")
    requires_merchant_id = models.BooleanField(default=False)
    requires_api_key = models.BooleanField(default=False)
    requires_api_secret = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

class Notification(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    action_url = models.CharField(max_length=255, blank=True, null=True)
    icon_class = models.CharField(max_length=50, default="fa-solid fa-bell", help_text="FontAwesome icon class")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.title}"

class SystemAuditLog(models.Model):
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('OTHER', 'Other')
    ]
    
    actor = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.CharField(max_length=255, blank=True, null=True)
    object_repr = models.CharField(max_length=255, blank=True, null=True)
    
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    
    payload = models.JSONField(blank=True, null=True, help_text="Stored data changes or relevant metadata")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "System Audit Log"
        verbose_name_plural = "System Audit Logs"
        
    def __str__(self):
        actor_name = self.actor.username if self.actor else "System/Anonymous"
        return f"[{self.created_at.strftime('%Y-%m-%d %H:%M:%S')}] {actor_name} {self.action} {self.model_name} ({self.object_id})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
