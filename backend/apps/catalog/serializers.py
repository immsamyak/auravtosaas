from rest_framework import serializers
from .models import Product, ProductVariant, ProductAIProfile
from apps.brands.serializers import BrandSerializer

class ProductAIProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAIProfile
        fields = '__all__'

class ProductVariantSerializer(serializers.ModelSerializer):
    stock = serializers.IntegerField(source='total_stock', read_only=True)
    ai_profile = ProductAIProfileSerializer(read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'color', 'size', 'stock', 'image', 'ai_profile']

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'brand', 'name', 'slug', 'description', 'category', 'product_type', 'price', 'is_vto_ready', 'created_at', 'variants']
