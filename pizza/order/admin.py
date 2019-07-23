from django.contrib import admin
from .models import Pizza, Order, OrderItem
# Register your models here.

@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'stock', 'img_url')
    list_editable = ('name', 'description', 'price', 'stock', 'img_url')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'comment', 'date', 'confirmed')
    list_editable = ('user', 'address', 'comment', 'confirmed')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'pizza_type', 'quantity', 'order')
    list_editable = ('pizza_type', 'quantity')
