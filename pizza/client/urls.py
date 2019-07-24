from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from .views import OrderList

urlpatterns = [
    re_path(r'home$', OrderList.as_view(), name='client_home'),
    re_path(r'login$', LoginView.as_view(template_name="client/login_form.html"),
                                        name='client_login'),
    re_path(r'logout$', LogoutView.as_view(), name="client_logout"),

]
