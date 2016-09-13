"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".
"""

from payments.forms import SignInForm, UserForm, CardForm
from django import forms
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
import django_ecomm.settings as settings
from payments.models import User
from .views import sign_in, sign_out, soon, register
from pprint import pformat
import mock


class UserModelTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.test_user = User(email="j@j.com", name='test_user')
        cls.test_user.save()

    def test_user_to_string_print_email(self):
        self.assertEquals(str(self.test_user), "j@j.com")

    def test_get_by_id(self):
        self.assertEquals(User.get_by_id(1), self.test_user)


class ViewTesterMixin(object):

    @classmethod
    def setupViewTester(cls, url, view_func, expected_html, status_code=200, session={}):
        request_factory = RequestFactory()
        cls.request = request_factory.get(url)
        cls.request.session = session
        cls.status_code = status_code
        cls.url = url
        cls.view_func = staticmethod(view_func)
        cls.expected_html = expected_html

    def test_resolves_to_correct_view(self):
        test_view = resolve(self.url)
        self.assertEquals(test_view.func, self.view_func)

    def test_returns_appropriate_response_code(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.status_code, self.status_code)

    def test_returns_correct_html(self):
        resp = self.view_func(self.request)
        self.assertEquals(resp.content, self.expected_html)


class SignInPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        html = render_to_response(
            'sign_in.html',
            {
                'form': SignInForm(),
                'user': None
            }
        )

        ViewTesterMixin.setupViewTester(
            '/sign_in',
            sign_in,
            html.content
        )


class SignOutPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        ViewTesterMixin.setupViewTester(
            '/sign_out',
            sign_out,
            "",  # a redirect will return no html
            status_code=302,
            session={"user": "dummy"},

        )

    def setUp(self):
        # sign_out clears the session, so this resets it
        self.request.session = {"user": "dummy"}


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

    def test_card_form_data_validation_for_invalid_data(self):
        invalid_data_list = [
            {
                'data': {'last_4_digits': '123'},
                'error': (
                    'last_4_digits',
                    [u'Ensure this value has at least 4 characters (it has 3).']
                )
            },
            {
                'data': {'last_4_digits': '12345'},
                'error': (
                    'last_4_digits',
                    [u'Ensure this value has at most 4 characters (it has 5).']
                )
            }
        ]

        for invalid_data in invalid_data_list:
            self.assert_form_error(
                CardForm,
                invalid_data['error'][0],
                invalid_data['error'][1],
                invalid_data["data"]
            )


class RegisterPageTests(TestCase, ViewTesterMixin):

    @classmethod
    def setUpClass(cls):
        html = render_to_response(
            'register.html',
            {
                'form': UserForm(),
                'months': range(1, 12),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': range(2011, 2036),
            }
        )
        ViewTesterMixin.setupViewTester(
            '/register',
            register,
            html.content,
        )

    def setUp(self):
        request_factory = RequestFactory()
        self.request = request_factory.get(self.url)

    def test_invalid_form_returns_registration_page(self):

        with mock.patch('payments.forms.UserForm.is_valid') as user_mock:

            user_mock.return_value = False

            self.request.method = 'POST'
            self.request.POST = None
            resp = register(self.request)
            self.assertEquals(resp.content, self.expected_html)

            # ensures is_valid function was called
            self.assertEquals(user_mock.call_count, 1)

    def test_registering_new_user_returns_successfully(self):

        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '4242424242424242',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        with mock.patch('stripe.Customer') as stripe_mock:

            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            resp = register(self.request)
            self.assertEquals(resp.content, "")
            self.assertEquals(resp.status_code, 302)
            self.assertEquals(self.request.session['user'], 1)

            # Verify that the user was actually stored in the database
            # If the user is not there, this will throw an error
            User.objects.get(email='python@rocks.com')

    def test_registering_user_twice_cause_error_msg(self):

        # Creates a user with the same email so we get an integrity error
        user = User(name='pyRock', email='python@rocks.com')
        user.save()

        # Creates the request used to test the view
        self.request.session = {}
        self.request.method = 'POST'
        self.request.POST = {
            'email': 'python@rocks.com',
            'name': 'pyRock',
            'stripe_token': '...',
            'last_4_digits': '4242',
            'password': 'bad_password',
            'ver_password': 'bad_password',
        }

        # Creates the expected form
        expected_form = UserForm(self.request.POST)
        expected_form.is_valid()
        expected_form.add_error('python@rocks.com is already a member.')

        # Creates expected HTML
        html = render_to_response(
            'register.html',
            {
                'form': expected_form,
                'months': range(1, 12),
                'publishable': settings.STRIPE_PUBLISHABLE,
                'soon': soon(),
                'user': None,
                'years': range(2011, 2036),
            }
        )

        # Mock out stripe so test doesn't hit their server
        with mock.patch('stripe.Customer') as stripe_mock:

            config = {'create.return_value': mock.Mock()}
            stripe_mock.configure_mock(**config)

            # Runs the test
            resp = register(self.request)

            # Verifies that things were done correctly
            self.assertEquals(resp.status_code, 200)
            self.assertEquals(self.request.session, {})

            # Asserts there is only one record in the database
            users = User.objects.filter(email="python@rocks.com")
            self.assertEquals(len(users), 1)

            # Verifies that the HTML returned is correct
            self.assertEquals(resp.content, html.content)
