from django.contrib import admin
from .models import Account

# Register your models here.
@admin.register(Account)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'user_id')
    list_editable = ('phone', 'user_id')
