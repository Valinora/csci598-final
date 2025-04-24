from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View

from ..forms import LoginForm, JoinForm


class UserJoin(View):
    template = "join.html"
    form_class = JoinForm

    def get(self, request):
        page_data = {"join_form": self.form_class}
        return render(request, self.template, page_data)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            return redirect("/")


class UserLogin(View):
    template = "login.html"
    form_class = LoginForm

    def get(self, request):
        page_data = {
            "login_form": self.form_class,
            "next": request.GET.get("next", "/"),
        }

        return render(request, self.template, page_data)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user and user.is_active:
                login(request, user)
                return redirect(request.POST.get("next", "/"))

        return render(request, self.template, {"login_form": form})


@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return redirect("/")
