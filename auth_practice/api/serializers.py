from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "last_login", "password", "email", "is_superuser", "is_staff" ]
        extra_kwargs = {'password': {'write_only': True}}
        
        
      
      