from django.urls import path, re_path
from .views import place_order, order_summary, pizza_details, get_price, confirm_order

urlpatterns = [
    re_path(r'^place_order$', place_order, name="place_order"),
    re_path(r'^order_summary/(?P<id>\d+)/$', order_summary, name="order_summary"),
    re_path(r'^pizza_details/(?P<id>\d+)/$', pizza_details, name="pizza_details"),
    re_path(r'^get_price$', get_price, name="get_price"),
    re_path(r'^confirm_order$', confirm_order, name="confirm_order"),
]
