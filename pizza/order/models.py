from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from pizza.models import Pizza
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
ORDER_STATUS_CHOICES = (
    ('O', 'Open'),
    ('C', 'Confirmed'),
    ('P', 'Paid'),
    ('D', 'Delivered')
)
DICT_CHOICES = dict(ORDER_STATUS_CHOICES)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=30, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    date = models.DateField(default=timezone.now().date())
    status = models.CharField(max_length=1, default='O',
                              choices=ORDER_STATUS_CHOICES)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "Date: {} | Status: {}".format(self.date,
                                              DICT_CHOICES[self.status])

    def get_amount(self):
        sum = 0
        for oi in self.order_items.all():
            if oi.pizza_type:
                sum = sum + oi.pizza_type.price * oi.quantity
        return sum

    def get_absolute_url(self):
        return reverse('order_details', args=[self.id])


class OrderItem(models.Model):
    pizza_type = models.ForeignKey(Pizza, on_delete=models.CASCADE, blank=True,
                                   null=True)
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, related_name='order_items',
                              on_delete=models.CASCADE)


@receiver(post_save, sender=Order)
def create_order_item(sender, instance, created, **kwargs):
    if created:
        OrderItem.objects.create(order=instance)


@receiver(post_save, sender=Order)
def save_order_item(sender, instance, **kwargs):
    instance.order_items.first().save()
