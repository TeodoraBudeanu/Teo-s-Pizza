from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account
from django.utils import timezone


class AccountTest(TestCase):
    def test_when_user_is_created_account_is_also_created(self):
        user = User(password='1234', is_superuser='0', username='teo',
                    first_name='teo', last_name='budeanu', email='teo@b.com',
                    is_staff=0, is_active=1, date_joined=timezone.now())
        user.save()
        self.assertEquals(Account.objects.get().user_id, User.objects.get().id)
