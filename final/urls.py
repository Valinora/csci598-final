# /backend/final/urls.py

from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.http import JsonResponse

from reststop_rater.views.login import UserJoin, UserLogin, user_logout
from reststop_rater.views.bathrooms import BathroomDetail
from reststop_rater.views.nearby import NearbyBathrooms

def cors_test_view(request):
    return JsonResponse({"message": "CORS works!"})

def home(request):
    return render(request, "home.html")

urlpatterns = [
    path("api/cors-test/", cors_test_view),
    path("admin/", admin.site.urls),
    path("login/", UserLogin.as_view(), name='login'),
    path("logout/", user_logout),
    path("join/", UserJoin.as_view(), name='join'),
    path("", home),
    path("bathrooms/<int:id>/", BathroomDetail.as_view(), name='bathroom_detail'),
    path("nearby/", NearbyBathrooms.as_view()),
]