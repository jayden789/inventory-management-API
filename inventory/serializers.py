"""
Serializers for the inventory app.
"""

from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User

class ItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the Item model.
    Includes validation for the quantity field.
    """
    class Meta:
        model = Item
        fields = '__all__'

    def validate_quantity(self, value):
        """
        Validate that the quantity is a non-negative integer.
        """
        if value < 0:
            raise serializers.ValidationError("Quantity must be a non-negative integer.")
        return value

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        Create a new user with encrypted password.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
