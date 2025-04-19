# /backend/final/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.views.generic import View
from django.http import FileResponse
from pathlib import Path

def cors_test_view(request):
    return JsonResponse({"message": "CORS works!"})


BASE_DIR = Path(__file__).resolve().parent.parent.parent 
index_file_path = BASE_DIR / 'frontend' / 'dist' / 'index.html'

class SPAView(TemplateView):
    def get(self, request, *args, **kwargs):
        return FileResponse(open(index_file_path, 'rb'), content_type='text/html')

urlpatterns = [
    path("api/cors-test/", cors_test_view),
    path('admin/', admin.site.urls),
    path('api/', include('reststop_rater.urls')),
    re_path(r'^(?!api/|api$).*', SPAView.as_view()),
    #re_path(r'^(?!api/|api$).*', TemplateView.as_view(template_name="index.html")),
] 
