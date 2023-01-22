from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, LoginForm
from django.contrib.auth import login
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required

# Create your views here.


class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("accounts:profile")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class LoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("accounts:profile")


class LogoutView(LogoutView):
    template_name = "registration/logout.html"


class topView(generic.TemplateView):
    template_name = "registration/top.html"


class exampleView(generic.TemplateView):
    template_name = "registration/example.html"


@login_required
def profile(request):
    return render(request, "registration/profile.html")


@login_required
def friend(request):
    return render(request, "registration/friend.html")


@login_required
def friend_profile(request, friend_profile):
    return render(request, "registration/friend_profile.html", {"name": friend_profile})
