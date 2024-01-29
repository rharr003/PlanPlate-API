from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Meal
from api.models import CustomUser
from .serializers import MealSerializer
from foodserving.models import FoodServing, MealOrder
from django.db.models import Q


@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def meal(request):
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = CustomUser.objects.get(pk=user_id)
    if request.method == "GET":
        meals = Meal.objects.filter(owner=user)
        serializer = MealSerializer(meals, many=True)
        return Response(serializer.data)
    try:
        if request.method == "POST":
            request.data['owner_id'] = user_id
            serializer = MealSerializer(data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "succesfully added meal"}, status=200)
            return Response({"message": "missing required keys for creating meal. Ensure that you include an object with the following keys: name: [str], type: ['meal' or 'snack']"}, status =400)
        meal_to_edit = get_object_or_404(Meal, pk=request.data['meal_id'])
        has_permission = meal_to_edit.owner.id == user.id or user.is_staff
        if not has_permission:
            return Response({"message": "You can only edit meals you are the owner of"}, status=401)
        if request.method == "DELETE":
            meal_to_edit.delete()
            return Response({"message": "successfully deleted meal"})
        elif request.method == "PUT":
            serializer = MealSerializer(meal_to_edit)
            data = {key: value for key, value in request.data.items() if key in serializer.data}
            updated_meal = meal_to_edit.update(data)
            updated_serializer = MealSerializer(updated_meal)
            return Response({"message": f"Successfully Updated {meal_to_edit.name}", "updated_meal": updated_serializer.data}, status=200)      
    except KeyError:
        return Response({"message": "Missing some required keys in the request body. Check your code and try again"}, status=400)
    
    

@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def meal_detail(request, meal_id): 
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = CustomUser.objects.get(pk=user_id)
    meal = get_object_or_404(Meal, pk=meal_id)
    has_permission = meal.owner.id == user.id or user.is_staff
    if not has_permission:
        return Response({"message": "You can only access meals you are the owner of"}, status=401)
    if request.method == "GET":
        serializer = MealSerializer(meal)
        return Response(serializer.data)   
    try:
        if request.method == "POST":
            food_serving = get_object_or_404(FoodServing, pk=request.data['food_serving_id'])
            if len(meal.foodserving_set.filter(id=food_serving.id)) > 0:
                return Response({"message": "This serving already exists on this meal consider increasing the quantity on existing serving"}, status=400)
            servings_to_be_adjusted = MealOrder.objects.filter(meal=meal).filter(index__gte=request.data['index'])
            for serving in servings_to_be_adjusted:
                serving.update_index(1)
            meal.foodserving_set.add(food_serving, through_defaults={'index': request.data['index']})

            return Response({"message": "successfully added new serving to meal"}, status=200)
        if request.method == "DELETE":
            try:
                serving_to_delete = MealOrder.objects.filter(Q(index=request.data['index'])&Q(meal_id=meal_id))
                serving_to_delete.delete()
                servings_to_be_adjusted = MealOrder.objects.filter(meal=meal).filter(index__gt=request.data['index'])
                for serving in servings_to_be_adjusted:
                    serving.update_index(-1)
                return Response({"message": "Successfully deleted the serving requested"}, status=204)
            
            except MealOrder.DoesNotExist:
                return Response({"message": "no serving found on meal at index provided. double check your meal id and index and try again"}, status=400)
        elif request.method == "PUT":
            index1 = request.data['index']
            index2 = request.data['index2']
            serving1 = MealOrder.objects.filter(Q(index=index1)&Q(meal_id=meal_id))[0]
            serving2 = MealOrder.objects.filter(Q(index=index2)&Q(meal_id=meal_id))[0]
            serving1.set_index(index2)
            serving2.set_index(index1)
            serializer = MealSerializer(meal)
            return Response({"message": "Successfully updated serving order on meal", "updated_meal": serializer.data}, status=200)
          
                
            
            
            
    except KeyError:
        return Response({"message": "please supply object with the following keys in request: food_serving_id: [int], index: [int0], (index2: [int0] **only for PUT requests)"}, status=400)
                
