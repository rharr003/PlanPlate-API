from django.urls import path
from . import views

urlpatterns = [
    path("", views.meal, name="meal"),
    path("detail/<int:meal_id>", views.meal_detail, name="meal_detail" )
]