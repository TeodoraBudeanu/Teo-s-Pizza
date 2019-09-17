from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem, Pizza
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


# Create your views here.
@method_decorator(login_required, name='dispatch')
class PlaceOrder(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'form.html'
    serializer_class = OrderSerializer
    style_vert = {'template_pack': 'rest_framework/vertical/'}
    style_hor = {'template_pack': 'rest_framework/inline/'}
    queryset = Order.objects.exclude(status='P')

    def get_object(self, queryset=queryset, *args, **kwargs):
        if (queryset.filter(user=self.request.user).count()):
            order = queryset.get(user=self.request.user)
            order.status = 'O'
            order.save()
        else:
            order = Order(user=self.request.user)
            order.save()
        return order

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order_ser = OrderSerializer(order)
        order_items_ser = []
        oi_query = order.order_items.all()
        for item in oi_query:
            order_items_ser.append(OrderItemSerializer(item))
        return Response({'order_ser': order_ser, 'order_items_ser':
                        order_items_ser, 'order': order, 'style_vert':
                        self.style_vert, 'style_hor': self.style_hor})


@method_decorator(login_required, name='dispatch')
class SaveOrder(generics.GenericAPIView):

    def get(self, request):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        order.address = request.GET.get('address')
        order.comment = request.GET.get('comment')
        order.save()
        return JsonResponse(1, safe=False)


@method_decorator(login_required, name='dispatch')
class ConfirmOrder(generics.GenericAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "confirmation.html"
    queryset = Order.objects.all()

    def get(self, request, format=None):
        order = Order.objects.filter(status='O').get(user=request.user)
        order.status = 'C'
        order_items = order.order_items.all()
        if order.comment == "":
            order.comment = "-"
        order.save()
        for item in order_items:
            if item.pizza_type is None:
                item.delete()
        return Response({'order': order, 'orderItems': order_items})

    def post(self, request, format=None):
        order = Order.objects.filter(status='C').get(user=request.user)
        order.status = 'P'
        order.date = timezone.now().date()
        order.save()
        order_items = order.order_items.all()
        for item in order_items:
            item.pizza_type.stock -= item.quantity
            item.pizza_type.save()
        return redirect(order)


class CheckTotal(generics.GenericAPIView):
    def get(self, request):
        order_id = request.GET.get('order_id')
        order = get_object_or_404(Order, pk=order_id)
        return JsonResponse(order.get_amount(), safe=False)


@method_decorator(login_required, name='dispatch')
class OrderDetails(generics.RetrieveAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'odetails.html'
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get(self, request, queryset=queryset, *args, **kwargs):
        pk = self.kwargs['pk']
        if(queryset.filter(pk=pk).count()):
            order = queryset.get(pk=pk)
            if not request.user == order.user:
                raise PermissionDenied
            order_items = order.order_items.all()
            return Response({'order': order, 'order_items': order_items})
        text = "We couldn't find the Order you requested."
        return Response({'text': text}, template_name='error.html',
                        status=status.HTTP_404_NOT_FOUND)


@method_decorator(login_required, name='dispatch')
class OrderList(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'history.html'
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).filter(status='P')

    def get(self, request):
        queryset = self.get_queryset()
        return Response({'orders': queryset})


@method_decorator(login_required, name='dispatch')
class SaveItem(generics.GenericAPIView):

    def get(self, request):
        item_id = request.GET.get('item_id')
        pizza_id = request.GET.get('pizza_id')
        quantity = request.GET.get('quantity')
        item = get_object_or_404(OrderItem, pk=item_id)
        pizza = get_object_or_404(Pizza, pk=pizza_id)
        if pizza.stock >= int(quantity):
            item.pizza_type = Pizza.objects.get(pk=pizza_id)
            item.quantity = quantity
            item.save()
            total = item.order.get_amount()
            return JsonResponse(total, safe=False)
        return JsonResponse('There are only {} {} left in stock.'.format(
                            pizza.stock, pizza.name), safe=False,
                            status=400)


@method_decorator(login_required, name='dispatch')
class CreateItem(generics.GenericAPIView):

    def get(self, request):
        item_id = request.GET.get('old_item_id')
        old_item = OrderItem.objects.get(pk=item_id)
        item = OrderItem(order=old_item.order)
        item.save()
        return JsonResponse(item.id, safe=False)


@method_decorator(login_required, name='dispatch')
class DeleteItem(generics.GenericAPIView):

    def get(self, request):
        item_id = request.GET.get('item_id')
        OrderItem.objects.filter(pk=item_id).delete()
        return JsonResponse(1, safe=False)
