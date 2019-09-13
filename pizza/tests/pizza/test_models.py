from django.test import TestCase
from pizza.models import Pizza


class PizzaTest(TestCase):
    fixtures = ['pizza.json']

    @classmethod
    def setUpTestData(cls):
        cls.pizza = Pizza.objects.get(pk=1)

    def test_str_returns_name(self):
        self.assertEquals('Pizza Carbonara', self.pizza.__str__())

    def test_get_absolute_url(self):
        self.assertEquals('/pizza/details/1/', self.pizza.get_absolute_url())
