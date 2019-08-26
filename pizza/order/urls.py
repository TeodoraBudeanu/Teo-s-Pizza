from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^place_order$', PlaceOrder.as_view(), name="place_order"),
    re_path(r'^save_order$', SaveOrder.as_view(), name="save_order"),
    re_path(r'^order_details/(?P<pk>\d+)/$', OrderDetails.as_view(),
            name="order_details"),
    re_path(r'^pizza_details/(?P<pk>\d+)/$', PizzaDetails.as_view(),
            name="pizza_details"),
    re_path(r'^confirm_order$', ConfirmOrder.as_view(), name="confirm_order"),
    re_path(r'^check_total$', CheckTotal.as_view(), name="check_total"),
    re_path(r'^check_stock$', CheckStock.as_view(), name="check_stock"),

]
