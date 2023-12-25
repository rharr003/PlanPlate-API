from django.urls import path
from . import views

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken import views as auth_views


urlpatterns = [
    path("cookie", views.get_cookie),
    path("signup", views.signup),
    path("login", auth_views.obtain_auth_token)
]
