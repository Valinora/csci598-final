from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from ..forms import LoginForm, JoinForm

class UserJoin(View):
    template = "join.html"
    form_class = JoinForm

    def get(self, request):
        next_url = request.GET.get("next", "/")
        print(f"Next URL from GET: {next_url}")
        page_data = {
            "join_form": self.form_class,
            "next": next_url,
        }
        return render(request, self.template, page_data)

    def post(self, request):
        form = self.form_class(request.POST)
        next_url = request.POST.get("next", "/")
        print(f"Next URL from POST: {next_url}")

        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user and user.is_active:
                login(request, user)

            print(f"Redirecting to: {next_url}")
            return redirect(next_url)
            
        return render(request, self.template, {"join_form": form, "next": next_url})

class UserLogin(View):
    template = "login.html"
    form_class = LoginForm

    def get(self, request):
        next_url = request.GET.get("next", "/")
        print(f"Next URL from GET: {next_url}")
        page_data = {
            "login_form": self.form_class,
            "next": next_url,
        }
        return render(request, self.template, page_data)

    def post(self, request):
        form = self.form_class(request.POST)
        next_url = request.POST.get("next", "/")
        print(f"Next URL from POST: {next_url}")

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(username=username, password=password)

            if user and user.is_active:
                login(request, user)
                print(f"Redirecting to: {next_url}")
                return redirect(next_url)

        return render(request, self.template, {"login_form": form, "next": next_url})

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    next_url = request.GET.get('next', '/')
    print(f"Redirecting to: {next_url}")
    return redirect(next_url)
