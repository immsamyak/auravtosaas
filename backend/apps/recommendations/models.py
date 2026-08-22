from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from django.contrib.auth.models import User
from apps.catalog.models import Product

class SizeRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='size_recommendations')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='size_recommendations')
    recommended_size = models.CharField(max_length=10)
    fit_type = models.CharField(max_length=50, help_text="e.g., True to Size, Runs Small")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}: {self.recommended_size} ({self.fit_type})"
