from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ConsumerProfile, UserPhotoProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ConsumerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = ConsumerProfile
        fields = ['id', 'user', 'skin_tone_category', 'shoulder_width_cm', 'waist_cm']

class UserPhotoProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPhotoProfile
        fields = '__all__'
