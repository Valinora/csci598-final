from django.shortcuts import render, redirect
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

            Bathroom.create_bathroom(name, address, lat, long)

        else:
            data["bathroom_form"] = form # is_valid call adds validation errors for display.
        
        return render(request, self.template, data)



class ReviewBathroom(LoginRequiredMixin, View):
    login_url = "/login/"
    template = "reviewbathroom.html"
    form = ReviewForm

    def get(self, request):
        return render(
            request,
            self.template,
            {"review_form": self.form},
        )
