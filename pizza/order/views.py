from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem, Pizza

# Create your views here.
@login_required
def place_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        OrderItemFormSet = modelformset_factory(OrderItem, exclude=())
        formset = OrderItemFormSet(request.POST, request.FILES)

        if (form.is_valid() and formset.is_valid()):
            order = form.save()
            instances = formset.save(commit=False)
            for i in instances:
                i.order=order
            formset.save()
            return redirect(order)
    else:
        order = Order(user=request.user)
        form = OrderForm(instance=order)

        orderItem = OrderItem(order=order)
        itemsForm = OrderItemForm(instance=orderItem)

        OrderItemFormSet = modelformset_factory(OrderItem, exclude=(), extra=2)
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())

    return render(request, "orders/order_form.html", {'formOrder' : form,
                                        'formSetOrderItem': formset})

@login_required
@csrf_exempt
def get_price(request):
    if request.method == "GET":
        pizza_name = request.GET.get('name')
        if (pizza_name == '---------'):
            return HttpResponse("0");
        pizza = get_object_or_404(Pizza, name= pizza_name)
        print(pizza.price)
        return HttpResponse(pizza.price)
    else:
        return HttpResponse("Request method is not a GET")


@login_required
def order_summary(request, id):
    order = get_object_or_404(Order, pk=id)
    order_items = OrderItem.objects.all().filter(order=order)
    if not request.user == order.user:
        raise PermissionDenied
    return render(request, "orders/order_summary.html", {'order': order,
                                                'order_items': order_items})

def pizza_details(request, id):
    pizza = get_object_or_404(Pizza, pk=id)
    return render(request, "orders/pizza_details.html", {'pizza': pizza})
