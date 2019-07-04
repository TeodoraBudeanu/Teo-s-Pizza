from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem

# Create your views here.
@login_required
def place_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        form2 = OrderItemForm(request.POST)

        if (form.is_valid() and form2.is_valid()):
            order = form.save()
            orderItem = OrderItem(order=order)
            form2 = OrderItemForm(instance=orderItem, data=request.POST)
            form2.save()
            return redirect(order)
    else:
        order = Order(user=request.user)
        form = OrderForm(instance=order)

        orderItem = OrderItem(order=order)
        form2 = OrderItemForm(instance=orderItem)

    return render(request, "orders/order_form.html", {'formOrder' : form,
                                        'formOrderItem': form2})

@login_required
def order_summary(request, id):
    order = get_object_or_404(Order, pk=id)
    order_items = OrderItem.objects.all().filter(order=order)
    if not request.user == order.user:
        raise PermissionDenied
    return render(request, "orders/order_summary.html", {'order': order,
                                                'order_items': order_items})
