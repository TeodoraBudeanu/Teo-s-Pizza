from django.test import TestCase
from pizza.models import Pizza


class PizzaTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.pizza = Pizza.objects.create(name='Pizza Carbonara',
                                         description='description',
                                         price=10, stock=10)

    def test_str_returns_date_and_status(self):
        self.assertEquals('Pizza Carbonara', self.pizza.__str__())

    def test_get_absolute_url(self):
        self.assertEquals('/pizza/details/1/', self.pizza.get_absolute_url())
