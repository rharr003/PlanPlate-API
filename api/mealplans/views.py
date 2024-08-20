from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import MealPlan
from api.models import CustomUser
from django.db.models import Q
from meals.models import MealPlanOrder, Meal
from .serializers import MealPlanSerializer, MealPlanSerializerFull

@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def meal_plan(request):
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = CustomUser.objects.get(pk=user_id)
    if request.method == 'GET':
        all_meal_plans = MealPlan.objects.filter(owner=user).order_by("-active")
        minified_serializer = MealPlanSerializer(all_meal_plans, many=True)
        # try:
        #     current_meal_plan = MealPlan.objects.get(owner=user, active=True)
        # except MealPlan.DoesNotExist:
        #     return Response({'current': None, 'all': minified_serializer.data})
        #return more detailed data on active meal plan since it will need to be fully rendered on the front end
        # full_serializer = MealPlanSerializerFull(current_meal_plan)
        return Response({'plans': minified_serializer.data})
    try:
        if request.method == 'POST':
            print(request.data)
            request.data['owner_id'] = user_id
            serializer = MealPlanSerializer(data=request.data)
            if serializer.is_valid():
                if request.data["active"]:
                    try:
                        meal_to_deactivate = MealPlan.objects.get(owner=user, active=True)
                        meal_to_deactivate.deactivate()
                    except MealPlan.DoesNotExist:
                        pass
                serializer.save()
                #Only 1 active meal allowed at a time this just tells the api which meal plan to fetch the full data for on a get request.
                return Response({"message": "Successfully created meal plan", "meal-plan": serializer.data}, status=200)
            return Response({"message": "missing required keys for creating meal plan. Ensure that you include an object with the following keys: name: [str], active: [boolean]"}, status=400)
        meal_plan_to_edit = get_object_or_404(MealPlan, pk=request.data['meal_plan_id'])
        has_permission = meal_plan_to_edit.owner.id == user.id or user.is_staff
        if not has_permission:
            return Response({"message": "You can only edit meal plans you are the owner of"}, status=401)
        if request.method == "DELETE":
            meal_plan_to_edit.delete()
            return Response({"message": "successfully deleted meal plan"}, status=200)
        elif request.method == "PUT":
            serializer = MealPlanSerializer(meal_plan_to_edit)
            data = {key: value for key, value in request.data.items() if key in serializer.data}
            if request.data["active"]:
                    try:
                        meal_to_deactivate = MealPlan.objects.get(owner=user, active=True)
                        meal_to_deactivate.deactivate()
                    except MealPlan.DoesNotExist:
                        pass
            updated_meal_plan = meal_plan_to_edit.update(data)
            updated_serializer = MealPlanSerializer(updated_meal_plan)
            return Response({'message': f"Successfully updated {updated_meal_plan.name}", "updated_meal_plan": updated_serializer.data}, status=200)
    except Exception as e:
        print(e)
        return Response({"message": "Missing some required keys in the request body. Check your code and try again"}, status=400)
    
# To do: add route for adding and editing meals to mealplan, make it so that only 1 mealplan can be active at a time. Then write tests and assemble documentation so I know how to use this api later when I build the front end. 

@api_view(["GET", "POST", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def meal_plan_detail(request, meal_plan_id):
    user_id = Token.objects.get(key=request.auth.key).user_id
    user = CustomUser.objects.get(pk=user_id)
    meal_plan = get_object_or_404(MealPlan, pk=meal_plan_id)
    has_permission = meal_plan.owner.id == user.id or user.is_staff
    if not has_permission:
        return Response({"message": "You can only access meal plans that you are the owner of"}, status=401)
    #Get method on this route simply returns the full details and meals of a particular meal plan
    if request.method == "GET":
        serializer = MealPlanSerializerFull(meal_plan)
        return Response(serializer.data)
        #Post method for adding new meals onto a meal plan at a specified index and reording the rest accordingly so that everything stays in the correct order.
    try:
        if request.method == "POST":
            meal_to_add = get_object_or_404(Meal, pk=request.data['meal_id'])
            curr_meal_plan_meals_len = meal_plan.meal_set.all().count()
            # meals_to_be_adjusted = MealPlanOrder.objects.filter(meal_plan=meal_plan).filter(index__gte=request.data['index'])
            # for meal in meals_to_be_adjusted:
            #     meal.update_index(1)
            meal_plan.meal_set.add(meal_to_add, through_defaults={"index": curr_meal_plan_meals_len})
            return Response({"message": "Successfully added new meal to meal plan"}, status=200)
        #Delete method removes specified meal from meal plan and updates indexes accordingly
        if request.method == "DELETE":
            try:
                meal_to_delete = MealPlanOrder.objects.filter(Q(index=request.data['index'])&Q(meal_plan_id=meal_plan.id))
                meals_to_be_adjusted = MealPlanOrder.objects.filter(meal_plan=meal_plan).filter(index__gte=request.data['index'])
                meal_to_delete.delete()
                for meal in meals_to_be_adjusted:
                    meal.update_index(-1)
                return Response({"message": "Successfully removed meal from meal plan"}, status=204)
            except MealPlanOrder.DoesNotExist:
                return Response({"message": "Requested meal not found on meal plan"}, status=404)
        if request.method == "PUT":
            index1 = request.data['index']
            index2 = request.data['index2']
            meal1 = MealPlanOrder.objects.filter(Q(index=index1)&Q(meal_plan_id=meal_plan.id))[0]
            meal2 = MealPlanOrder.objects.filter(Q(index=index2)&Q(meal_plan_id=meal_plan.id))[0]
            meal1.set_index(index2)
            meal2.set_index(index1)
            serializer = MealPlanSerializerFull(meal_plan)
            return Response({"message": "Successfully updated meal order on meal plan", "updated_meal": serializer.data}, status=200)
    except KeyError:
        return Response({"message": "please supply object with the following keys in request body: index: [int], index2: [int] ** only for PUT requests, meal_id: [int] ** only for POST requests"})
    
        
    