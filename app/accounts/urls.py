# accounts/urls.py
from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("top/", views.topView.as_view(), name="top"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("profile/", views.profile, name="profile"),
    path("friend/", views.friend, name="friend"),
    path("friend/<str:friend_profile>", views.friend_profile, name="friend_profile"),
    path("example/", views.exampleView.as_view(), name="example"),
]
