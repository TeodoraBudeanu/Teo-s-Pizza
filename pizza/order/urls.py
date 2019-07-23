from django.urls import path, re_path
from .views import PlaceOrder, OrderSummary, PizzaDetails, GetPrice, ConfirmOrder

urlpatterns = [
    re_path(r'^place_order$', PlaceOrder.as_view(), name="place_order"),
    re_path(r'^order_summary/(?P<pk>\d+)/$', OrderSummary.as_view(), name="order_summary"),
    re_path(r'^pizza_details/(?P<pk>\d+)/$', PizzaDetails.as_view(), name="pizza_details"),
    re_path(r'^get_price$', GetPrice.as_view(), name="get_price"),
    re_path(r'^confirm_order$', ConfirmOrder.as_view(), name="confirm_order"),
]
