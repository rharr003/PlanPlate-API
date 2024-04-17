from django.db import models
from api.models import CustomUser
# Create your models here.

class FoodItem(models.Model):
    name = models.CharField(null=False, max_length=100)
    base_serving_size = models.FloatField(null=False)
    base_serving_size_unit = models.CharField(null=False, max_length=25)
    calories = models.IntegerField(null=False)
    fat = models.FloatField(null=False)
    saturated_fat = models.FloatField(default=0.0)
    carbohydrates = models.FloatField(null=False)
    fiber = models.FloatField(default=0.0)
    sugar = models.FloatField(default= 0.0)
    protein = models.FloatField(null=False)
    sodium = models.IntegerField(default=0)
    potassium = models.IntegerField(default=0)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def update(self, fields):
        for field_name, value in fields.items():
            setattr(self, field_name, value)
        self.save(update_fields=fields)
        return self