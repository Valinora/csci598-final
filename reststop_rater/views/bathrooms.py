from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from ..forms import CreateBathroomForm, ReviewForm
from ..models.bathroom import Bathroom
from django.http import Http404



class BathroomDetail(View):
    template = "bathroom_detail.html"

    def get(self, request, id):
        # Fetch the Bathroom object using its local database ID
        bathroom = get_object_or_404(Bathroom, id=id)

        # Render the detailed bathroom page
        return render(request, self.template, {"bathroom": bathroom})

    def post(self, request, id):
        print("post called")
        # Handle when the user clicks on a specific bathroom (for example, saving review or other actions)
        bathroom = get_object_or_404(Bathroom, id=id)

        # Process the data from the form (example: saving reviews or other operations)
        if all(key in request.POST for key in ['name', 'address', 'lat', 'long']):
            bathroom.name = request.POST.get("name")
            bathroom.address = request.POST.get("address")
            bathroom.latitude = request.POST.get("lat")
            bathroom.longitude = request.POST.get("long")
            bathroom.save()
            
            print("Updated Bathroom:", bathroom)

            return redirect("bathroom_detail", id=id)
        else:
            print("Missing data in POST request!")
            return Http404("Missing bathroom data in the request.")