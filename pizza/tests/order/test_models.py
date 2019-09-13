from django.test import TestCase
from order.models import Order, OrderItem, Pizza
from django.contrib.auth.models import User


# Create your tests here.
class OrderTest(TestCase):
    fixtures = ['users.json', 'orders.json', 'pizza.json']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=2)
        cls.pizza = Pizza.objects.get(pk=1)

    def setUp(self):
        self.order = Order.objects.get(pk=1)

    def test_str_returns_date_and_status(self):
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-09-09 | Status: Open")
        self.order.status = "C"
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-09-09 | Status: Confirmed")
        self.order.status = "P"
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-09-09 | Status: Paid")
        self.order.status = "D"
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-09-09 | Status: Delivered")

    def test_get_absolute_url(self):
        self.assertEquals(self.order.get_absolute_url(),
                          '/order/order_details/1/')

    def test_when_order_is_created_order_amount_is_0(self):
        self.order = Order.objects.create(user=User.objects.get(pk=3))
        self.assertEquals(self.order.get_amount(), 0)

    def test_order_amount_is_calculated_correctly_with_one_order_item(self):
        self.assertEquals(self.order.get_amount(), 50)

    def test_order_amount_is_calculated_correctly_with_two_order_items(self):
        OrderItem.objects.create(order=self.order, pizza_type=self.pizza,
                                 quantity=2)
        self.assertEquals(self.order.get_amount(), 70)


class OrderItemTest(TestCase):
    fixtures = ['users.json', 'orders.json', 'pizza.json']
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(pk=2)
        cls.pizza = Pizza.objects.get(pk=1)
        cls.order = Order.objects.create(user=cls.user)

    def test_when_order_is_created_order_item_is_created(self):
        self.assertEquals(self.order.order_items.count(), 1)

    def test_when_order_is_created_order_item_fields_are_blank(self):
        self.order = Order.objects.create(user=self.user)
        self.order.save()
        self.assertEquals(self.order.order_items.get().pizza_type, None)
        self.assertEquals(self.order.order_items.get().quantity, 0)
