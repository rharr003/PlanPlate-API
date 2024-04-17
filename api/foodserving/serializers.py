from .models import FoodServing
from rest_framework import serializers
from fooditems.serializers import FoodItemSerializer


class FoodServingSerializer(serializers.ModelSerializer):
    # not entirely sure how this works but we need the foreign key passed in the the data and the nested serializer somehow figures things out
    #specifying write only means this data wont be returned in serialize.data but can be used to properly save the entry when using serialize.save
    owner_id = serializers.IntegerField(write_only=True)
    food_item_id = serializers.IntegerField(write_only=True)
    food_item = FoodItemSerializer(read_only=True)
    
    class Meta:
        model = FoodServing
        fields = ["id","serving_multiple", "owner_id", "food_item_id", "food_item"]