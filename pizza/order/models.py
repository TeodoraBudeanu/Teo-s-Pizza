from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from pizza.models import Pizza
# Create your models here.
ORDER_STATUS_CHOICES = (
    ('O', 'Open'),
    ('C', 'Confirmed'),
    ('P', 'Paid'),
)


class OrdersQuerySet(models.QuerySet):
    def orders_for_client(self, user):
        return self.filter(user=user)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=30, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=1, default='O',
                              choices=ORDER_STATUS_CHOICES)
    objects = OrdersQuerySet.as_manager()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "Order {} - {}".format(self.id, self.date)

    def get_amount(self):
        return sum([Pizza.objects.get(pk=ol.pizza_type.id).price * ol.quantity
                   for ol in self.order_items.all()])

    def get_absolute_url(self):
        return reverse('order_details', args=[self.id])


class OrderItem(models.Model):
    pizza_type = models.ForeignKey(Pizza, on_delete=models.CASCADE, blank=True,
                                   null=True)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, related_name='order_items',
                              on_delete=models.CASCADE)
