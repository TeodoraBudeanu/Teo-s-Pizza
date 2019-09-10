from django.test import TestCase
from order.models import Order, OrderItem, Pizza
from django.contrib.auth.models import User
from django.utils import timezone
import datetime


# Create your tests here.
class OrderTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(password='1234', is_superuser='0',
                                       username='teo', first_name='teo',
                                       last_name='budeanu', email='teo@b.com',
                                       is_staff=0, is_active=1,
                                       date_joined=timezone.now())

        cls.pizza = Pizza.objects.create(name='Pizza Carbonara',
                                         description='description',
                                         price=10, stock=10)

    def setUp(self):
        self.order = Order.objects.create(user=self.user, address='address',
                                          comment='comment',
                                          date=datetime.date(2019, 8, 8))

    def test_str_returns_date_and_status(self):
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-08-08 | Status: Open")
        self.order.status = "C"
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-08-08 | Status: Confirmed")
        self.order.status = "P"
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-08-08 | Status: Paid")
        self.order.status = "D"
        self.assertEquals(self.order.__str__(),
                          "Date: 2019-08-08 | Status: Delivered")

    def test_get_absolute_url(self):
        self.assertEquals(self.order.get_absolute_url(),
                          '/order/order_details/1/')

    def test_when_order_is_created_order_amount_is_0(self):
        self.assertEquals(self.order.get_amount(), 0)

    def test_order_amount_is_calculated_correctly_with_one_order_item(self):
        order_item = OrderItem.objects.get(pk=1)
        order_item.pizza_type = self.pizza
        order_item.quantity = 5
        order_item.save()
        self.assertEquals(self.order.get_amount(), 50)

    def test_order_amount_is_calculated_correctly_with_two_order_items(self):
        order_item = OrderItem.objects.get(pk=1)
        order_item.pizza_type = self.pizza
        order_item.quantity = 5
        order_item.save()
        OrderItem.objects.create(order=self.order, pizza_type=self.pizza,
                                 quantity=2)
        self.assertEquals(self.order.get_amount(), 70)


class OrderItemTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(password='1234', is_superuser='0',
                                       username='teo', first_name='teo',
                                       last_name='budeanu', email='teo@b.com',
                                       is_staff=0, is_active=1,
                                       date_joined=timezone.now())

        cls.pizza = Pizza.objects.create(name='Pizza Carbonara',
                                         description='description',
                                         price=10, stock=10)

        cls.order = Order.objects.create(user=cls.user, address='address',
                                         comment='comment',
                                         date=datetime.date(2019, 8, 8))

    def test_when_order_is_created_order_item_is_created(self):
        self.assertEquals(self.order.order_items.count(), 1)

    def test_when_order_is_created_order_item_fields_are_blank(self):
        self.assertEquals(self.order.order_items.get().pizza_type, None)
        self.assertEquals(self.order.order_items.get().quantity, 0)
