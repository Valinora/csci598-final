from django.shortcuts import render
from django.views import View


class HomePage(View):
    template = "home.html"

    def get(self, request):
        return render(request, self.template)