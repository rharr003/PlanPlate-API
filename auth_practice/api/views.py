from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.middleware.csrf import get_token
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


# Create your views here.

# class SignUp(generics.CreateAPIView):
#     serializer_class = UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if(serializer.is_valid()):
        user = User.objects.create_user(**request.data)
        token = Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response("hello world")
@api_view(["GET"])
def get_cookie(request):
        token = get_token(request)
        return Response(token)
    