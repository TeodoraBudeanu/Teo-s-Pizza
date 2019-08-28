from django.contrib import admin
from .models import Pizza
# Register your models here.


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'stock', 'img_url')
    list_editable = ('name', 'description', 'price', 'stock', 'img_url')
