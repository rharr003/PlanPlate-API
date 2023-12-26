from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser


# create new user and return token
@api_view(['POST'])
def signup(request):
    # prevent superuser from being created externally
    request.data['is_superuser'] = False
    request.data["is_staff"] = False
    serializer = UserSerializer(data=request.data)
    if(serializer.is_valid()):
        user = serializer.save()
        # the serializer doesnt salt and hash the password properly so we have to reset it here
        user.set_password(serializer.validated_data["password"])
        #save the user to db after salting and hashing password
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key})
    return Response(status=400)



# fetch user info for use on front end after authentication
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    # get user id from token
    user_id = Token.objects.get(key=request.auth.key).user_id
    # use user id to create and serialize a user object to return to the front end
    user = User.objects.get(pk=user_id)
    serializer = UserSerializer(user)
    return Response(serializer.data)

    