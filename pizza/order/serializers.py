from rest_framework import serializers
from .models import Pizza, Order, OrderItem

class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'name', 'description', 'price', 'stock', 'img_url']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'comment', 'date', 'confirmed']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'pizza_type', 'quantity', 'order']
