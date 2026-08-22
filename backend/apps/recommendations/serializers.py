from rest_framework import serializers
from .models import SizeRecommendation
from apps.accounts.serializers import UserSerializer
from apps.catalog.serializers import ProductSerializer

class SizeRecommendationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = SizeRecommendation
        fields = ['id', 'user', 'product', 'recommended_size', 'fit_type', 'created_at']
