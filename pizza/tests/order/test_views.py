from django.test import TestCase
from django.utils import timezone
from order.models import Order, Pizza
from django.contrib.auth.models import User


class OrderViewsAnonymousUserTest(TestCase):
    # python3 manage.py test tests.order.test_views.OrderViewsAnonymousUserTest
    def test_user_is_redirected_to_login_when_tries_to_place_order(self):
        response = self.client.get('/order/place_order')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          '/accounts/login/?next=/order/place_order')

    def test_user_is_redirected_to_login_when_tries_to_save_order(self):
        response = self.client.get('/order/save_order')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          '/accounts/login/?next=/order/save_order')

    def test_user_is_redirected_to_login_when_tries_to_get_confirm_order(self):
        response = self.client.get('/order/confirm_order')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          '/accounts/login/?next=/order/confirm_order')

    def test_user_is_redirected_to_login_when_tries_to_confirm_order(self):
        response = self.client.post('/order/confirm_order')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          '/accounts/login/?next=/order/confirm_order')


class OrderViewsLoggedInUserTest(TestCase):
    # python3 manage.py test tests.order.test_views.OrderViewsLoggedInUserTest
    fixtures = ['users.json', 'orders.json', 'pizza.json']

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.response = self.client.force_login(self.user)
        self.order = Order.objects.get(pk=1)

    def test_place_order(self):
        self.response = self.client.get('/order/place_order')
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'form.html')

    def test_when_user_places_order_a_new_order_is_created(self):
        # if an Open/Confirmed order doesn't already exist
        Order.objects.all().delete()
        self.response = self.client.get('/order/place_order')
        self.assertEquals(Order.objects.all().count(), 1)

    def test_when_user_places_order_status_updates_to_open(self):
        # if an Open/Confirmed order exists
        self.order.status = 'C'
        self.order.save()
        self.assertEquals(Order.objects.get(pk=1).status, 'C')
        self.response = self.client.get('/order/place_order')
        self.assertEquals(Order.objects.get(pk=1).status, 'O')

    def test_save_order(self):
        self.assertFalse(self.order.address == 'test_address')
        self.response = self.client.get('/order/save_order',
                                        {'order_id': 1,
                                         'address': 'test_address'})
        self.assertEquals(self.response.status_code, 200)

    def test_when_user_saves_order_address_is_updated(self):
        self.response = self.client.get('/order/save_order',
                                        {'order_id': 1,
                                         'address': 'test_address'})
        self.order.refresh_from_db()
        self.assertEquals(self.order.address, 'test_address')

    def test_when_user_saves_order_comment_is_updated(self):
        self.response = self.client.get('/order/save_order',
                                        {'order_id': 1,
                                         'comment': 'test_comment'})
        self.order.refresh_from_db()
        self.assertEquals(self.order.comment, 'test_comment')

    def test_confirm_order_get(self):
        self.response = self.client.get('/order/confirm_order')
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'confirmation.html')

    def test_confirm_order_post(self):
        self.order.status = 'C'
        self.order.save()
        self.response = self.client.post('/order/confirm_order')
        self.assertRedirects(self.response, '/order/order_details/1/')

    def test_when_user_confirms_order_status_updates_to_confirmed(self):
        self.response = self.client.get('/order/confirm_order')
        self.order.refresh_from_db()
        self.assertEquals(self.order.status, 'C')

    def test_when_user_pays_order_status_updates_to_paid(self):
        self.order.status = 'C'
        self.order.save()
        self.response = self.client.post('/order/confirm_order')
        self.order.refresh_from_db()
        self.assertEquals(self.order.status, 'P')

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
        self.assertEquals(self.order.order_items.get(pk=1).pizza_type.stock, 5)

    def test_check_total_returns_order_amount(self):
        self.response = self.client.get('/order/check_total', {'order_id': 1})
        self.assertEquals(self.response.content.decode("utf-8"), '50')

    def test_when_non_existent_order_id_is_provided_check_total_raises_404(self):
        self.response = self.client.get('/order/check_total', {'order_id': 2})
        self.assertEquals(self.response.status_code, 404)

    def test_order_details(self):
        self.response = self.client.get('/order/order_details/1/')
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'odetails.html')

    def test_order_details_returns_order(self):
        self.response = self.client.get('/order/order_details/1/')
        self.assertEquals(self.response.context['order'].id, 1)

    def test_order_details_raises_PermissionDenied_to_user(self):
        user = User.objects.get(pk=3)
        self.order.status = "P"
        self.order.save()
        self.response = self.client.force_login(user)
        self.response = self.client.get('/order/order_details/1/')
        self.assertEquals(self.response.status_code, 403)

    def test_when_non_existent_order_id_is_provided_order_details_raises_404(self):
        self.response = self.client.get('/order/order_details/2/')
        self.assertEquals(self.response.status_code, 404)

    def test_order_list(self):
        self.response = self.client.get('/order/history')
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'history.html')

    def test_order_list_returns_list(self):
        self.order.status = "P"
        self.order.save()
        self.response = self.client.get('/order/history')
        self.assertEquals(len(self.response.context['orders']), 1)


