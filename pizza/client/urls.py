from django.urls import re_path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    re_path(r'home$', OrderList.as_view(), name='client_home'),
    re_path(r'login$', LoginView.as_view(
            template_name="client/login_form.html"), name='client_login'),
    re_path(r'logout$', LogoutView.as_view(), name="client_logout"),
    re_path(r'new_user$', CreateNewUser.as_view(), name="new_user"),
    re_path(r'check_username$', CheckUsername.as_view(),
            name="check_username"),
    re_path(r'check_email$', CheckEmail.as_view(), name="check_email"),

]
