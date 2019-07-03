from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

class Pizza(models.Model):
    name = models.CharField (max_length = 30)
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(30)])

class OrdersQuerySet(models.QuerySet):
    def orders_from_user(self, user):
        return self.filter(user_email=user.email)

class Order(models.Model):
    user_email = models.ForeignKey(User, on_delete=models.CASCADE,
                                                editable=False)
    address = models.CharField(max_length = 30)
    comment = models.TextField()
    objects = OrdersQuerySet.as_manager()

    def get_amount(self):
    #    return sum([ol.amount for ol in self.order_items.all()])

        return sum([Pizza.objects.get(pk=ol.pizza_type).price for ol in self.order_items.all()])

class OrderItem(models.Model):
    pizza_type = models.ForeignKey(Pizza, on_delete=models.CASCADE,
                                                editable=False)
    quantity = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(10)])
    order = models.ForeignKey(Order, related_name='order_items',
                                    on_delete=models.CASCADE)
