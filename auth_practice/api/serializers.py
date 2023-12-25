from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "last_login" ]
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        print(validated_data)
        print(repr(self))
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return {"token": token.key, "user": user}
        
      
      