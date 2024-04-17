from .models import Meal
from rest_framework import serializers
from foodserving.serializers import FoodServingSerializer
class MealSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(write_only=True)
    food_servings = serializers.SerializerMethodField(read_only=True)
    #using a method here lets us have the returned list of food_servings properly ordered
    def get_food_servings(self, model):
        data = [food_serving for food_serving in model.foodserving_set.all().order_by("mealorder__index")]
        serializer = FoodServingSerializer(data, many=True)
        return serializer.data
    
    class Meta:
        model = Meal
        fields = ['id', 'name', 'type', "owner_id", "food_servings"]