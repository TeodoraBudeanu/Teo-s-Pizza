from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem, Pizza
from .serializers import PizzaSerializer, OrderSerializer, OrderItemSerializer

# Create your views here.
class PlaceOrder(LoginRequiredMixin, FormView):
    def get(self, request, format=None):
        Order.objects.filter(confirmed='0').delete()
        order = Order(user=request.user)
        form = OrderForm(instance=order)
        orderItem = OrderItem(order=order)
        itemsForm = OrderItemForm(instance=orderItem)
        OrderItemFormSet = modelformset_factory(OrderItem, exclude=())
        formset = OrderItemFormSet(queryset=OrderItem.objects.none())
        return render(request, "orders/order_form.html", {'formOrder' : form,
                                    'formSetOrderItem': formset})

    def post(self, request, format=None):
        order = Order(user=request.user)
        form = OrderForm(request.POST, instance = order)
        OrderItemFormSet = modelformset_factory(OrderItem, exclude=('confirmed',))
        formset = OrderItemFormSet(request.POST, request.FILES)
        if (form.is_valid() and formset.is_valid()):
            order = form.save()
            order.save()
            instances = formset.save(commit=False)
            for i in instances:
                i.order=order
                i.save()
            return redirect('confirm_order')


class ConfirmOrder(LoginRequiredMixin, TemplateView):
    def get(self, request, format=None):
        order = Order.objects.get(confirmed='0')
        orderItems = OrderItem.objects.filter(order=order)

        return render(request, "orders/order_confirmation.html",
                                {'order': order, 'orderItems': orderItems})

    def post(self, request, format=None):
        order = Order.objects.get(confirmed='0')
        setattr(order, 'confirmed', '1')
        order.save()
        orderItems = OrderItem.objects.filter(order=order)
        return redirect(order)


@method_decorator(csrf_exempt, name='dispatch')
class GetPrice(TemplateView):
    def get(self, request):
        pizza_name = request.GET.get('name')
        if (pizza_name == '---------'):
            return HttpResponse("0");
        pizza = get_object_or_404(Pizza, name=pizza_name)
        return HttpResponse(pizza.price)


class OrderSummary(LoginRequiredMixin, DetailView):
    model = OrderForm

    def get(self, request,*args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs['pk'])
        order_items = OrderItem.objects.all().filter(order=order)
        if not request.user == order.user:
            raise PermissionDenied
        return render(request, "orders/order_summary.html", {'order': order,
                                                'order_items': order_items})


class PizzaDetails(DetailView):
    model = Pizza

    def get(self, request,*args, **kwargs):
        pizza = get_object_or_404(Pizza, pk=kwargs['pk'])
        context = {'pizza': pizza}
        return render(request, 'orders/pizza_details.html', context)
