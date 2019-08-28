from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, style={'base_template':
                                      'listfieldset.html'})

    class Meta:
        model = Order
        fields = '__all__'

        def create(self, validated_data):
            order_items_data = validated_data.pop('order_items')
            order = Order.objects.create(**validated_data)
            for item_data in order_items_data:
                OrderItem.objects.create(order=order, **item_data)
            return order
