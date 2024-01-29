from django.db import models
from api.models import CustomUser
from mealplans.models import MealPlan

# Create your models here.
class Meal(models.Model):
    name = models.CharField(null=False, max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    type = models.CharField(choices=[("meal", "meal"), ("snack", "snack")], max_length=5)
    meal_plan = models.ManyToManyField(MealPlan, through='MealPlanOrder')
    def update(self, fields):
        for field_name, value in fields.items():
            setattr(self, field_name, value)
        self.save(update_fields=fields)
        return self
    
class MealPlanOrder(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    meal_plan = models.ForeignKey(MealPlan, on_delete=models.CASCADE)
    index = models.IntegerField()