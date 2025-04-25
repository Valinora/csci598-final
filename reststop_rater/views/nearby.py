from django.shortcuts import render
from django.views import View

from ..services.bathroom import get_nearby_bathrooms

class NearbyBathrooms(View):
    template = "nearby.html"


    def get(self, request):
        try:
            lat = float(request.GET["lat"])
            long = float(request.GET["long"])
            bathrooms = get_nearby_bathrooms(lat, long)

        except ValueError:
            print("blerg")
        bathrooms = get_nearby_bathrooms(5, 5) # TODO: Get this information from the get request.
        return render(request, self.template, {"bathrooms": bathrooms})