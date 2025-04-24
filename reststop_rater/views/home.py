from django.shortcuts import render
from django.views import View

from ..models.bathroom import Bathroom


class HomePage(View):
    template = "index.html"

    def get(self, request):
        bathrooms = Bathroom.get_nearby_bathrooms(5, 5) # TODO: Figure out how to get this from the user and then update the results
        return render(request, self.template, {"bathrooms": bathrooms})