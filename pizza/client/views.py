from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from order.models import Order
from order.serializers import OrderSerializer
from rest_framework.generics import ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

# Create your views here.

@method_decorator(login_required, name='dispatch')
class OrderList(ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'client/home.html'
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.orders_for_client(self.request.user).filter(confirmed=1)

    def get(self, request):
        queryset = self.get_queryset()
        return Response({'orders' : queryset})
