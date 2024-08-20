from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import FoodServing
from api.models import CustomUser
from .serializers import FoodServingSerializer
from meals.models import Meal

@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def food_serving(request):
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = CustomUser.objects.get(pk=user_id)
    if request.method == "GET":
        food_servings = FoodServing.objects.filter(owner=user)
        serializer = FoodServingSerializer(food_servings, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # make it so that the owner id is passed to the serializer
        data = {key: value for key, value in request.data.items()}
        data["owner_id"] = user_id
        serializer = FoodServingSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"message": "successfully added food serving", "food_serving": serializer.data}, status=200)
        return Response({"message": "missing required keys for creating food serving or food_item_id does not exist. Ensure that you include an object with the following keys: food_item_id: [int], serving_multiple: [float] and that the food_item_id exists"}, status=400)
    try:
        food_serving_id = request.data["food_serving_id"]
        food_serving = get_object_or_404(FoodServing, pk=food_serving_id)
        has_permission = food_serving.owner.id == user.id or user.is_staff
        if not has_permission:
            return Response({"message": "You can only edit food_servings you are the owner of"}, status=401)
        if request.method == "DELETE":
            food_serving.delete()
            return Response({"message": f"Successfully deleted food_serving with id of {food_serving_id}"},  status=204)
        elif request.method == "PUT":
            try:
                new_serving_size = float(request.data['serving_multiple'])
                updated_serving = food_serving.update_serving_size(new_serving_size)
                serializer = FoodServingSerializer(updated_serving)
                return Response({"message": f"Successfully updated food_serving with id of {updated_serving.id}", "updated_item": serializer.data}, status=200)
            except (KeyError, TypeError):
                return Response({"message": "Ensure valid key serving_multiple is supplied with value that can be parsed to float"}, status=400)
            
    except KeyError:
        return Response ({"message": "Ensure that you include a food_serving_id key in the request body"}, status=400)
        
    

        