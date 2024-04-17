from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractUser
# Create your models here.
    
#make sure you implement your custom user before the first migration    
class CustomUser(AbstractUser):
    class Format(models.TextChoices):
        METRIC = "metric"
        IMPERIAL = "imperial"
    weight = models.FloatField(default=0.0)
    weight_format = models.CharField(choices=Format.choices, max_length=8, default="imperial")
    height = models.IntegerField(default=0)
    height_format = models.CharField(choices=Format.choices, max_length=8, default="imperial")
    date_of_birth = models.DateField(default=now)
    
    def update(self, fields):
        for field_name, value in fields.items():
            setattr(self, field_name, value)
        self.save(update_fields=fields)
        