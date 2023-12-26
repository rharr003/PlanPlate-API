from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views


urlpatterns = [
    path("user", views.get_user_info, name="user"),
    path("signup", views.signup, name="signup"),
    path("login", auth_views.obtain_auth_token, name="login")
]
