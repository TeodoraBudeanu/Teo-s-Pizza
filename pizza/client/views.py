from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from order.models import Order

# Create your views here.
@login_required()
def home(request):
    my_orders = Order.objects.orders_for_client(request.user)
    return render (request, "client/home.html", {"orders" : my_orders})
