from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError

from .models import Order, OrderItem


class OrderItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['user'].widget.attrs['readonly'] = True

    class Meta:
        model = OrderItem
        exclude = ['confirmed']

class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['pizza_type'].widget.attrs['readonly'] = True

    class Meta:
        model = Order
        exclude = ['confirmed']
        widgets = {
            'comment': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
