from django.urls import re_path

from .views import PizzaDetails

urlpatterns = [
    re_path(r'^details/(?P<pk>\d+)/$', PizzaDetails.as_view(), name="details"),
]
