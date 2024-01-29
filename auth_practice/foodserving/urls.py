from django.urls import path 
from . import views

urlpatterns = [
    path("", views.food_serving, name="food_serving"),
    # path("<int:meal_id>", views.food_serving_meals, name="food_serving_meals")
]
