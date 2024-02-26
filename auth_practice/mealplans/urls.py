from django.urls import path
from . import views

urlpatterns = [
    path("", views.meal_plan, name='meal_plan'),
    path("detail/<int:meal_plan_id>", views.meal_plan_detail, name="meal_plan_detail")
]