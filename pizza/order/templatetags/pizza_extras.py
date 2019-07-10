from django import template
from order.models import Pizza

register = template.Library()

@register.inclusion_tag('orders/pizza_listing.html')
def pizza_list():
    pizzas = Pizza.objects.all()
    return {'pizza_list' : pizzas}
