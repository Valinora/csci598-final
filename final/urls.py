# /backend/final/urls.py

from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.http import JsonResponse


def cors_test_view(request):
    return JsonResponse({"message": "CORS works!"})


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")

def apitest(request):
    return render(request, "apitest.html")


urlpatterns = [
    path("api/cors-test/", cors_test_view),
    path("admin/", admin.site.urls),
    path("api/", include("reststop_rater.urls")),
    path("", index),
    path("about", about),
    path("apitest", apitest)
]
