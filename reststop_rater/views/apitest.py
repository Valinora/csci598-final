from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from ..forms import CreateBathroomForm, ReviewForm


class ApiTest(LoginRequiredMixin, View):
    login_url = "/login/"
    template = "apitest.html"
    bathroom_form = CreateBathroomForm
    review_form = ReviewForm

    def get(self, request):
        return render(
            request,
            self.template,
            {"bathroom_form": self.bathroom_form, "review_form": self.review_form},
        )
