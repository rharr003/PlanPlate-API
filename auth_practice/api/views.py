from rest_framework.response import Response
from .serializers import UserSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from django.shortcuts import get_object_or_404


# create new user and return token
@api_view(['POST'])
def signup(request):
    # prevent superuser from being created externally
    request.data['is_superuser'] = True
    request.data["is_staff"] = True
    serializer = UserSerializer(data=request.data)
    if(serializer.is_valid()):
        user = serializer.save()
        # the serializer doesnt salt and hash the password properly so we have to reset it here
        user.set_password(serializer.validated_data["password"])
        #save the user to db after salting and hashing password
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token": token.key}, status=200)
    return Response(status=400)



# fetch user info for use on front end after authentication
@api_view(["GET", "DELETE", "PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_detail(request):   
    # get user id from token
    user_id = Token.objects.get(key=request.auth.key).user_id
    # use user id to create and serialize a user object to return to the front end
    user = CustomUser.objects.get(pk=user_id)
    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
    else:
        try: 
            user_for_update = get_object_or_404(CustomUser, pk=request.data['user_id'])
            serializer = UserSerializer(user_for_update)
        except KeyError: 
            return Response("must supply user_id key in request body", status=400)
        #django rest framework does not support checking object level permissions in functional views so we have to manually check here 
        has_permission = user.is_staff or user_id == user_for_update.id
        if not has_permission:
            return Response("Not authorized", status=401)  
        elif request.method == "DELETE":
            user_for_update.delete()
            return Response(f"Deleted {user_for_update.username}", status=204)
        elif request.method == "PUT":
            #ensures only valid keys are set will ignore invalid keys
            restricted_keys = ["id", "is_superuser", "is_staff"]
            keys = {key: value for key, value in request.data.items() if key in serializer.data and key not in restricted_keys}
            if len(keys.items()) < 1:
                return Response("Must supply valid fields for update in request", status=400)
            user_for_update.update(keys)
            return Response(f"Succesfully changed {' ,'.join(keys)} for user {user_for_update.username}", status=200)

        

            

   
    
       
       
        


    