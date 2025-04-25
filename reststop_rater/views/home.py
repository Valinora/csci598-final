from django.shortcuts import render
from django.views import View

from ..services.bathroom import get_nearby_bathrooms


class HomePage(View):
    template = "home.html"

    def get(self, request):
        bathrooms = get_nearby_bathrooms(5, 5) # TODO: Figure out how to get this from the user and then update the results
        return render(request, self.template, {"bathrooms": bathrooms})