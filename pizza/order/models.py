from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
# Create your models here.

class Pizza(models.Model):
    name = models.CharField (max_length = 30)
    description = models.TextField()
    price = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(30)])
    img_url = models.CharField(max_length = 50, default = "bg1.jpg")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('pizza_details', args=[self.id])

class OrdersQuerySet(models.QuerySet):
    def orders_for_client(self, user):
        return self.filter(user=user)

    def order_items_for_order(self):
        return self.order_items.all()

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length = 30)
    comment = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)
    objects = OrdersQuerySet.as_manager()
    confirmed = models.IntegerField(default = '0')

    def __str__(self):
        return "Order {} - {}".format(self.id, self.date)

    def get_amount(self):
    #    return sum([ol.amount for ol in self.order_items.all()])
        return sum([Pizza.objects.get(pk=ol.pizza_type.id).price for ol in self.order_items.all()])

    def get_absolute_url(self):
        return reverse('order_summary', args=[self.id])


class OrderItem(models.Model):
    pizza_type = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[MinValueValidator(0),
                                            MaxValueValidator(10)])
    order = models.ForeignKey(Order, related_name='order_items',
                                    on_delete=models.CASCADE, editable=False)
    confirmed = models.IntegerField(default = '0')
