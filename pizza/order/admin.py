from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'comment', 'date', 'status')
    list_editable = ('user', 'address', 'comment', 'status')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'pizza_type', 'quantity', 'order')
    list_editable = ('pizza_type', 'quantity')
