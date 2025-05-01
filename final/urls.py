# /backend/final/urls.py

import requests

from django.contrib import admin
from django.conf import settings
from django.shortcuts import render
from django.urls import path, include
from django.http import HttpResponse, JsonResponse

from reststop_rater.views.login import UserJoin, UserLogin, user_logout
from reststop_rater.views.bathrooms import BathroomDetail, ReportView, QuickRateView
from reststop_rater.views.nearby import NearbyBathrooms

def cors_test_view(request):
    return JsonResponse({"message": "CORS works!"})

def home(request):
    return render(request, "home.html")

def server_info(request):
    server_geodata = requests.get('https://ipwhois.app/json/').json()
    settings_dump = settings.__dict__
    return HttpResponse("{}{}".format(server_geodata, settings_dump))

urlpatterns = [
    path("api/cors-test/", cors_test_view),
    path("admin/", admin.site.urls),
    path("login/", UserLogin.as_view(), name='login'),
    path("logout/", user_logout),
    path("join/", UserJoin.as_view(), name='join'),
    path("", home),
    path("bathrooms/<int:id>/", BathroomDetail.as_view(), name='bathroom_detail'),
    path("report/<int:id>/<str:response>/", ReportView.as_view(), name="report"),
    path("quickrate/<int:id>/<int:rating>/", QuickRateView.as_view(), name="quick_rate"),
    path("quickrate/<int:id>/", QuickRateView.as_view(), name="quick_rate_post"),
    path("nearby/", NearbyBathrooms.as_view()),
    path("server_info/", server_info),
]