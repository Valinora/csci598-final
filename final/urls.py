# /backend/final/urls.py

from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.http import JsonResponse

from reststop_rater.views.login import UserJoin, UserLogin, user_logout
from reststop_rater.views.home import HomePage
from reststop_rater.views.apitest import ApiTest


def cors_test_view(request):
    return JsonResponse({"message": "CORS works!"})


urlpatterns = [
    path("api/cors-test/", cors_test_view),
    path("admin/", admin.site.urls),
    path("api/", include("reststop_rater.urls")),
    path("login/", UserLogin.as_view()),
    path("logout/", user_logout),
    path("join/", UserJoin.as_view()),
    path("", HomePage.as_view()),
    path("apitest", ApiTest.as_view()),
]
