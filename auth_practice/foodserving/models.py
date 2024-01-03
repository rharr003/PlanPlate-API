from django.db import models
from fooditems.models import FoodItem
from meals.models import Meal
from api.models import CustomUser

# Create your models here.


class FoodServing(models.Model):
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    serving_multiple = models.FloatField( null=False)
    meals = models.ManyToManyField(Meal, through='MealOrder')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class MealOrder(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    food_serving = models.ForeignKey(FoodServing, on_delete=models.CASCADE)
    index = models.IntegerField()