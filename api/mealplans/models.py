from django.db import models
from api.models import CustomUser

# Create your models here.

class MealPlan(models.Model):
    name = models.CharField(null=False, max_length=100)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    active = models.BooleanField(default=False)
    def update(self, fields):
        for field_name, value in fields.items():
            setattr(self, field_name, value)
        self.save(update_fields=fields)
        return self
    def deactivate(self):
        setattr(self, "active", False)
        self.save(update_fields="active")
        return self
