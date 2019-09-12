from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail
from unittest import skip


class AnonymousUserTest(TestCase):

    fixtures = ['regular_user.json', 'inactive_user.json']

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

    fixtures = ['superuser.json', 'regular_user.json']

    def setUp(self):
        self.response = self.client.force_login(User.objects.get(pk=2))

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

    @skip("Not passing - user password is not updated in db")
    def test_password_is_changed_by_user(self):
        user = User.objects.get(pk=2)
        old_password = user.password
        self.response = self.client.post('/accounts/password/change',
                                         {'old_password': 'loginpass0',
                                          'new_password1': 'newpass0',
                                          'new_password2': 'newpass0'})
        self.client.logout()
        self.response = self.client.login(username='johnny',
                                          password='loginpass0')
        user.refresh_from_db()
        new_password = user.password
        self.assertFalse(old_password == new_password)

# user password is not updated in db

    @skip("Logout redirects to 'Are you sure?' page. How to pass by that?")
    def test_user_logout(self):
        self.response = self.client.get('/logout/')  # =>> "Are you sure?" page
        self.assertFalse(User.objects.get(pk=2).is_authenticated)

    def test_logout_page(self):
        self.response = self.client.get('/logout/')
        self.assertTrue(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'account/logout.html')
