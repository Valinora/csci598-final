from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View

from ..forms import CreateBathroomForm, ReviewForm


class ApiTest(View):
    template = "apitest.html"
    bathroom_form = CreateBathroomForm
    review_form = ReviewForm

    def get(self, request):
        return render(
            request,
            self.template,
            {"bathroom_form": self.bathroom_form, "review_form": self.review_form},
        )
