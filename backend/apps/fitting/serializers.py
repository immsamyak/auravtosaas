from rest_framework import serializers
from .models import VirtualTryOn
from apps.accounts.serializers import UserSerializer
from apps.catalog.serializers import ProductVariantSerializer

class VirtualTryOnSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product_variant = ProductVariantSerializer(read_only=True)
    
    class Meta:
        model = VirtualTryOn
        fields = ['id', 'user', 'photo_profile', 'product_variant', 'selected_size', 'generated_image', 'status', 'provider', 'error_message', 'processing_started_at', 'processing_completed_at', 'created_at', 'updated_at', 'ai_confidence_score']
