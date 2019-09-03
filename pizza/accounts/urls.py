from django.urls import re_path
from allauth.account.views import LoginView, LogoutView, SignupView
from .views import Home

urlpatterns = [
    re_path(r'login$', LoginView.as_view(template_name="login.html"),
            name='login'),
    re_path(r'logout$', LogoutView.as_view(template_name="logout.html"),
            name="logout"),
    re_path(r'signup$', SignupView.as_view(
            template_name="account_signup.html"), name="account_signup"),
    re_path(r'home$', Home.as_view(), name="home"),
    re_path(r'^$', Home.as_view(), name="home"),
]
