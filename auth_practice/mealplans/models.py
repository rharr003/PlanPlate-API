from django.db import models
from api.models import CustomUser

# Create your models here.

class MealPlan(models.Model):
    name = models.CharField(null=False, max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
