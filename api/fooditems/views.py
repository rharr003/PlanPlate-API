from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import FoodItem
from api.models import CustomUser
from .serializers import FoodItemSerializer

@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def food_item(request):
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = CustomUser.objects.get(pk=user_id)
    if request.method == "GET":
        food_items = FoodItem.objects.filter(owner=user).order_by("name")
        serializer = FoodItemSerializer(food_items, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        # make it so that the owner id is passed to the serializer
        data = {key: value for key, value in request.data.items()}
        data["owner_id"] = user_id
        serializer = FoodItemSerializer(data=data)
        if(serializer.is_valid()):
            serializer.save()
            return Response({"message": "successfully added food item", "data": serializer.data}, status=200)
        return Response({"message": "missing required keys for creating food item. Ensure that you include and object with the following keys { name: [string], base_serving_size: [float], base_serving_size_unit: [string], calories: [integer], fat: [float], carbohydrates: [float], and protein: [float]"}, status=400)
    try:
        food_item_id = request.data["food_item_id"]
        food_item = get_object_or_404(FoodItem, pk=food_item_id)
        has_permission = food_item.owner.id == user.id or user.is_staff
        if not has_permission:
            return Response({"message": "You can only edit food_items you are the owner of"}, status=401)
        if request.method == "DELETE":
            food_item.delete()
            return Response({"message": f"Successfully deleted {food_item.name}"},  status=204)
        elif request.method == "PUT":
            serializer = FoodItemSerializer(food_item)
            data = {key: value for key, value in request.data.items() if key in serializer.data}
            if len(data) < 1:
                return Response({"message": "Ensure valid keys for update are supplied"}, status=400)
            updated_item = food_item.update(data)
            updated_serializer = FoodItemSerializer(updated_item)
            return Response({"message": f"Successfully Updated {food_item.name}", "updated_item": updated_serializer.data}, status=200)
    except KeyError: 
        return Response({"message": "Ensure that you include a food_item_id key in the request body"}, status=400)
        
