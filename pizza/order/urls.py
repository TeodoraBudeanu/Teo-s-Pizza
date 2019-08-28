from django.urls import re_path
from .views import *

urlpatterns = [
    re_path(r'^place_order$', PlaceOrder.as_view(), name="place_order"),
    re_path(r'^save_order$', SaveOrder.as_view(), name="save_order"),
    re_path(r'^save_item$', SaveItem.as_view(), name="save_item"),
    re_path(r'^delete_item$', DeleteItem.as_view(), name="delete_item"),
    re_path(r'^create_item$', CreateItem.as_view(), name="create_item"),
    re_path(r'^order_details/(?P<pk>\d+)/$', OrderDetails.as_view(),
            name="order_details"),
    re_path(r'^confirm_order$', ConfirmOrder.as_view(), name="confirm_order"),
    re_path(r'^check_total$', CheckTotal.as_view(), name="check_total"),

]
