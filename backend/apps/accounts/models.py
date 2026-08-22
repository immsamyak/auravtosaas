from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.contrib.auth.models import User

class ConsumerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(validators=[RegexValidator(regex=r"^\+?1?\d{9,15}$", message="Invalid phone format.")], max_length=20, blank=True, null=True, db_index=True, help_text="Used for POS global lookup")
    skin_tone_category = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Autumn, Winter")
    shoulder_width_cm = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    chest_cm = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    waist_cm = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    
    # Store Credit (from gift card redemptions, refunds, etc.)
    store_credit = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), help_text="Available store credit balance")
    
    # B2B / Wholesale
    is_b2b = models.BooleanField(default=False, help_text="Mark as a B2B / wholesale customer")
    company_name = models.CharField(max_length=200, blank=True, help_text="Company name for B2B customers")
    tax_id = models.CharField(max_length=50, blank=True, help_text="Tax / VAT registration number")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class UserPhotoProfile(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Validation'),
        ('VALID', 'Valid for Try-On'),
        ('INVALID', 'Invalid/Poor Quality'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_profiles', null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    original_photo = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='users/photo_profiles/original/')
    processed_photo = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='users/photo_profiles/processed/', blank=True, null=True)
    segmentation_mask = models.ImageField(validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp', 'svg'])], upload_to='users/photo_profiles/masks/', blank=True, null=True)
    
    processing_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    is_default = models.BooleanField(default=False)
    
    # Store pose, lighting, body analysis metrics here
    analysis_metadata = models.JSONField(blank=True, null=True, default=dict)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_default:
            # Unset any existing default photo profiles for this user or session
            if self.user:
                UserPhotoProfile.objects.filter(user=self.user, is_default=True).update(is_default=False)
            elif self.session_key:
                UserPhotoProfile.objects.filter(session_key=self.session_key, is_default=True).update(is_default=False)
        super().save(*args, **kwargs)

    def __str__(self):
        owner = self.user.username if self.user else f"Guest ({self.session_key})"
        return f"Photo Profile for {owner} ({self.processing_status})"

import random
from django.utils import timezone
from datetime import timedelta

class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    @classmethod
    def generate_otp(cls, user):
        import secrets
        # Invalidate old OTPs for this user
        cls.objects.filter(user=user, is_used=False).update(is_used=True)
        # Generate cryptographically secure 6-digit OTP
        code = str(secrets.randbelow(900000) + 100000)
        return cls.objects.create(user=user, otp_code=code)

    def is_valid(self):
        # Valid for 15 minutes
        expiration_time = self.created_at + timedelta(minutes=15)
        return not self.is_used and timezone.now() <= expiration_time

    def __str__(self):
        return f"OTP for {self.user.username}"
