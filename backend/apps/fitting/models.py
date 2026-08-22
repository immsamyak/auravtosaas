from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.contrib.auth.models import User
from apps.catalog.models import ProductVariant, Size

class FitPassport(models.Model):
    SHAPE_CHOICES = [
        ('HOURGLASS', 'Hourglass'),
        ('PEAR', 'Pear'),
        ('APPLE', 'Apple'),
        ('RECTANGLE', 'Rectangle'),
        ('INVERTED_TRIANGLE', 'Inverted Triangle'),
    ]
    FIT_CHOICES = [
        ('TIGHT', 'Tight Fit'),
        ('REGULAR', 'Regular Fit'),
        ('LOOSE', 'Loose/Oversized Fit'),
    ]
    GENDER_CHOICES = [
        ('MASCULINE', 'Masculine'),
        ('FEMININE', 'Feminine'),
        ('ANDROGYNOUS', 'Androgynous'),
        ('NEUTRAL', 'Neutral'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fit_passport', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    
    height_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    weight_kg = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    body_shape = models.CharField(max_length=20, choices=SHAPE_CHOICES, null=True, blank=True)
    fit_preference = models.CharField(max_length=20, choices=FIT_CHOICES, default='REGULAR')
    gender_preference = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    
    chest_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    waist_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    hips_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    inseam_cm = models.FloatField(validators=[MinValueValidator(0.0)], null=True, blank=True)
    
    # GDPR / Privacy Consent
    consent_given = models.BooleanField(default=False, help_text="User has consented to body data processing for virtual try-on")
    consent_given_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when consent was granted")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        owner = self.user.username if self.user else f"Guest ({self.session_key})"
        return f"Fit Passport: {owner}"


class VTOPhotoVault(models.Model):
    POSE_CHOICES = [
        ('FRONT', 'Front'),
        ('SIDE', 'Side'),
        ('FULL', 'Full Body'),
    ]

    passport = models.ForeignKey(FitPassport, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='vto/vault/')
    pose_type = models.CharField(max_length=10, choices=POSE_CHOICES, default='FRONT')
    is_default = models.BooleanField(default=False)
    
    quality_score = models.FloatField(help_text="0.0 to 1.0", null=True, blank=True)
    validation_metadata = models.JSONField(default=dict, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            VTOPhotoVault.objects.filter(passport=self.passport, pose_type=self.pose_type).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passport} - {self.pose_type} Photo"


class VTOProductAssets(models.Model):
    ASSET_TYPE_CHOICES = [
        ('FLAT_LAY', 'Flat Lay'),
        ('GHOST_MANNEQUIN', 'Ghost Mannequin'),
        ('MASK', 'Mask'),
    ]

    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='vto_assets')
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPE_CHOICES)
    image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='vto/product_assets/')
    
    readiness_status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_variant} - {self.asset_type}"


class VTOSession(models.Model):
    passport = models.ForeignKey(FitPassport, on_delete=models.CASCADE, related_name='vto_sessions')
    status = models.CharField(max_length=20, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.id} for {self.passport}"


class VirtualTryOn(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VALIDATING', 'Validating Inputs'),
        ('ANALYZING', 'Analyzing Photos'),
        ('PROCESSING', 'Processing Generation'),
        ('COMPLETED', 'Completed Successfully'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    progress_percent = models.IntegerField(default=0, help_text="Real-time generation progress 0-100")

    PROVIDER_CHOICES = [
        ('MOCK', 'Mock Provider'),
        ('STABLE_DIFFUSION', 'Stable Diffusion API'),
        ('TRYON_DIFFUSION', 'TryOn Diffusion Engine'),
    ]

    session = models.ForeignKey(VTOSession, on_delete=models.CASCADE, related_name='try_ons', null=True)
    base_photo = models.ForeignKey(VTOPhotoVault, on_delete=models.SET_NULL, null=True, related_name='try_ons')
    
    # Keeping these for backward compatibility, but ideally they'd move to a VTOProduct model
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.PROTECT, related_name='try_ons')
    selected_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    
    generated_image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='tryons/outputs/', blank=True, null=True)
    ai_confidence_score = models.FloatField(help_text="0.0 to 1.0", blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    provider = models.CharField(max_length=50, choices=PROVIDER_CHOICES, default='TRYON_DIFFUSION')
    
    error_message = models.TextField(blank=True, null=True)
    
    processing_started_at = models.DateTimeField(blank=True, null=True)
    processing_completed_at = models.DateTimeField(blank=True, null=True)
    
    # QA Moderation
    QA_STATUS_CHOICES = [
        ('UNREVIEWED', 'Unreviewed'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('FLAGGED', 'Flagged for Review'),
    ]
    qa_status = models.CharField(max_length=20, choices=QA_STATUS_CHOICES, default='UNREVIEWED')
    qa_reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_tryons')
    qa_reviewed_at = models.DateTimeField(null=True, blank=True)
    qa_notes = models.TextField(blank=True, help_text="Internal reviewer notes")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()
        if self.status == 'COMPLETED' and not self.generated_image:
            raise ValidationError({'generated_image': 'A generated image is required when status is COMPLETED.'})
        if self.status == 'FAILED' and not self.error_message:
            raise ValidationError({'error_message': 'An error message is required when status is FAILED.'})

    def __str__(self):
        return f"Try-On: {self.product_variant} ({self.status})"


class VTOProduct(models.Model):
    """
    Allows multiple products (Top, Bottom, Shoes) to be part of a single Try-On (Outfit Builder).
    """
    PRODUCT_TYPE_CHOICES = [
        ('TOP', 'Top'),
        ('BOTTOM', 'Bottom'),
        ('SHOES', 'Shoes'),
        ('OUTERWEAR', 'Outerwear'),
        ('ACCESSORY', 'Accessory'),
    ]
    try_on = models.ForeignKey(VirtualTryOn, on_delete=models.CASCADE, related_name='products')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    selected_size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True, blank=True)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE_CHOICES, default='TOP')
    
    def __str__(self):
        return f"{self.product_type}: {self.product_variant}"


class VirtualWardrobeLook(models.Model):
    """
    Saves a completed VTO result to a user's Virtual Wardrobe.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wardrobe_looks')
    try_on = models.ForeignKey(VirtualTryOn, on_delete=models.CASCADE)
    notes = models.TextField(blank=True, null=True)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Look saved on {self.saved_at.strftime('%Y-%m-%d')} by {self.user}"

class AIAvatarModel(models.Model):
    """
    Catalog of professional AI-generated models for VTO for users who don't want to upload photos.
    """
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('NON_BINARY', 'Non-Binary'),
    ]
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    image = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='vto/avatars/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.gender})"

