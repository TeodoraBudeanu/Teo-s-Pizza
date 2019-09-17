from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from unittest import skip


class AnonymousUserTest(TestCase):

    fixtures = ['users.json']

    def test_home_page(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_login_page(self):
        response = self.client.login(username='johnny', password='loginpass0')
        self.assertTrue(response)

    def test_login_page_inactive_user(self):
        response = self.client.login(username='bob', password='loginpass0')
        self.assertFalse(response)


class UserLoggedInTest(TestCase):

    fixtures = ['users.json']

    def setUp(self):
        self.user = User.objects.get(pk=2)
        self.response = self.client.login(username='johnny',
                                          password='loginpass0')

    def test_account_view(self):
        self.response = self.client.get('/account')
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account.html')

    def test_email_view(self):
        self.response = self.client.post('', {'first_name': 'Teo',
                                              'last_name': 'Budeanu',
                                              'email': 'teo.bud@mail.com',
                                              'message': 'message',
                                              'subject': 'Test'})
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'home.html')

    def test_email_is_sent(self):
        self.response = self.client.post('', {'first_name': 'Teo',
                                              'last_name': 'Budeanu',
                                              'email': 'teo.bud@mail.com',
                                              'message': 'message',
                                              'subject': 'Test'})
        self.assertEquals(len(mail.outbox), 1)
        self.assertEquals(mail.outbox[0].subject, 'Test')

    def test_password_change_view(self):
        self.response = self.client.get('/accounts/password/change')
        self.assertEquals(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'password_change.html')

    def test_password_is_changed_by_user(self):
        user = User.objects.get(pk=2)
        old_password = user.password
        self.response = self.client.post('/accounts/password/change',
                                         {'oldpassword': 'loginpass0',
                                          'password1': 'newpass0',
                                          'password2': 'newpass0'})
        self.client.logout()
        self.response = self.client.login(username='johnny',
                                          password='newpass0')
        user.refresh_from_db()
        new_password = user.password
        self.assertFalse(old_password == new_password)

    def test_logged_out_user_is_redirected_lo_login(self):
        self.response = self.client.post('/logout/')
        self.response = self.client.get('/order/place_order')
        self.assertEquals(self.response.status_code, 302)
        self.assertEquals(self.response.url,
                          '/accounts/login/?next=/order/place_order')

    def test_logout_page(self):
        self.response = self.client.get('/logout/')
        self.assertTrue(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/logout.html')

    def test_signup_page(self):
        self.client.logout()
        self.response = self.client.get('/accounts/signup')
        self.assertTrue(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account_signup.html')

    def test_signup_page_post(self):
        self.client.logout()
        self.response = self.client.post('/accounts/signup',
                                         {'username': 'teo',
                                          'first_name': 'teo',
                                          'last_name': 'bud',
                                          'email': 'teo.bud@mail.com',
                                          'phone': '0111111111',
                                          'password1': 'loginpass2',
                                          'password2': 'loginpass2'})
        self.assertEquals(self.response.status_code, 302)
        self.assertEquals(self.response.url, '/accounts/')
        self.assertEquals(User.objects.last().username, 'teo')