class OrderItemViewsAnonymousUserTest(TestCase):
    # python3 manage.py
    # test tests.order.test_views.OrderItemViewsAnonymousUserTest
    def test_user_is_redirected_to_login_when_tries_to_save_item(self):
        response = self.client.get('/order/save_item')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          '/accounts/login/?next=/order/save_item')

    def test_user_is_redirected_to_login_when_tries_to_create_item(self):
        response = self.client.get('/order/save_item')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          '/accounts/login/?next=/order/save_item')

    def test_user_is_redirected_to_login_when_tries_to_delete_item(self):
        response = self.client.get('/order/save_item')
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url,
                          '/accounts/login/?next=/order/save_item')


class OrderItemViewsLoggedInUserTest(TestCase):
    # python3 manage.py
    # test tests.order.test_views.OrderItemViewsLoggedInUserTest
    fixtures = ['users.json', 'orders.json', 'pizza.json']

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.response = self.client.force_login(self.user)
        self.order = Order.objects.get(pk=1)
        self.order_item = self.order.order_items.get(pk=1)

    def test_order_item_is_saved_when_new_pizza_id_is_provided(self):
        self.order_item.quantity = 0
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 1,
                                         'quantity': 0})
        self.order_item.refresh_from_db()
        self.assertEquals(self.order_item.pizza_type.id, 1)

    def test_order_item_is_saved_when_new_quantity_is_provided(self):
        self.order_item.pizza_type = Pizza.objects.get(pk=1)
        self.order_item.quantity = 0
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 1,
                                         'quantity': 3})
        self.order_item.refresh_from_db()
        self.assertEquals(self.order_item.quantity, 3)

    def test_when_non_existent_id_is_provided_save_item_raises_404(self):
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 2, 'pizza_id': 1,
                                         'quantity': 3})
        self.assertEquals(self.response.status_code, 404)

    def test_when_non_existent_pizza_id_is_provided_save_item_raises_404(self):
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 2,
                                         'quantity': 3})
        self.assertEquals(self.response.status_code, 404)

    def test_when_provided_quantity_is_higher_than_stock_raises_400(self):
        self.response = self.client.get('/order/save_item',
                                        {'item_id': 1, 'pizza_id': 1,
                                         'quantity': 20})
        self.assertEquals(self.response.status_code, 400)

    def test_create_item(self):
        self.assertEquals(1, self.order.order_items.all().count())
        self.response = self.client.get('/order/create_item',
                                        {'old_item_id': 1})
        self.assertEquals(self.order.order_items.all().count(), 2)

    def test_delete_item(self):
        self.assertEquals(self.order.order_items.all().count(), 1)
        self.response = self.client.get('/order/delete_item', {'item_id': 1})
        self.assertEquals(self.order.order_items.all().count(), 0)
