from django.test import TestCase
from unittest import skip
from django.utils import timezone
from order.models import Order, OrderItem, Pizza
from django.contrib.auth.models import User
import datetime


class OrderViewsAnonymousUserTest(TestCase):
    # python3 manage.py test tests.order.test_views.OrderViewsAnonymousUserTest
    def test_user_is_redirected_to_login_when_tries_to_place_order(self):
        response = self.client.get('/order/place_order')
        self.assertEquals(302, response.status_code)
        self.assertEquals('/accounts/login/?next=/order/place_order',
                          response.url)

    def test_user_is_redirected_to_login_when_tries_to_save_order(self):
        response = self.client.get('/order/save_order')
        self.assertEquals(302, response.status_code)
        self.assertEquals('/accounts/login/?next=/order/save_order',
                          response.url)

    def test_user_is_redirected_to_login_when_tries_to_get_confirm_order(self):
        response = self.client.get('/order/confirm_order')
        self.assertEquals(302, response.status_code)
        self.assertEquals('/accounts/login/?next=/order/confirm_order',
                          response.url)

    def test_user_is_redirected_to_login_when_tries_to_confirm_order(self):
        response = self.client.post('/order/confirm_order')
        self.assertEquals(302, response.status_code)
        self.assertEquals('/accounts/login/?next=/order/confirm_order',
                          response.url)


class OrderViewsLoggedInUserTest(TestCase):
    # python3 manage.py test tests.order.test_views.OrderViewsLoggedInUserTest
    fixtures = ['regular_user.json']

    def setUp(self):
        self.response = self.client.force_login(User.objects.get())
        self.order = Order.objects.create(user=User.objects.get(),
                                          date=datetime.date(2019, 9, 9))
        self.pizza = Pizza.objects.create(name="Pizza Carbonara", price="10",
                                          description="Description", stock=10)
        self.order_item = self.order.order_items.get()
        self.order_item.pizza_type = Pizza.objects.get()
        self.order_item.quantity = 5
        self.order_item.save()

    def test_place_order(self):
        self.response = self.client.get('/order/place_order')
        self.assertEquals(200, self.response.status_code)
        self.assertTemplateUsed(self.response, 'form.html')

    def test_when_user_places_order_a_new_order_is_created(self):
        # if an Open/Confirmed order doesn't already exist
        Order.objects.all().delete()
        self.response = self.client.get('/order/place_order')
        self.assertEquals(1, Order.objects.all().count())

    def test_when_user_places_order_status_updates_to_open(self):
        # if an Open/Confirmed order exists
        self.order.status = 'C'
        self.order.save()
        self.assertEquals('C', Order.objects.get().status)
        self.response = self.client.get('/order/place_order')
        self.assertEquals('O', Order.objects.get().status)

    def test_save_order(self):
        self.response = self.client.get('/order/save_order',
                                        {'order_id': 1,
                                         'address': 'test_address'})
        self.assertEquals(200, self.response.status_code)

    def test_when_user_saves_order_address_is_updated(self):
        self.response = self.client.get('/order/save_order',
                                        {'order_id': 1,
                                         'address': 'test_address'})
        self.order.refresh_from_db()
        self.assertEquals('test_address', self.order.address)

    def test_when_user_saves_order_comment_is_updated(self):
        self.response = self.client.get('/order/save_order',
                                        {'order_id': 1,
                                         'comment': 'test_comment'})
        self.order.refresh_from_db()
        self.assertEquals('test_comment', self.order.comment)

    def test_confirm_order_get(self):
        self.response = self.client.get('/order/confirm_order')
        self.assertEquals(200, self.response.status_code)
        self.assertTemplateUsed(self.response, 'confirmation.html')

    def test_confirm_order_post(self):
        self.order.status = 'C'
        self.order.save()
        self.response = self.client.post('/order/confirm_order')
        self.assertRedirects(self.response, '/order/order_details/1/')

    def test_when_user_confirms_order_status_updates_to_confirmed(self):
        self.response = self.client.get('/order/confirm_order')
        self.order.refresh_from_db()
        self.assertEquals('C', self.order.status)

    def test_when_user_pays_order_status_updates_to_paid(self):
        self.order.status = 'C'
        self.order.save()
        self.response = self.client.post('/order/confirm_order')
        self.order.refresh_from_db()
        self.assertEquals('P', self.order.status)

    def test_when_user_pays_order_date_updates_to_current(self):
        self.order.status = 'C'
        self.order.save()
        self.assertFalse(self.order.date is timezone.now().date())
        self.response = self.client.post('/order/confirm_order')
        self.order.refresh_from_db()
        self.assertEquals(self.order.date, timezone.now().date())

    def test_when_order_is_paid_pizza_stock_decreases(self):
        self.order.status = 'C'
        self.order.save()
        self.response = self.client.post('/order/confirm_order')
        self.order.refresh_from_db()
        self.assertEquals(self.order.order_items.get().pizza_type.stock, 5)


class OrderItemViewsAnonymousUserTest(TestCase):
    # python3 manage.py
    # test tests.order.test_views.OrderItemViewsAnonymousUserTest
    def test_user_is_redirected_to_login_when_tries_to_save_item(self):
        response = self.client.get('/order/save_item')
        self.assertEquals(302, response.status_code)
        self.assertEquals('/accounts/login/?next=/order/save_item',
                          response.url)


class OrderItemViewsLoggedInUserTest(TestCase):
    # python3 manage.py
    # test tests.order.test_views.OrderItemViewsLoggedInUserTest
    fixtures = ['regular_user.json']

    def setUp(self):
        self.response = self.client.force_login(User.objects.get())
        self.order = Order.objects.create(user=User.objects.get(),
                                          date=datetime.date(2019, 9, 9))
        self.pizza = Pizza.objects.create(name="Pizza Carbonara", price="10",
                                          description="Description", stock=10)
        self.order_item = self.order.order_items.get()

    def test_order_item_is_saved_when_new_pizza_id_is_provided(self):
        self.order_item.quantity = 0
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 1,
                                         'quantity': 0})
        self.order_item.refresh_from_db()
        self.assertEquals(1, self.order_item.pizza_type.id)

    def test_order_item_is_saved_when_new_quantity_is_provided(self):
        self.order_item.pizza_type = Pizza.objects.get()
        self.order_item.quantity = 0
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 1,
                                         'quantity': 3})
        self.order_item.refresh_from_db()
        self.assertEquals(3, self.order_item.quantity)

    def test_when_non_existent_id_is_provided_save_item_raises_404(self):
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 2, 'pizza_id': 1,
                                         'quantity': 3})
        self.assertEquals(404, self.response.status_code)

    def test_when_non_existent_pizza_id_is_provided_save_item_raises_404(self):
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 2,
                                         'quantity': 3})
        self.assertEquals(404, self.response.status_code)

    def test_when_provided_quantity_is_higher_than_stock_raises_400(self):
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 1,
                                         'quantity': 20})
        self.assertEquals(400, self.response.status_code)

    def test_create_item(self):
        self.assertEquals(1, self.order.order_items.all().count())
        self.response = self.client.get('/order/create_item',
                                        {'old_item_id': 1})
        self.assertEquals(2, self.order.order_items.all().count())

    def test_delete_item(self):
        self.assertEquals(1, self.order.order_items.all().count())
        self.response = self.client.get('/order/delete_item', {'item_id': 1})
        self.assertEquals(0, self.order.order_items.all().count())
