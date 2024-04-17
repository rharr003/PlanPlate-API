from rest_framework import serializers
from .models import CustomUser
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "last_login", "password", "email", "is_superuser", "is_staff", "weight", "weight_format", "height", "height_format", "date_of_birth"]
        extra_kwargs = {'password': {'write_only': True}}
        
      
      