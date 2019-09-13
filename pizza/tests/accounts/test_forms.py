from django.test import TestCase
from accounts.forms import SignupForm, EmailForm


class SignUpFormTest(TestCase):

    def test_SignupForm_valid(self):
        form = SignupForm(data={'first_name': 'teo', 'last_name': 'budeanu',
                                'email': 'teo@bud.com', 'phone': '0111111111'})
        self.assertTrue(form.is_valid())

    def test_SignupForm_not_valid_missing_first_name(self):
        form = SignupForm(data={'last_name': 'budeanu',
                                'email': 'teo@bud.com', 'phone': '0111111111'})
        self.assertFalse(form.is_valid())

    def test_SignupForm_not_valid_missing_last_name(self):
        form = SignupForm(data={'first_name': 'teo',
                                'email': 'teo@bud.com', 'phone': '0111111111'})
        self.assertFalse(form.is_valid())

    def test_SignupForm_not_valid_missing_email(self):
        form = SignupForm(data={'first_name': 'teo',
                                'email': 'teo@bud.com', 'phone': '0111111111'})
        self.assertFalse(form.is_valid())

    def test_SignupForm_not_valid_missing_phone(self):
        form = SignupForm(data={'first_name': 'teo', 'last_name': 'budeanu',
                                'email': 'teo@bud.com'})
        self.assertFalse(form.is_valid())


class EmailFormTest(TestCase):

    def test_EmailForm_valid(self):
        form = EmailForm(data={'first_name': 'teo', 'last_name': 'budeanu',
                               'email': 'teo@bud.com', 'subject': 'test',
                               'message': 'This is a test.'})
        self.assertTrue(form.is_valid())

    def test_EmailForm_not_valid_missing_first_name(self):
        form = EmailForm(data={'last_name': 'budeanu',
                               'email': 'teo@bud.com', 'subject': 'test',
                               'message': 'This is a test.'})
        self.assertFalse(form.is_valid())

    def test_EmailForm_not_valid_missing_last_name(self):
        form = EmailForm(data={'first_name': 'teo',
                               'email': 'teo@bud.com', 'subject': 'test',
                               'message': 'This is a test.'})
        self.assertFalse(form.is_valid())

    def test_EmailForm_not_valid_missing_email(self):
        form = EmailForm(data={'first_name': 'teo', 'last_name': 'budeanu',
                               'subject': 'test',
                               'message': 'This is a test.'})
        self.assertFalse(form.is_valid())

    def test_EmailForm_not_valid_missing_subject(self):
        form = EmailForm(data={'first_name': 'teo', 'last_name': 'budeanu',
                               'email': 'teo@bud.com',
                               'message': 'This is a test.'})
        self.assertFalse(form.is_valid())

    def test_EmailForm_not_valid_with_invalid_email(self):
        form = EmailForm(data={'first_name': 'teo', 'last_name': 'budeanu',
                               'email': 'teo', 'subject': 'test',
                               'message': 'This is a test.'})
        self.assertFalse(form.is_valid())
