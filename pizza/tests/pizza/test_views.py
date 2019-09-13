from django.test import TestCase
from pizza.models import Pizza
from django.contrib.auth.models import User


class PizzaViewsAnonymousUserTest(TestCase):

    fixtures = ['pizza.json']

    @classmethod
    def setUpTestData(cls):
        cls.pizza = Pizza.objects.get(pk=1)

    def test_pizza_details(self):
        response = self.client.get('/pizza/details/1/')
        self.assertEquals(200, response.status_code)

    def test_pizza_details_raises_404(self):
        response = self.client.get('/pizza/details/2/')
        self.assertEquals(404, response.status_code)


class PizzaViewsLoggedUserTest(TestCase):

    fixtures = ['users.json', 'pizza.json']

    @classmethod
    def setUpTestData(cls):
        cls.pizza = Pizza.objects.get(pk=1)

    def setUp(self):
        self.response = self.client.force_login(User.objects.get(pk=2))

    def test_pizza_details(self):
        self.response = self.client.get('/pizza/details/1/')
        self.assertEquals(200, self.response.status_code)

    def test_pizza_details_raises_404(self):
        self.response = self.client.get('/pizza/details/2/')
        self.assertEquals(404, self.response.status_code)
