from .models import MealPlan
from rest_framework import serializers
from meals.serializers import MealSerializer


class MealPlanSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MealPlan
        fields = ['id', 'name', 'active', "owner_id"]
        
class MealPlanSerializerFull(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    meals = serializers.SerializerMethodField(read_only=True)
    def get_meals(self, model):
        data = [meal for meal in model.meal_set.all().order_by("mealplanorder__index")]
        serializer = MealSerializer(data, many=True)
        return serializer.data
    class Meta:
        model = MealPlan
        fields = ['id', 'name', 'active', "owner_id", "meals"]