from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, FormView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import OrderForm, OrderItemForm
from .models import Order, OrderItem, Pizza
from .serializers import PizzaSerializer, OrderSerializer, OrderItemSerializer
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class GetOrder(TemplateView):

    def get(self, request):
        order_id = request.GET.get('id')
        order = get_object_or_404(Order, pk=order_id)
        setattr(order, 'confirmed', '0')
        order.save()
        order_serializer = OrderSerializer(order)
        return JsonResponse(order_serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class GetPizzas(TemplateView):

    def get(self, request):
        pizzas = Pizza.objects.filter(stock__gt=0)
        pizzas_ser=[]
        for pizza in pizzas:
            pizzas_ser.append(PizzaSerializer(pizza).data)
        return JsonResponse(pizzas_ser, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class GetPizzaStock(TemplateView):

    def get(self, request):
        name = request.GET.get('name')
        stock = get_object_or_404(Pizza, name=name).stock
        return JsonResponse(stock)


@method_decorator(login_required, name='dispatch')
class PlaceOrder(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/order_form.html'
    serializer_class = OrderSerializer
    style_vert = {'template_pack': 'rest_framework/vertical/'}
    style_hor = {'template_pack': 'rest_framework/inline/'}

    def get_queryset(self):
        return Order.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(paid='0').filter(user=self.request.user)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return None
        return obj

    def get(self, request, *args, **kwargs):
        # get order, order_item objects
        order = self.get_object()
        if (order is None):
            order = Order(user=request.user)
            order.save()
            order_item = OrderItem(order=order)
            order_item.save()
        else:
            setattr(order, 'confirmed', '0')
            order.save()
        # serializers
        order_ser = OrderSerializer(order)
        order_items_ser = []
        oi_query = OrderItem.objects.filter(order=order)
        for item in oi_query:
            order_items_ser.append(OrderItemSerializer(item))
        return Response({'order_ser': order_ser, 'order_items_ser' : order_items_ser,
                    'order': order, 'style_vert': self.style_vert, 'style_hor': self.style_hor})


@method_decorator(login_required, name='dispatch')
class SaveOrder(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/order_details.html'
    serializer_class = OrderSerializer
    permission_classes = []

    def get_queryset(self):
        return Order.objects.all()

    def get(self, request):
        # parse request data
        def parseString(s):
            s = s.split('&')
            st = []
            arr = []
            for subs in s:
                subs = subs.split('=')
                arr.append({subs[0]: subs[1]})
            return arr

        order_data = parseString(request.GET['order_data'])
        order_item_data = parseString(request.GET['order_item_data'])
        # update order
        order = get_object_or_404(Order, pk=request.GET['order_id'])
        order_data = {**order_data[1], **order_data[2]}
        serializer = OrderSerializer(order, data=order_data, partial=True)
        if (serializer.is_valid()):
            order=serializer.save()
            setattr(order, 'confirmed', '1')
            order.save()
        else:
            return JsonResponse({'text':serializer.errors})
        # update order items
        OrderItem.objects.filter(order=order).delete()

        n = len(order_item_data)
        for i in range(0, n, 2):
            order_item = OrderItem(order=order)
            order_item.save()
            data = {**order_item_data[i], **order_item_data[i+1]}
            serializer = OrderItemSerializer(order_item, data=data, partial=True)
            if (serializer.is_valid()):
                serializer.save()
            else:
                return JsonResponse({'text':serializer.errors})
        OrderItem.objects.filter(quantity=0).delete()
        return JsonResponse(order.get_amount(), safe=False)


@method_decorator(login_required, name='dispatch')
class ConfirmOrder(CreateAPIView):
    def get_queryset(self):
        return Order.objects.all()

    def get(self, request, format=None):
        order = Order.objects.filter(paid='0').get(user=request.user)
        order_items = OrderItem.objects.filter(order=order)
        return render(request, "orders/order_confirmation.html",
                                {'order': order, 'orderItems': order_items})

    def post(self, request, format=None):
        order = Order.objects.filter(paid='0').get(user=request.user)
        setattr(order, 'paid', '1')
        order.save()
        order_items = OrderItem.objects.filter(order=order)
        for item in order_items:
            item.pizza_type.stock -= item.quantity
            item.pizza_type.save()
        return redirect(order)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class GetPrice(TemplateView):

    def get(self, request):
        pizza_name = request.GET.get('name')
        if (pizza_name == '---------'):
            return JsonResponse("0");
        pizza = get_object_or_404(Pizza, name=pizza_name)
        return JsonResponse(pizza.price)

class CheckStock(TemplateView):

    def get(self, request):
        pizza_id = request.GET.get('pizza_id')
        quantity = request.GET.get('quantity')
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        if pizza.stock >= int(quantity):
            return JsonResponse("ok", safe=False)
        else:
            return JsonResponse("There are only " + str(pizza.stock) + " " + pizza.name + " left in stock.", safe=False)


class CheckTotal(TemplateView):

    def get(self, request):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        return JsonResponse(order.get_amount(), safe=False)


@method_decorator(login_required, name='dispatch')
class OrderDetails(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/order_details.html'
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs['pk']
        queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return None
        return obj

    def get(self, request,*args, **kwargs):
        order = self.get_object()
        if(order!=None):
            if not request.user == order.user:
                text = "You are not authorized to access this Order"
                return Response({'text': text}, template_name = 'error.html',
                                                 status=status.HTTP_404_NOT_FOUND)
            order_items = OrderItem.objects.all().filter(order=order)
            order_serializer = OrderSerializer(order)
            order_items_serializer = OrderItemSerializer(order_items)
            return Response({'order': order, 'order_items': order_items},
                                                    status=status.HTTP_200_OK)
        else:
            text = "We couldn't find the Order you requested."
            return Response({'text':text}, template_name = 'error.html',
                                             status=status.HTTP_404_NOT_FOUND)


class PizzaDetails(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/pizza_details.html'
    serializer_class = PizzaSerializer

    def get_queryset(self):
        return Pizza.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs['pk']
        queryset = queryset.filter(pk=pk)
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return None
        return obj

    def get(self, request,*args, **kwargs):
        pizza = self.get_object()
        if(pizza!=None):
            serializer = PizzaSerializer(pizza)
            return Response({'pizza' : serializer.data}, status=status.HTTP_200_OK)
        else:
            text = "We couldn't find the Pizza you requested."
            return Response({'text':text}, template_name = 'error.html', status=status.HTTP_404_NOT_FOUND)
