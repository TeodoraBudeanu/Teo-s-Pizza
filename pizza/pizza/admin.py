from django.contrib import admin
from .models import Pizza
# Register your models here.


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', 'price', 'stock', 'image')
    list_editable = ('name', 'description', 'price', 'stock', 'image')
