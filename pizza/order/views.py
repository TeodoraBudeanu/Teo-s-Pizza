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
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Create your views here.
@method_decorator(login_required, name='dispatch')
class PlaceOrder(RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/order_form.html'
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(user=self.request.user).filter(confirmed='0')
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            return None
        return obj

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        if(order is None):
            order = Order(user=request.user)
            order.save()
        return Response({'order_id': order.id})

@method_decorator(csrf_exempt, name='dispatch')
class GetOrder(TemplateView):

    def get(self, request):
        order_id = request.GET.get('id')
        order = get_object_or_404(Order, pk=order_id)
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
        import pdb; pdb.set_trace()
        stock = get_object_or_404(Pizza, name=name).stock
        import pdb; pdb.set_trace()
        return JsonResponse(stock)


class SaveOrder(UpdateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'orders/order_details.html'
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        #TODO: populate Date in Order
        order = get_object_or_404(Order, pk=kwargs['pk'])
        order_serializer = OrderSerializer(order, request.data)
        order_items = OrderItem.objects.filter(order=order)
        order_items_serializer = OrderItemSerializer()




        formset = OrderItemFormSet(request.POST, request.FILES)
        if (form.is_valid() and formset.is_valid()):
            order = form.save()
            order.save()
            instances = formset.save(commit=False)
            for i in instances:
                i.order=order
                i.save()
            return redirect('confirm_order')
#        Order.objects.filter(confirmed='0').delete()
#        order = Order(user=request.user)
#        form = OrderForm(instance=order)
#        orderItem = OrderItem(order=order)
#        itemsForm = OrderItemForm(instance=orderItem)
#        OrderItemFormSet = modelformset_factory(OrderItem, exclude=())
#        formset = OrderItemFormSet(queryset=OrderItem.objects.none())
#        return render(request, "orders/order_form.html", {'formOrder' : form,
#                                    'formSetOrderItem': formset})



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
