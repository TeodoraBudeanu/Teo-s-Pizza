from django.urls import re_path
from allauth.account import views
from .views import HomeView, AccountView, CustomPasswordChangeView

urlpatterns = [
    re_path(r'login$', views.LoginView.as_view(template_name="login.html"),
            name='login'),
    re_path(r'logout$', views.LogoutView.as_view(template_name="logout.html"),
            name="logout"),
    re_path(r'signup$', views.SignupView.as_view(
            template_name="account_signup.html"), name="account_signup"),
    re_path(r'password/change$', CustomPasswordChangeView.as_view(
            template_name="password_change.html"),
            name="account_change_password"),
    re_path(r'account$', AccountView.as_view(), name="account"),
    re_path(r'home$', HomeView.as_view(), name="home"),
    re_path(r'^$', HomeView.as_view(), name="home"),
]
