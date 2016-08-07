"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from payments.forms import SignInForm, UserForm
from django import forms
from django.test import TestCase
from payments.models import User
from pprint import pformat


class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User(email="j@j.com", name='test_user')
        cls.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEquals(str(self.test_user), "j@j.com")

    def test_get_by_id(self):
        self.assertEquals(User.get_by_id(1), self.test_user)


class FormTesterMixin():

    def assert_form_error(self, form_cls, expected_error_name, expected_error_msg, data):

        test_form = form_cls(data=data)
        # if we get an error, the form should not be valid
        self.assertFalse(test_form.is_valid())

        self.assertEquals(
            test_form.errors[expected_error_name],
            expected_error_msg,
            msg="Expected {} : Actual {} : using data {}".format(
                test_form.errors[expected_error_name],
                expected_error_msg, pformat(data)
            )
        )


class FormTests(TestCase, FormTesterMixin):

    def test_signin_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {'data': {'email': 'j@j.com'},
             'error': ('password', [u'This field is required.'])},
            {'data': {'password': '1234'},
             'error': ('email', [u'This field is required.'])}
        ]

        for invalid_data in invalid_data_list:
            self.assert_form_error(SignInForm,
                                   invalid_data['error'][0],
                                   invalid_data['error'][1],
                                   invalid_data["data"])

    def test_user_passwords_match(self):
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '1234',
                'ver_password': '1234',
                'last_4_digits': '3333',
                'stripe_token': '1'
            }
        )

        # Is the data valid? -- if not, output errors
        self.assertTrue(form.is_valid(), form.errors)

        # Will throw an error if the form doesn't clean correctly
        self.assertIsNotNone(form.clean())

    def test_user_form_passwords_dont_match_throws_errors(self):
        form = UserForm(
            {
                'name': 'jj',
                'email': 'j@j.com',
                'password': '1234',
                'ver_password': '123',  # bad password
                'last_4_digits': '3333',
                'stripe_token': '1'
            }
        )

        # Is the data valid?
        self.assertFalse(form.is_valid())

        self.assertRaisesMessage(forms.ValidationError, "Passwords do not match.",
                                 form.clean)
