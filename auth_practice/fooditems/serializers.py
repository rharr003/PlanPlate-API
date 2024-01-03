from rest_framework import serializers
from .models import FoodItem
from api.serializers import UserSerializer

class FoodItemSerializer(serializers.ModelSerializer):
    # not entirely sure how this works but we need the foreign key passed in the the data and the nested serializer somehow figures things out
    owner_id = serializers.IntegerField(write_only=True)
    owner = UserSerializer(read_only=True)
    
    class Meta:
        model = FoodItem
        fields = ["id", 'name', 'calories', 'base_serving_size', "base_serving_size_unit", "fat", "saturated_fat", "carbohydrates", "fiber", "sugar", "protein", "sodium", "potassium", "owner", "owner_id"]