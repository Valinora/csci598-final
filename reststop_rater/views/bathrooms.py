from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from ..forms import CreateBathroomForm, ReviewForm
from ..models.bathroom import Bathroom


class CreateBathroom(LoginRequiredMixin, View):
    login_url = "/login/"
    template = "createbathroom.html"
    form = CreateBathroomForm

    def get(self, request):
        return render(
            request,
            self.template,
            {"bathroom_form": self.form},
        )

    def post(self, request):
        form = self.form(request.POST)
        data = {"bathroom_form": self.form}

        if form.is_valid():
            name = form.cleaned_data["name"]
            address = form.cleaned_data["address"]
            lat = form.cleaned_data["latitude"]
            long = form.cleaned_data["longitude"]

            new_bathroom = Bathroom.create_bathroom(name, address, lat, long)
            return redirect(f"/bathrooms/{new_bathroom.pk}")

        else:
            data["bathroom_form"] = form # is_valid call adds validation errors for display.
        
        return render(request, self.template, data)


class BathroomDetailView(View):
    template = "bathroom.html"
    review_form = ReviewForm
    
    def get(self, request, *args, **kwargs):
        id = kwargs["bathroom_id"]
        bathroom = get_object_or_404(Bathroom, id=id)

        return render(request, self.template, {"review_form": self.review_form, "bathroom": bathroom})

