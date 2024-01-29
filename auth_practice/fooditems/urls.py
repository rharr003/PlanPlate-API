from django.urls import path
from . import views

urlpatterns = [
    path('', views.food_item, name="food_item"),
]