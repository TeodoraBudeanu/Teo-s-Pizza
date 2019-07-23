from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError
from django import forms

from .models import Order, OrderItem


class OrderItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['user'].widget = forms.HiddenInput()

    class Meta:
        model = OrderItem
        exclude = ['confirmed']

class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['paid'].widget = forms.HiddenInput()
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['pizza_type'].widget.attrs['readonly'] = True
            self.fields['user'].widget = forms.HiddenInput()

    class Meta:
        model = Order
        exclude = ['user', 'confirmed']
        widgets = {
            'comment': Textarea(attrs={'cols': 80, 'rows': 5}),
        }
