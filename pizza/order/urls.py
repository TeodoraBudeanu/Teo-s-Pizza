from django.urls import path, re_path
from .views import place_order, order_summary

urlpatterns = [
    re_path(r'place_order$', place_order, name="place_order"),
    re_path(r'order_summary/(?P<id>\d+)/$', order_summary, name="order_summary"),
]
