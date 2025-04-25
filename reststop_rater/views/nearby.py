from django.shortcuts import render
from django.views import View

class NearbyBathrooms(View):
    template = "nearby.html"


    def get(self, request):
        return render(request, self.template)