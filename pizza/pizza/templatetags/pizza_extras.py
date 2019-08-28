from django import template
from pizza.models import Pizza

register = template.Library()


@register.inclusion_tag('pizza/listing.html')
def pizza_list():
    pizzas = Pizza.objects.all()
    return {'pizza_list': pizzas}
