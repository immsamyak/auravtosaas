from rest_framework import serializers
from .models import Brand
from apps.accounts.serializers import UserSerializer

class BrandSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = Brand
        fields = ['id', 'owner', 'name', 'slug', 'contact_email', 'logo', 'created_at']
